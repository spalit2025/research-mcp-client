# 🤖 Multi-Server AI Assistant

A Claude AI chatbot with advanced MCP (Model Context Protocol) integration that connects to multiple servers simultaneously for enhanced research, analysis, and productivity capabilities.

## ✨ Features

- 🤖 **Interactive Chat Interface** - Natural conversation with Claude AI
- 🔧 **Multi-Server MCP Integration** - Connect to multiple MCP servers simultaneously
- 📚 **Research & Analysis** - Search arXiv, analyze papers, and access academic resources
- 🗂️ **File System Access** - Read, write, and manage files through MCP servers
- 🌐 **Web Search** - Access real-time information through search APIs
- 🗄️ **Database Operations** - Query and manage databases via MCP tools
- 🎯 **Intelligent Tool Selection** - Claude automatically chooses the best tools for each task
- ⚡ **Async Performance** - Fast, responsive interactions across all servers
- 🛡️ **Robust Error Handling** - Graceful handling of server failures and tool errors
- 🔄 **Dynamic Configuration** - Easy server management through JSON configuration

## 🔗 Related Projects

- [research-mcp-server](https://github.com/spalit2025/research-mcp-server) - Academic research tools for arXiv integration
- [MCP Official Servers](https://github.com/modelcontextprotocol) - Collection of official MCP server implementations

## 📋 Prerequisites

- **Python 3.10+**
- **UV package manager** ([Installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Anthropic API key** ([Get one here](https://console.anthropic.com/))
- **One or more MCP servers** - See [Configuration](#-configuration) for setup options

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/spalit2025/research-mcp-client.git
cd research-mcp-client
```

### 2. Install Dependencies
```bash
uv sync
```

### 3. Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 4. Configure MCP Servers
```bash
cp server_config.example.json server_config.json
# Edit server_config.json to configure your MCP servers
```

### 5. Run the Chatbot
```bash
uv run mcp_chatbot.py
```

## 💬 Usage Examples

The chatbot can now handle diverse tasks across multiple domains:

### Research & Academic
```
📝 Query: Search for papers about machine learning transformers
📝 Query: Extract information from paper ID 2301.07041
📝 Query: Find recent papers on quantum computing
```

### Web Content & Information Fetching
```
📝 Query: Fetch the content from https://arxiv.org/abs/2301.07041
📝 Query: Get the latest news from a technology website
📝 Query: Fetch and summarize content from a research blog
```

### File Operations
```
📝 Query: Read the contents of my project README
📝 Query: Create a summary document from these files
📝 Query: List all Python files in the current directory
📝 Query: Show me the directory structure of my project
```

### Combined Operations
```
📝 Query: Search for AI papers, fetch their abstracts, and save to a file
📝 Query: Read my research notes and find related papers on arXiv
📝 Query: Fetch web content and save it to a local file for analysis
```

### Commands
- Type your queries naturally - Claude will choose the appropriate tools
- Use `quit`, `exit`, or `q` to exit
- Press `Ctrl+C` to interrupt

## 🏗️ Project Structure

```
research-mcp-client/
├── mcp_chatbot.py              # Main multi-server chatbot application
├── server_config.json          # Your MCP server configurations
├── server_config.example.json  # Example server configurations
├── pyproject.toml              # Project dependencies
├── .env.example                # Environment variables template
├── .env                        # Your API key (create from .env.example)
├── README.md                   # This file
└── .venv/                      # Virtual environment (created by uv)
```

## 🔧 How It Works

1. **Configuration Loading** - Reads server configurations from `server_config.json`
2. **Multi-Server Connection** - Establishes connections to all configured MCP servers
3. **Tool Discovery** - Automatically discovers and aggregates tools from all servers
4. **Query Processing** - User queries are processed by Claude AI with access to all available tools
5. **Intelligent Routing** - Claude selects the appropriate server and tool for each task
6. **Response Integration** - Results from multiple tools are seamlessly integrated into responses

## 🛠️ Configuration

### Server Configuration File

Create a `server_config.json` file to define your MCP servers:

```json
{
  "mcpServers": {
    "research-server": {
      "command": "python",
      "args": ["/path/to/research-mcp-server/research_server.py"],
      "env": null
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": null
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/allowed/directory"],
      "env": null
    },
    "web-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key-here"
      }
    },
    "database": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "/path/to/database.db"],
      "env": null
    }
  }
}
```

### Available MCP Servers

Popular MCP servers you can integrate:

- **Research Server** - Academic paper search and analysis (custom implementation)
- **Fetch Server** - Web content fetching and HTTP requests (`uvx mcp-server-fetch`)
- **Filesystem Server** - File and directory operations (`npx @modelcontextprotocol/server-filesystem`)
- **Brave Search** - Web search capabilities (`npx @modelcontextprotocol/server-brave-search`)
- **SQLite Server** - Database query and management (`npx @modelcontextprotocol/server-sqlite`)
- **Git Server** - Git repository operations
- **Slack Server** - Slack integration and messaging
- **Google Drive Server** - Google Drive file access

### Current Working Configuration

The project includes a working configuration with these servers:

1. **Research Server** (2 tools)
   - `search_papers` - Search arXiv papers by topic
   - `extract_info` - Extract information about specific papers

2. **Fetch Server** (1 tool)
   - `fetch` - Fetch web content and convert to markdown

3. **Filesystem Server** (11 tools)
   - `read_file`, `write_file`, `edit_file` - File operations
   - `list_directory`, `directory_tree` - Directory browsing
   - `create_directory`, `move_file` - File management
   - `search_files`, `get_file_info` - File discovery
   - `read_multiple_files`, `list_allowed_directories` - Batch operations

**Total: 14 tools available across 3 servers**

### Environment Variables

Required environment variables in `.env`:
- `ANTHROPIC_API_KEY` - Your Anthropic API key

Optional environment variables for specific servers:
- `BRAVE_API_KEY` - For Brave search functionality
- `GOOGLE_APPLICATION_CREDENTIALS` - For Google services
- Other API keys as required by your chosen servers

## 🐛 Troubleshooting

### Configuration Issues
- ✅ Ensure `server_config.json` exists and is valid JSON
- ✅ Check that all server paths and commands are correct
- ✅ Verify required environment variables are set

### Connection Issues
- ✅ Test each server independently before adding to configuration
- ✅ Check server dependencies are installed (Node.js for npx servers)
- ✅ Verify file paths and permissions

### API Issues
- ✅ Verify your `ANTHROPIC_API_KEY` is set correctly in `.env`
- ✅ Ensure you have sufficient API credits
- ✅ Check your internet connection for web-based servers

### Tool Errors
- ✅ Check individual server logs for detailed error information
- ✅ Verify tool arguments match expected schemas
- ✅ Ensure all required API keys are configured

### Common Solutions
```bash
# Reinstall dependencies
uv sync

# Test server configuration
python -c "import json; print(json.load(open('server_config.json')))"

# Check individual server
npx @modelcontextprotocol/inspector python /path/to/server.py

# Verify API key
echo $ANTHROPIC_API_KEY
```

## 🔄 Development

### Adding New Servers
1. Install the MCP server following its documentation
2. Add server configuration to `server_config.json`
3. Test the server independently
4. Restart the chatbot to discover new tools

### Making Changes
1. Edit `mcp_chatbot.py` for core functionality
2. Update `server_config.json` for server configurations
3. Update `pyproject.toml` for dependencies
4. Test with your configured servers
5. Update documentation as needed

### Server Development
- The chatbot automatically discovers new tools from any server
- No client-side changes needed when server tools are updated
- Focus on improving the chat interface and error handling
- Consider server-specific error handling for better user experience

## 📦 Dependencies

- **[anthropic](https://github.com/anthropics/anthropic-sdk-python)** - Claude AI API client
- **[mcp](https://github.com/modelcontextprotocol/python-sdk)** - Model Context Protocol implementation
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[nest-asyncio](https://github.com/erdewit/nest_asyncio)** - Async support for interactive environments

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and test with multiple servers
4. Ensure configuration examples are updated
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [Model Context Protocol](https://modelcontextprotocol.io/) for the excellent framework
- [MCP Community](https://github.com/modelcontextprotocol) for server implementations
- [arXiv](https://arxiv.org/) for providing access to research papers

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review your `server_config.json` configuration
3. Test individual servers with MCP Inspector
4. Look at existing [Issues](https://github.com/spalit2025/research-mcp-client/issues)
5. Create a new issue with detailed information about your problem

---

**Happy exploring with multiple MCP servers! 🚀✨** 