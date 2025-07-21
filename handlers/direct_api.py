"""Direct API handler for Eagle MCP Server."""

import json
from typing import Any, Dict, List

from mcp.types import Tool, TextContent
from eagle_client import EagleClient, EagleAPIError
from handlers.base import BaseHandler

class DirectApiHandler(BaseHandler):
    """Handler for direct Eagle API calls."""

    def get_tools(self) -> List[Tool]:
        """Get all direct API tools."""
        # In a real implementation, these would be loaded from a config file
        # or generated, but for clarity, we define them here.
        tool_definitions = [
            # Application
            {"name": "api_application_info", "description": "Get Eagle application info.", "params": {}},

            # Folder
            {"name": "api_folder_create", "description": "Create a new folder.", "params": {"folderName": "string", "parent": "string"}},
            {"name": "api_folder_rename", "description": "Rename a folder.", "params": {"folderId": "string", "newName": "string"}},
            {"name": "api_folder_update", "description": "Update folder details.", "params": {"folderId": "string", "newName": "string", "newDescription": "string", "newColor": "string"}},
            {"name": "api_folder_list", "description": "List all folders.", "params": {}},
            {"name": "api_folder_listRecent", "description": "List recent folders.", "params": {}},

            # Item
            {"name": "api_item_addFromURL", "description": "Add item from a URL.", "params": {"url": "string", "name": "string", "folderId": "string", "tags": "array", "annotation": "string"}},
            {"name": "api_item_addFromURLs", "description": "Add items from multiple URLs.", "params": {"items": "array", "folderId": "string"}},
            {"name": "api_item_addFromPath", "description": "Add item from a local path.", "params": {"path": "string", "name": "string", "folderId": "string", "tags": "array"}},
            {"name": "api_item_addBookmark", "description": "Add a bookmark.", "params": {"url": "string", "name": "string", "base64": "string", "tags": "array", "folderId": "string"}},
            {"name": "api_item_info", "description": "Get item details.", "params": {"id": "string"}},
            {"name": "api_item_list", "description": "Search for items.", "params": {"limit": "integer", "keyword": "string", "folders": "string", "tags": "string", "ext": "string"}},
            {"name": "api_item_moveToTrash", "description": "Move items to trash.", "params": {"itemIds": "array"}},
            {"name": "api_item_update", "description": "Update item metadata.", "params": {"id": "string", "tags": "array", "annotation": "string", "star": "integer", "url": "string"}},

            # Library
            {"name": "api_library_info", "description": "Get library info.", "params": {}},
            {"name": "api_library_history", "description": "Get library history.", "params": {}},
            {"name": "api_library_switch", "description": "Switch to a different library.", "params": {"libraryPath": "string"}},
        ]

        tools = []
        for tool_def in tool_definitions:
            properties = {}
            required = []
            for param, param_type in tool_def["params"].items():
                properties[param] = {"type": param_type}
                # Simple logic to make params required if they are part of the core functionality
                if "Id" in param or "Name" in param or "URL" in param or "Path" in param or "items" in param:
                    required.append(param)

            tools.append(Tool(
                name=tool_def["name"],
                description=tool_def["description"],
                inputSchema={
                    "type": "object",
                    "properties": properties,
                    "required": list(set(required)) # Ensure no duplicates
                }
            ))
        return tools

    async def handle_call(self, name: str, arguments: Dict[str, Any], client: EagleClient) -> List[TextContent]:
        """Handle direct API tool calls."""
        try:
            # Use EagleClient's helper method for endpoint determination
            endpoint, method = client.get_endpoint_and_method(name)
            
            # Use EagleClient's direct_api_call helper method
            result = await client.direct_api_call(
                endpoint=endpoint, 
                method=method, 
                params=arguments if method == "GET" else None,
                data=arguments if method == "POST" else None
            )

            # Return the raw JSON response as a string
            return self._success_response(json.dumps(result, indent=2, ensure_ascii=False))

        except EagleAPIError as e:
            return self._error_response(f"Eagle API error in {name}: {e}")
        except Exception as e:
            return self._error_response(f"Unexpected error in {name}: {e}")

