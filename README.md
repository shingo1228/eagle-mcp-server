# Eagle MCP Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-1.12.0-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Modern Context Protocol (MCP) server implementation for [Eagle App](https://eagle.cool/) integration. This server enables AI assistants to interact with your Eagle library through a standardized interface.

## ✨ Features

- **🏗️ Modern Architecture**: Pure MCP implementation built with mcp-python
- **🛠️ Comprehensive Tools**: 7 specialized tools for complete Eagle operations
- **🔌 Cross-platform**: Compatible with LM Studio, Claude Desktop, and other MCP clients  
- **🛡️ Robust Error Handling**: Comprehensive error handling and logging
- **⚡ High Performance**: Async implementation with efficient Eagle API integration
- **📝 Type Safe**: Full type annotations with Pydantic validation

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- [Eagle App](https://eagle.cool/) running locally (default: `localhost:41595`)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/eagle-mcp-server.git
cd eagle-mcp-server
```

2. Install dependencies:
```bash
uv sync
```

3. Start the server:
```bash
# Windows
run.bat

# Unix/Linux/macOS  
uv run main.py
```

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file for local configuration:

```env
EAGLE_API_URL=http://localhost:41595
EAGLE_API_TIMEOUT=30.0
LOG_LEVEL=INFO
```

### MCP Client Configuration

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "eagle-mcp-server": {
      "command": "/path/to/eagle-mcp-server/run.bat",
      "env": {
        "PYTHONPATH": "/path/to/eagle-mcp-server"
      }
    }
  }
}
```

#### LM Studio

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "eagle-mcp-server": {
      "command": "/path/to/eagle-mcp-server/run.bat",
      "env": {
        "PYTHONPATH": "/path/to/eagle-mcp-server"
      }
    }
  }
}
```

## 🛠️ Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `health_check` | Check Eagle API connection status | None |
| `folder_list` | List all folders in Eagle library | None |
| `folder_search` | Search folders by name | `keyword` |
| `folder_info` | Get detailed folder information | `folder_id` |
| `item_search` | Search items by keyword | `keyword`, `limit?` |
| `item_info` | Get detailed item information | `item_id` |
| `library_info` | Get Eagle library information | None |

## 📁 Project Structure

```
eagle-mcp-server/
├── main.py                 # Main MCP server implementation
├── run.bat                 # Server startup script
├── eagle_client.py         # Eagle API client
├── config.py              # Configuration management
├── handlers/              # Tool handlers
│   ├── folder.py          # Folder operations
│   ├── item.py            # Item operations
│   └── library.py         # Library operations
├── schemas/               # Pydantic schemas
├── tests/                 # Unit tests
├── docs/                  # Documentation
└── scripts/               # Setup scripts
```

## 🧪 Testing

Run the test suite:

```bash
uv run python -m pytest tests/
```

Run basic functionality test:

```bash
uv run python -c "from eagle_client import EagleClient; import asyncio; asyncio.run(EagleClient().health_check())"
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection refused**: Ensure Eagle App is running on the configured port
2. **Module not found**: Check Python path and virtual environment activation
3. **Permission denied**: Verify file permissions on startup scripts

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Install development dependencies: `uv sync --extra dev`
4. Make your changes
5. Run tests: `uv run python -m pytest`
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Eagle App](https://eagle.cool/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)

## 📞 Support

If you encounter any issues or have questions:

1. Check the [troubleshooting guide](docs/TROUBLESHOOTING.md)
2. Search [existing issues](https://github.com/yourusername/eagle-mcp-server/issues)
3. Create a [new issue](https://github.com/yourusername/eagle-mcp-server/issues/new)

---

**Note**: This project requires Eagle App to be installed and running. Eagle App is a powerful digital asset management application available at [eagle.cool](https://eagle.cool/).