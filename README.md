# 🤖 AI Research Assistant

A Claude AI chatbot with MCP (Model Context Protocol) integration for intelligent paper search, analysis, and academic discovery.

## ✨ Features

- 🤖 **Interactive Chat Interface** - Natural conversation with Claude AI
- 🔧 **MCP Integration** - Seamless connection to research server tools
- 📚 **Paper Search & Analysis** - Search arXiv and analyze research papers
- 🎯 **Tool-based Responses** - Enhanced capabilities through MCP tools
- ⚡ **Async Performance** - Fast, responsive interactions
- 🛡️ **Error Handling** - Robust error management and user feedback

## 🔗 Related Projects

- [research-mcp-server](https://github.com/spalit2025/research-mcp-server) - The MCP server that provides research tools for this client

## 📋 Prerequisites

- **Python 3.10+**
- **UV package manager** ([Installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- **Anthropic API key** ([Get one here](https://console.anthropic.com/))
- **Access to research MCP server** - Clone and set up [research-mcp-server](https://github.com/spalit2025/research-mcp-server)

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

### 4. Set Up the Research Server
Make sure you have the research server running. Follow the setup instructions at:
[research-mcp-server](https://github.com/spalit2025/research-mcp-server)

### 5. Run the Chatbot
```bash
uv run mcp_chatbot.py
```

## 💬 Usage Examples

Once the chatbot is running, try these queries:

```
📝 Query: Search for papers about machine learning
📝 Query: Find research on neural networks and transformers
📝 Query: Extract information from paper_1
📝 Query: What are the latest developments in AI?
```

### Commands
- Type your research queries naturally
- Use `quit`, `exit`, or `q` to exit
- Press `Ctrl+C` to interrupt

## 🏗️ Project Structure

```
research-mcp-client/
├── mcp_chatbot.py      # Main chatbot application
├── pyproject.toml      # Project dependencies
├── .env.example        # Environment variables template
├── .env                # Your API key (create from .env.example)
├── README.md           # This file
└── .venv/              # Virtual environment (created by uv)
```

## 🔧 How It Works

1. **Connection** - The chatbot connects to your MCP research server using stdio communication
2. **Tool Discovery** - Automatically discovers available tools from the server
3. **Query Processing** - User queries are processed by Claude AI with access to MCP tools
4. **Tool Execution** - When Claude decides to use a tool, it's executed on the MCP server
5. **Response Integration** - Results are seamlessly integrated back into the conversation

## 🛠️ Configuration

### Server Path Configuration
The chatbot is configured to connect to the research server. If your server is in a different location, update the path in `mcp_chatbot.py`:

```python
server_params = StdioServerParameters(
    command="python",
    args=["/path/to/your/research-mcp-server/research_server.py"],
    env=None,
)
```

### Environment Variables
Required environment variables in `.env`:
- `ANTHROPIC_API_KEY` - Your Anthropic API key

## 🐛 Troubleshooting

### Connection Issues
- ✅ Ensure the research server path is correct
- ✅ Make sure the research server can run independently
- ✅ Check that all server dependencies are installed

### API Issues
- ✅ Verify your `ANTHROPIC_API_KEY` is set correctly in `.env`
- ✅ Ensure you have sufficient API credits
- ✅ Check your internet connection

### Tool Errors
- ✅ Check the research server logs for detailed error information
- ✅ Verify the tool arguments match the expected schema
- ✅ Ensure the research server is running and accessible

### Common Solutions
```bash
# Reinstall dependencies
uv sync

# Check if server runs independently
cd /path/to/research-mcp-server
python research_server.py

# Verify API key
echo $ANTHROPIC_API_KEY
```

## 🔄 Development

### Making Changes
1. Edit `mcp_chatbot.py` for core functionality
2. Update `pyproject.toml` for dependencies
3. Test with your research server
4. Update documentation as needed

### Adding New Features
- The chatbot automatically discovers new tools from the MCP server
- No client-side changes needed when server tools are updated
- Focus on improving the chat interface and error handling

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
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP framework
- [arXiv](https://arxiv.org/) for providing access to research papers

## 📞 Support

If you encounter any issues or have questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Look at existing [Issues](https://github.com/spalit2025/research-mcp-client/issues)
3. Create a new issue with detailed information about your problem

---

**Happy researching! 🔬✨** 