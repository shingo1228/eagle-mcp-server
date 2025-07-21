# Eagle MCP Server

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-1.12.0-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/shingo1228/eagle-mcp-server/releases)

[🇯🇵 日本語](README.jp.md) | **English**

A Modern Context Protocol (MCP) server implementation for [Eagle App](https://eagle.cool/) integration. This server enables AI assistants to interact with your Eagle library through a standardized interface with comprehensive tools and multilingual support.

## ✨ Features

- **🏗️ Modern Architecture**: Pure MCP implementation built with mcp-python
- **🛠️ Comprehensive Tools**: 16 high-level tools + 17 direct API tools for complete Eagle operations
- **🎛️ Configurable API Access**: Toggle between user-friendly and advanced developer tools
- **🌏 Multilingual Support**: Enhanced Japanese text handling and UTF-8 encoding
- **🖼️ Image Processing**: Base64 encoding, thumbnail generation, and metadata analysis
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
git clone https://github.com/shingo1228/eagle-mcp-server.git
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

# Tool Configuration
EXPOSE_DIRECT_API_TOOLS=false  # Set to true for advanced API access

# Optional: Custom paths
# USER_DATA_DIR=/custom/path/to/data
# CACHE_DIR=/custom/path/to/cache
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

### Core Tools (Always Available)

| Tool | Description | Parameters |
|------|-------------|------------|
| `health_check` | Check Eagle API connection status | None |

### Folder Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `folder_list` | List all folders in Eagle library | None |
| `folder_search` | Search folders by name | `keyword` |
| `folder_info` | Get detailed folder information | `folder_id` |
| `folder_create` | Create a new folder | `folder_name`, `parent_id?` |
| `folder_update` | Update folder properties | `folder_id`, `folder_name?`, `description?` |
| `folder_rename` | Rename a folder | `folder_id`, `new_name` |

### Item Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `item_search` | Search items by keyword | `keyword`, `limit?` |
| `item_info` | Get detailed item information | `item_id` |
| `item_by_folder` | Get items in a specific folder | `folder_id`, `limit?` |
| `item_update_tags` | Update item tags | `item_id`, `tags`, `mode?` |
| `item_update_metadata` | Update item metadata | `item_id`, `annotation?`, `star?` |
| `item_delete` | Move item to trash | `item_id` |

### Image Processing

| Tool | Description | Parameters |
|------|-------------|------------|
| `image_info` | Get image file paths and metadata | `item_id` |
| `image_base64` | Get image as base64 data | `item_id`, `use_thumbnail?` |
| `image_analyze` | Set up image for AI analysis | `item_id`, `analysis_prompt`, `use_thumbnail?` |
| `thumbnail_path` | Get thumbnail file path | `item_id` |

### Library Management

| Tool | Description | Parameters |
|------|-------------|------------|
| `library_info` | Get Eagle library information | None |

### Direct API Tools (Advanced)

> 💡 **Note**: Enable with `EXPOSE_DIRECT_API_TOOLS=true` for low-level Eagle API access (17 additional tools)

When enabled, provides direct access to Eagle's REST API endpoints for advanced users and developers.

## 🤖 AI Integration

### System Prompts for AI Assistants

To help AI assistants effectively use Eagle MCP Server, we provide comprehensive system prompts:

- **[Complete System Prompt](docs/SYSTEM_PROMPT.md)** - Detailed guide with workflows and best practices
- **[Concise System Prompt](docs/SYSTEM_PROMPT_CONCISE.md)** - Quick reference for AI integration
- **[Japanese System Prompt](docs/SYSTEM_PROMPT.jp.md)** - 日本語版システムプロンプト

These prompts include:
- 33 tool usage patterns and workflows
- Best practices for efficient operations
- Error handling and user interaction guidelines
- Response format recommendations
- Performance optimization tips

### Integration Examples

```python
# Example: AI assistant using Eagle MCP Server
from mcp import ClientSession

# 1. Always start with health check
await session.call_tool("health_check")

# 2. Discover content structure  
library = await session.call_tool("library_info")
folders = await session.call_tool("folder_list")

# 3. Search and analyze
items = await session.call_tool("item_search", {"keyword": "design", "limit": 10})
image_data = await session.call_tool("image_base64", {"item_id": "abc123", "use_thumbnail": true})
```

## 📁 Project Structure

```
eagle-mcp-server/
├── main.py                 # Main MCP server implementation
├── run.bat                 # Server startup script (Windows)
├── eagle_client.py         # Eagle API client
├── config.py              # Configuration management
├── handlers/              # Tool handlers
│   ├── base.py            # Base handler class
│   ├── folder.py          # Folder operations (6 tools)
│   ├── item.py            # Item operations (6 tools)
│   ├── library.py         # Library operations (1 tool)
│   ├── image.py           # Image processing (4 tools)
│   └── direct_api.py      # Direct API access (17 tools)
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── encoding.py        # Text encoding utilities
├── schemas/               # Pydantic schemas
├── tests/                 # Unit tests
├── debug/                 # Debug scripts
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
# Basic health check
uv run python -c "from eagle_client import EagleClient; import asyncio; asyncio.run(EagleClient().health_check())"

# Test with Direct API tools enabled
EXPOSE_DIRECT_API_TOOLS=true uv run python debug/simple_test.py

# Run comprehensive test
uv run python test_v3.py
```

## 🐛 Troubleshooting

### Common Issues

1. **Connection refused**: Ensure Eagle App is running on the configured port (default: 41595)
2. **Module not found**: Check Python path and virtual environment activation
3. **Permission denied**: Verify file permissions on startup scripts
4. **Japanese text issues**: Ensure UTF-8 encoding is properly configured
5. **Direct API tools not visible**: Set `EXPOSE_DIRECT_API_TOOLS=true` in your environment

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
2. Search [existing issues](https://github.com/shingo1228/eagle-mcp-server/issues)
3. Create a [new issue](https://github.com/shingo1228/eagle-mcp-server/issues/new)

---

**Note**: This project requires Eagle App to be installed and running. Eagle App is a powerful digital asset management application available at [eagle.cool](https://eagle.cool/).