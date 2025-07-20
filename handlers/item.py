"""Item handler for Eagle MCP Server."""

from typing import Any, Dict, List

from mcp.types import Tool, TextContent
from eagle_client import EagleClient
from handlers.base import BaseHandler


class ItemHandler(BaseHandler):
    """Handler for item-related tools."""
    
    def get_tools(self) -> List[Tool]:
        """Get item tools."""
        return [
            Tool(
                name="item_search",
                description="Search for items by keyword",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "Search keyword"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Maximum number of items to return",
                            "default": 10
                        }
                    },
                    "required": ["keyword"]
                }
            ),
            Tool(
                name="item_info",
                description="Get detailed information about a specific item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item"
                        }
                    },
                    "required": ["item_id"]
                }
            )
        ]
    
    async def handle_call(self, name: str, arguments: Dict[str, Any], client: EagleClient) -> List[TextContent]:
        """Handle item tool calls."""
        if name == "item_search":
            return await self._search_items(arguments.get("keyword"), arguments.get("limit", 10), client)
        elif name == "item_info":
            return await self._get_item_info(arguments["item_id"], client)
        else:
            return self._error_response(f"Unknown item tool: {name}")
    
    async def _search_items(self, keyword: str, limit: int, client: EagleClient) -> List[TextContent]:
        """Search items by keyword."""
        try:
            result = await client.get("/api/item/list", {"keyword": keyword, "limit": limit})
            
            if not result.get("status") == "success":
                return self._error_response("Failed to search items")
            
            items = result.get("data", [])
            
            if not items:
                return self._success_response(f"No items found matching '{keyword}'")
            
            # Format response
            response = f"Found {len(items)} items matching '{keyword}':\n\n"
            for item in items:
                response += f"- {item.get('name', 'Unknown')} ({item.get('ext', 'unknown')})\n"
                response += f"  ID: {item.get('id', 'Unknown')}\n"
                if item.get('tags'):
                    response += f"  Tags: {', '.join(item.get('tags', []))}\n"
                response += "\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error searching items: {e}")
    
    async def _get_item_info(self, item_id: str, client: EagleClient) -> List[TextContent]:
        """Get detailed item information."""
        try:
            result = await client.get("/api/item/info", {"id": item_id})
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to get item info for ID: {item_id}")
            
            item = result.get("data", {})
            
            # Format response
            response = f"Item Information:\n"
            response += f"- Name: {item.get('name', 'Unknown')}\n"
            response += f"- ID: {item.get('id', 'Unknown')}\n"
            response += f"- Type: {item.get('ext', 'unknown')}\n"
            response += f"- Size: {item.get('size', 0)} bytes\n"
            
            if item.get('width') and item.get('height'):
                response += f"- Dimensions: {item.get('width')}x{item.get('height')}\n"
            
            if item.get('tags'):
                response += f"- Tags: {', '.join(item.get('tags', []))}\n"
            
            if item.get('annotation'):
                response += f"- Annotation: {item.get('annotation')}\n"
            
            if item.get('star'):
                response += f"- Rating: {item.get('star')} stars\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error getting item info: {e}")