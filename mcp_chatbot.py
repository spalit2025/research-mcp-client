#!/usr/bin/env python3
"""
MCP Research Chatbot - A chatbot that connects to an MCP research server
to provide research paper analysis capabilities.
"""

from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List, Optional
import asyncio
import nest_asyncio
import os

nest_asyncio.apply()
load_dotenv()

class MCP_ChatBot:
    """A chatbot that uses MCP tools for research paper analysis."""
    
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.anthropic = Anthropic()
        self.available_tools: List[dict] = []
        
        # Validate API key
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please check your .env file.")
    
    async def process_query(self, query: str) -> None:
        """Process a user query using Claude with MCP tools."""
        messages = [{'role': 'user', 'content': query}]
        
        try:
            response = self.anthropic.messages.create(
                max_tokens=2024,
                model='claude-3-5-sonnet-20241022',  # Updated to latest model
                tools=self.available_tools,
                messages=messages
            )
            
            process_query = True
            while process_query:
                assistant_content = []
                
                for content in response.content:
                    if content.type == 'text':
                        print(content.text)
                        assistant_content.append(content)
                        if len(response.content) == 1:
                            process_query = False
                            
                    elif content.type == 'tool_use':
                        assistant_content.append(content)
                        messages.append({'role': 'assistant', 'content': assistant_content})
                        
                        tool_id = content.id
                        tool_args = content.input
                        tool_name = content.name
                        
                        print(f"\n🔧 Calling tool '{tool_name}' with args: {tool_args}")
                        
                        # Call the MCP tool
                        try:
                            result = await self.session.call_tool(tool_name, arguments=tool_args)
                            
                            # Handle the result content properly
                            result_content = []
                            for item in result.content:
                                if hasattr(item, 'text'):
                                    result_content.append(item.text)
                                else:
                                    result_content.append(str(item))
                            
                            messages.append({
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_id,
                                        "content": "\n".join(result_content)
                                    }
                                ]
                            })
                            
                        except Exception as tool_error:
                            print(f"❌ Error calling tool '{tool_name}': {tool_error}")
                            messages.append({
                                "role": "user",
                                "content": [
                                    {
                                        "type": "tool_result",
                                        "tool_use_id": tool_id,
                                        "content": f"Error: {str(tool_error)}"
                                    }
                                ]
                            })
                        
                        # Get the next response from Claude
                        response = self.anthropic.messages.create(
                            max_tokens=2024,
                            model='claude-3-5-sonnet-20241022',
                            tools=self.available_tools,
                            messages=messages
                        )
                        
                        if len(response.content) == 1 and response.content[0].type == "text":
                            print(f"\n{response.content[0].text}")
                            process_query = False
                            
        except Exception as e:
            print(f"❌ Error processing query: {str(e)}")

    async def chat_loop(self) -> None:
        """Run an interactive chat loop."""
        print("\n🤖 MCP Research Chatbot Started!")
        print("Ask me about research papers, and I'll use my tools to help you.")
        print("Type 'quit' to exit.\n")
        
        while True:
            try:
                query = input("📝 Query: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    print("Please enter a query.")
                    continue
                
                await self.process_query(query)
                print("\n" + "="*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {str(e)}")

    async def connect_to_server_and_run(self) -> None:
        """Connect to the MCP server and start the chat loop."""
        # Create server parameters for stdio connection
        server_params = StdioServerParameters(
            command="python",
            args=["/Users/sandippalit/research-mcp-server/research_server.py"],
            env=None,
        )
        
        print("🔌 Connecting to MCP research server...")
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    self.session = session
                    
                    # Initialize the connection
                    await session.initialize()
                    
                    # List available tools
                    response = await session.list_tools()
                    tools = response.tools
                    
                    print(f"✅ Connected to server with {len(tools)} tools:")
                    for tool in tools:
                        print(f"  • {tool.name}: {tool.description}")
                    
                    self.available_tools = [{
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    } for tool in tools]
                    
                    await self.chat_loop()
                    
        except Exception as e:
            print(f"❌ Failed to connect to MCP server: {str(e)}")
            print("Make sure the research server is available at the specified path.")

async def main():
    """Main entry point."""
    try:
        chatbot = MCP_ChatBot()
        await chatbot.connect_to_server_and_run()
    except Exception as e:
        print(f"❌ Failed to start chatbot: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())