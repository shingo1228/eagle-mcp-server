"""Item handler for Eagle MCP Server with management operations."""

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
            ),
            Tool(
                name="item_move_to_folder",
                description="Move item to a specific folder",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to move"
                        },
                        "folder_id": {
                            "type": "string",
                            "description": "The ID of the destination folder"
                        }
                    },
                    "required": ["item_id", "folder_id"]
                }
            ),
            Tool(
                name="item_update_tags",
                description="Update item tags",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item"
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "New tags for the item"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["replace", "add", "remove"],
                            "description": "How to update tags (replace, add, or remove)",
                            "default": "replace"
                        }
                    },
                    "required": ["item_id", "tags"]
                }
            ),
            Tool(
                name="item_rename",
                description="Rename an item",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to rename"
                        },
                        "new_name": {
                            "type": "string",
                            "description": "New name for the item"
                        }
                    },
                    "required": ["item_id", "new_name"]
                }
            ),
            Tool(
                name="item_update_metadata",
                description="Update item metadata (annotation, rating, etc.)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item"
                        },
                        "annotation": {
                            "type": "string",
                            "description": "New annotation for the item"
                        },
                        "star": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": 5,
                            "description": "Star rating (0-5)"
                        }
                    },
                    "required": ["item_id"]
                }
            ),
            Tool(
                name="item_delete",
                description="Move item to trash (delete)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to delete"
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
        elif name == "item_move_to_folder":
            return await self._move_item_to_folder(
                arguments["item_id"],
                arguments["folder_id"],
                client
            )
        elif name == "item_update_tags":
            return await self._update_item_tags(
                arguments["item_id"],
                arguments["tags"],
                arguments.get("mode", "replace"),
                client
            )
        elif name == "item_rename":
            return await self._rename_item(
                arguments["item_id"],
                arguments["new_name"],
                client
            )
        elif name == "item_update_metadata":
            return await self._update_item_metadata(
                arguments["item_id"],
                arguments.get("annotation"),
                arguments.get("star"),
                client
            )
        elif name == "item_delete":
            return await self._delete_item(arguments["item_id"], client)
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
    
    async def _move_item_to_folder(self, item_id: str, folder_id: str, client: EagleClient) -> List[TextContent]:
        """Move item to a specific folder."""
        try:
            data = {
                "id": item_id,
                "folders": [folder_id]
            }
            
            result = await client.post("/api/item/update", data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to move item '{item_id}' to folder '{folder_id}'")
            
            response = f"Item moved successfully:\n"
            response += f"- Item ID: {item_id}\n"
            response += f"- Destination Folder ID: {folder_id}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error moving item: {e}")
    
    async def _update_item_tags(self, item_id: str, tags: List[str], mode: str, client: EagleClient) -> List[TextContent]:
        """Update item tags."""
        try:
            if mode != "replace":
                # Get current tags for add/remove operations
                item_info = await client.get("/api/item/info", {"id": item_id})
                if not item_info.get("status") == "success":
                    return self._error_response(f"Failed to get current tags for item '{item_id}'")
                
                current_tags = item_info.get("data", {}).get("tags", [])
                
                if mode == "add":
                    # Add new tags to existing ones
                    updated_tags = list(set(current_tags + tags))
                elif mode == "remove":
                    # Remove specified tags from existing ones
                    updated_tags = [tag for tag in current_tags if tag not in tags]
                else:
                    return self._error_response(f"Invalid mode '{mode}'. Use 'replace', 'add', or 'remove'")
            else:
                updated_tags = tags
            
            data = {
                "id": item_id,
                "tags": updated_tags
            }
            
            result = await client.post("/api/item/update", data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to update tags for item '{item_id}'")
            
            response = f"Item tags updated successfully:\n"
            response += f"- Item ID: {item_id}\n"
            response += f"- Mode: {mode}\n"
            response += f"- New Tags: {', '.join(updated_tags)}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error updating item tags: {e}")
    
    async def _rename_item(self, item_id: str, new_name: str, client: EagleClient) -> List[TextContent]:
        """Rename an item."""
        try:
            data = {
                "id": item_id,
                "name": new_name
            }
            
            result = await client.post("/api/item/update", data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to rename item '{item_id}'")
            
            response = f"Item renamed successfully:\n"
            response += f"- Item ID: {item_id}\n"
            response += f"- New Name: {new_name}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error renaming item: {e}")
    
    async def _update_item_metadata(self, item_id: str, annotation: str, star: int, client: EagleClient) -> List[TextContent]:
        """Update item metadata."""
        try:
            data = {"id": item_id}
            
            if annotation is not None:
                data["annotation"] = annotation
            if star is not None:
                data["star"] = star
            
            if len(data) == 1:  # Only item_id provided
                return self._error_response("No metadata provided (annotation or star required)")
            
            result = await client.post("/api/item/update", data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to update metadata for item '{item_id}'")
            
            response = f"Item metadata updated successfully:\n"
            response += f"- Item ID: {item_id}\n"
            if annotation is not None:
                response += f"- New Annotation: {annotation}\n"
            if star is not None:
                response += f"- New Rating: {star} stars\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error updating item metadata: {e}")
    
    async def _delete_item(self, item_id: str, client: EagleClient) -> List[TextContent]:
        """Move item to trash (delete)."""
        try:
            data = {"itemIds": [item_id]}
            
            result = await client.post("/api/item/moveToTrash", data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to delete item '{item_id}'")
            
            response = f"Item moved to trash successfully:\n"
            response += f"- Item ID: {item_id}\n"
            response += f"- Status: Moved to trash (can be restored from Eagle's trash)\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error deleting item: {e}")