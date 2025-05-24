#!/usr/bin/env python3
"""
MCP Research Chatbot - A chatbot that connects to multiple MCP servers
to provide enhanced research and analysis capabilities.
"""

from dotenv import load_dotenv
from anthropic import Anthropic
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List, Dict, TypedDict, Optional
from contextlib import AsyncExitStack
import json
import asyncio
import nest_asyncio
import os

nest_asyncio.apply()
load_dotenv()

class ToolDefinition(TypedDict):
    name: str
    description: str
    input_schema: dict

class MCP_ChatBot:
    """A chatbot that connects to multiple MCP servers for enhanced capabilities."""
    
    def __init__(self):
        # Initialize session and client objects for multiple servers
        self.sessions: List[ClientSession] = []
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()
        self.available_tools: List[ToolDefinition] = []
        self.tool_to_session: Dict[str, ClientSession] = {}
        
        # Validate API key
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables. Please check your .env file.")

    async def connect_to_server(self, server_name: str, server_config: dict) -> None:
        """Connect to a single MCP server."""
        try:
            print(f"🔌 Connecting to {server_name}...")
            
            server_params = StdioServerParameters(**server_config)
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()
            self.sessions.append(session)
            
            # List available tools for this session
            response = await session.list_tools()
            tools = response.tools
            
            print(f"✅ Connected to {server_name} with {len(tools)} tools:")
            for tool in tools:
                print(f"  • {tool.name}: {tool.description}")
                
                # Map tool to session and add to available tools
                self.tool_to_session[tool.name] = session
                self.available_tools.append({
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.inputSchema
                })
                
        except Exception as e:
            print(f"❌ Failed to connect to {server_name}: {e}")
            # Continue with other servers even if one fails

    async def connect_to_servers(self) -> None:
        """Connect to all configured MCP servers."""
        try:
            config_file = "server_config.json"
            if not os.path.exists(config_file):
                print(f"❌ Configuration file '{config_file}' not found.")
                print("Please create a server_config.json file with your MCP server configurations.")
                raise FileNotFoundError(f"Configuration file '{config_file}' not found")
            
            with open(config_file, "r") as file:
                data = json.load(file)
            
            servers = data.get("mcpServers", {})
            
            if not servers:
                print("❌ No servers configured in server_config.json")
                raise ValueError("No servers configured")
            
            print(f"📋 Found {len(servers)} server(s) in configuration")
            
            for server_name, server_config in servers.items():
                await self.connect_to_server(server_name, server_config)
            
            if not self.available_tools:
                print("❌ No tools available from any server")
                raise RuntimeError("No tools available from any server")
                
            print(f"\n🎉 Successfully connected! Total tools available: {len(self.available_tools)}")
            
        except Exception as e:
            print(f"❌ Error loading server configuration: {e}")
            raise

    async def process_query(self, query: str) -> None:
        """Process a user query using Claude with MCP tools from multiple servers."""
        messages = [{'role': 'user', 'content': query}]
        
        try:
            response = self.anthropic.messages.create(
                max_tokens=2024,
                model='claude-3-5-sonnet-20241022',
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
                        
                        # Call the MCP tool using the appropriate session
                        try:
                            if tool_name not in self.tool_to_session:
                                raise ValueError(f"Tool '{tool_name}' not found in any connected server")
                            
                            session = self.tool_to_session[tool_name]
                            result = await session.call_tool(tool_name, arguments=tool_args)
                            
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
        print("\n🤖 Multi-Server MCP Chatbot Started!")
        print("Ask me anything, and I'll use tools from all connected servers to help you.")
        print("Type 'quit' to exit.\n")
        
        # Show available tools summary
        if self.available_tools:
            print("🛠️  Available tools:")
            for tool in self.available_tools:
                print(f"  • {tool['name']}: {tool['description']}")
            print()
        
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

    async def cleanup(self) -> None:
        """Cleanly close all resources using AsyncExitStack."""
        print("🧹 Cleaning up connections...")
        await self.exit_stack.aclose()

async def main():
    """Main entry point."""
    chatbot = MCP_ChatBot()
    try:
        await chatbot.connect_to_servers()
        await chatbot.chat_loop()
    except Exception as e:
        print(f"❌ Failed to start chatbot: {str(e)}")
    finally:
        await chatbot.cleanup()

if __name__ == "__main__":
    asyncio.run(main())