# Contributing to Eagle MCP Server

Thank you for your interest in contributing to Eagle MCP Server! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- [Eagle App](https://eagle.cool/) for testing
- Git

### Development Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/eagle-mcp-server.git
   cd eagle-mcp-server
   ```

3. Install development dependencies:
   ```bash
   uv sync --extra dev
   ```

4. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
uv run python -m pytest

# Run with coverage
uv run python -m pytest --cov=. --cov-report=html

# Run specific test file
uv run python -m pytest tests/test_eagle_client.py
```

### Testing with Real Eagle Instance

1. Ensure Eagle App is running on `localhost:41595`
2. Run integration tests:
   ```bash
   uv run python -c "from eagle_client import EagleClient; import asyncio; print('✅ Connected' if asyncio.run(EagleClient().health_check()) else '❌ Failed')"
   ```

## 📝 Code Style

### Python Style Guidelines

- Follow [PEP 8](https://pep8.org/)
- Use type hints for all function signatures
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Code Formatting

We use `ruff` for code formatting and linting:

```bash
# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check --fix .
```

### Type Checking

```bash
# Run type checking
uv run mypy .
```

## 🏗️ Architecture Guidelines

### Adding New Tools

1. Create handler in `handlers/` directory
2. Inherit from `BaseHandler`
3. Implement required methods:
   ```python
   class YourHandler(BaseHandler):
       def get_tools(self) -> List[Tool]:
           # Return tool definitions
           
       async def handle_call(self, name: str, arguments: Dict[str, Any], client: EagleClient) -> List[TextContent]:
           # Handle tool execution
   ```

4. Register handler in `main.py`
5. Add tests in `tests/`

### Error Handling

- Use `EagleAPIError` for Eagle API-related errors
- Return appropriate `TextContent` responses
- Log errors appropriately with context

### Documentation

- Update README.md if adding new features
- Add docstrings to all public functions
- Update tool documentation table

## 📋 Pull Request Process

1. **Create Issue**: For major changes, create an issue first to discuss
2. **Feature Branch**: Create a feature branch from `main`
3. **Implementation**: 
   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation
4. **Testing**: Ensure all tests pass
5. **Commit Messages**: Use clear, descriptive commit messages
6. **Pull Request**: 
   - Fill out the PR template
   - Link related issues
   - Request review

### Commit Message Format

```
type(scope): brief description

Detailed description if needed

Fixes #issue-number
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(handlers): add new search tool for items`
- `fix(client): handle connection timeout gracefully`
- `docs: update installation instructions`

## 🐛 Reporting Issues

### Bug Reports

Include:
- Eagle App version
- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

### Feature Requests

Include:
- Clear description of the feature
- Use case and motivation
- Proposed implementation (if any)
- Examples of similar features

## 🔧 Development Tips

### Local Configuration

Create `.env.local` for development:
```env
EAGLE_API_URL=http://localhost:41595
LOG_LEVEL=DEBUG
```

### Debugging

1. Enable debug logging:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. Use the debug tools in `debug/` folder for reference

### Testing Against Different Eagle Versions

Test compatibility with different Eagle App versions when possible.

## 📚 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Eagle App API Documentation](https://api.eagle.cool/)
- [Python Async/Await Guide](https://docs.python.org/3/library/asyncio.html)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🤝 Community

- Be respectful and inclusive
- Help others learn and grow
- Share knowledge and best practices
- Follow our Code of Conduct

## ❓ Questions?

- Check existing [Issues](https://github.com/yourusername/eagle-mcp-server/issues)
- Create a new issue with the "question" label
- Join discussions in existing PRs

Thank you for contributing to Eagle MCP Server! 🎉