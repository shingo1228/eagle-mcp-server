"""Base handler for Eagle MCP Server."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from mcp.types import Tool, TextContent
from eagle_client import EagleClient


class BaseHandler(ABC):
    """Base class for tool handlers."""
    
    @abstractmethod
    def get_tools(self) -> List[Tool]:
        """Get list of tools provided by this handler."""
        pass
    
    @abstractmethod
    async def handle_call(self, name: str, arguments: Dict[str, Any], client: EagleClient) -> List[TextContent]:
        """Handle a tool call."""
        pass
    
    def _success_response(self, text: str) -> List[TextContent]:
        """Create a successful response."""
        return [TextContent(type="text", text=text)]
    
    def _error_response(self, text: str) -> List[TextContent]:
        """Create an error response."""
        return [TextContent(type="text", text=text)]