# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-07-20

### Added
- Initial release of Eagle MCP Server
- Pure MCP implementation using mcp-python 1.12.0
- 7 comprehensive tools for Eagle App integration:
  - `health_check` - Eagle API connection status
  - `folder_list` - List all folders
  - `folder_search` - Search folders by name
  - `folder_info` - Get detailed folder information
  - `item_search` - Search items by keyword
  - `item_info` - Get detailed item information
  - `library_info` - Get Eagle library information
- Async Eagle API client with robust error handling
- Modular handler architecture
- Full type annotations with Pydantic validation
- Cross-platform compatibility (Windows, macOS, Linux)
- Support for LM Studio and Claude Desktop
- Comprehensive configuration system with environment variables
- Debug tools and development utilities
- Complete documentation and setup guides

### Technical Details
- Python 3.11+ support
- Modern async/await implementation
- Clean separation of concerns with handlers
- Comprehensive error handling and logging
- Test-driven development approach
- UV package manager support

### Fixed
- Resolved "tuple object has no attribute name" error in MCP 1.12.0
- Fixed tool registration and execution compatibility
- Proper return type handling for MCP decorators

[Unreleased]: https://github.com/yourusername/eagle-mcp-server/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/eagle-mcp-server/releases/tag/v0.1.0