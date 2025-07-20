"""Library handler for Eagle MCP Server."""

from typing import Any, Dict, List

from mcp.types import Tool, TextContent
from eagle_client import EagleClient
from handlers.base import BaseHandler


class LibraryHandler(BaseHandler):
    """Handler for library-related tools."""
    
    def get_tools(self) -> List[Tool]:
        """Get library tools."""
        return [
            Tool(
                name="library_info",
                description="Get information about the Eagle library",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    async def handle_call(self, name: str, arguments: Dict[str, Any], client: EagleClient) -> List[TextContent]:
        """Handle library tool calls."""
        if name == "library_info":
            return await self._get_library_info(client)
        else:
            return self._error_response(f"Unknown library tool: {name}")
    
    async def _get_library_info(self, client: EagleClient) -> List[TextContent]:
        """Get library information."""
        try:
            result = await client.get("/api/library/info")
            
            if not result.get("status") == "success":
                return self._error_response("Failed to get library info")
            
            library = result.get("data", {}).get("library", {})
            
            # Format response
            response = f"Library Information:\n"
            response += f"- Name: {library.get('name', 'Unknown')}\n"
            response += f"- Path: {library.get('path', 'Unknown')}\n"
            
            if library.get('folders'):
                response += f"- Folders: {len(library.get('folders', []))}\n"
            
            if library.get('modificationTime'):
                response += f"- Last Modified: {library.get('modificationTime')}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error getting library info: {e}")