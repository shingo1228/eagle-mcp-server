"""Folder handler for Eagle MCP Server with CRUD operations."""

import json
from typing import Any, Dict, List

from mcp.types import Tool, TextContent
from eagle_client import EagleClient
from handlers.base import BaseHandler
from utils.encoding import create_safe_summary, get_display_name, clean_response_text, format_japanese_safe


class FolderHandler(BaseHandler):
    """Handler for folder-related tools."""
    
    def get_tools(self) -> List[Tool]:
        """Get folder tools."""
        return [
            Tool(
                name="folder_list",
                description="List all folders in the Eagle library",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="folder_search",
                description="Search for folders by name",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "Search keyword for folder name"
                        }
                    },
                    "required": ["keyword"]
                }
            ),
            Tool(
                name="folder_info",
                description="Get detailed information about a specific folder",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "folder_id": {
                            "type": "string",
                            "description": "The ID of the folder"
                        }
                    },
                    "required": ["folder_id"]
                }
            ),
            Tool(
                name="folder_create",
                description="Create a new folder in Eagle library",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "folder_name": {
                            "type": "string",
                            "description": "Name of the new folder"
                        },
                        "parent_id": {
                            "type": "string",
                            "description": "Parent folder ID (optional)",
                            "default": ""
                        }
                    },
                    "required": ["folder_name"]
                }
            ),
            Tool(
                name="folder_update",
                description="Update folder properties (name, description)",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "folder_id": {
                            "type": "string",
                            "description": "The ID of the folder to update"
                        },
                        "folder_name": {
                            "type": "string",
                            "description": "New folder name (optional)"
                        },
                        "description": {
                            "type": "string",
                            "description": "New folder description (optional)"
                        }
                    },
                    "required": ["folder_id"]
                }
            ),
            Tool(
                name="folder_rename",
                description="Rename a folder",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "folder_id": {
                            "type": "string",
                            "description": "The ID of the folder to rename"
                        },
                        "new_name": {
                            "type": "string",
                            "description": "New name for the folder"
                        }
                    },
                    "required": ["folder_id", "new_name"]
                }
            )
        ]
    
    async def handle_call(self, name: str, arguments: Dict[str, Any], client: EagleClient) -> List[TextContent]:
        """Handle folder tool calls."""
        if name == "folder_list":
            return await self._list_folders(client)
        elif name == "folder_search":
            return await self._search_folders(arguments["keyword"], client)
        elif name == "folder_info":
            if "folder_id" not in arguments:
                return self._error_response("Missing required parameter: folder_id")
            return await self._get_folder_info(arguments["folder_id"], client)
        elif name == "folder_create":
            if "folder_name" not in arguments:
                return self._error_response("Missing required parameter: folder_name")
            return await self._create_folder(
                arguments["folder_name"],
                arguments.get("parent_id", ""),
                client
            )
        elif name == "folder_update":
            if "folder_id" not in arguments:
                return self._error_response("Missing required parameter: folder_id")
            return await self._update_folder(
                arguments["folder_id"],
                arguments.get("folder_name"),
                arguments.get("description"),
                client
            )
        elif name == "folder_rename":
            if "folder_id" not in arguments:
                return self._error_response("Missing required parameter: folder_id")
            if "new_name" not in arguments:
                return self._error_response("Missing required parameter: new_name")
            return await self._rename_folder(
                arguments["folder_id"],
                arguments["new_name"],
                client
            )
        else:
            return self._error_response(f"Unknown folder tool: {name}")
    
    async def _list_folders(self, client: EagleClient) -> List[TextContent]:
        """List all folders."""
        try:
            result = await client.get("/api/folder/list")
            
            if not result.get("status") == "success":
                return self._error_response("Failed to get folder list")
            
            folders = result.get("data", [])
            
            # Clean response data for proper encoding
            folders = clean_response_text(folders)
            
            # Format response with proper Japanese text handling
            response = f"Found {len(folders)} folders:\n\n"
            for folder in folders:
                name = get_display_name(folder, 'Unnamed Folder')
                response += f"- {name} (ID: {folder.get('id', 'Unknown')})\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error listing folders: {e}")
    
    async def _search_folders(self, keyword: str, client: EagleClient) -> List[TextContent]:
        """Search folders by keyword."""
        try:
            result = await client.get("/api/folder/list")
            
            if not result.get("status") == "success":
                return self._error_response("Failed to get folder list")
            
            folders = result.get("data", [])
            folders = clean_response_text(folders)
            
            # Filter by keyword (case-insensitive)
            matching_folders = [
                f for f in folders 
                if keyword.lower() in get_display_name(f).lower()
            ]
            
            if not matching_folders:
                return self._success_response(f"No folders found matching '{keyword}'")
            
            # Use the safe summary function
            response = create_safe_summary(matching_folders, "folders")
            response = f"Search results for '{keyword}':\n\n{response}"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error searching folders: {e}")
    
    async def _get_folder_info(self, folder_id: str, client: EagleClient) -> List[TextContent]:
        """Get detailed folder information."""
        try:
            # Get folder details
            result = await client.get("/api/folder/list")
            
            if not result.get("status") == "success":
                return self._error_response("Failed to get folder list")
            
            folders = result.get("data", [])
            folder = next((f for f in folders if f.get("id") == folder_id), None)
            
            if not folder:
                return self._error_response(f"Folder with ID '{folder_id}' not found")
            
            # Get items in folder with higher limit to get accurate count
            items_result = await client.get("/api/item/list", {"folders": folder_id, "limit": 1000})
            items_count = 0
            sample_items = []
            total_items = 0
            
            if items_result.get("status") == "success":
                items = items_result.get("data", [])
                items_count = len(items)
                total_items = items_count
                sample_items = [item.get("name", "Unknown") for item in items[:5]]
                
                # If we hit the limit, try to get a more accurate count
                if items_count == 1000:
                    # Note: Eagle API doesn't provide total count, so we show 1000+
                    total_items = "1000+"
            
            # Clean response data and get display name
            folder = clean_response_text(folder)
            name = get_display_name(folder, 'Unnamed Folder')
            
            response = f"Folder Information:\n"
            response += f"- Name: {name}\n"
            response += f"- ID: {folder.get('id', 'Unknown')}\n"
            response += f"- Items: {total_items}\n"
            
            # Add folder status information
            if items_count == 0:
                response += f"- Status: Empty folder (no items)\n"
            elif isinstance(total_items, str) and "+" in str(total_items):
                response += f"- Status: Large folder (showing first 1000 items)\n"
            else:
                response += f"- Status: Active folder\n"
            
            if folder.get("description"):
                desc = format_japanese_safe(folder.get('description', ''))
                response += f"- Description: {desc}\n"
            
            # Add creation/modification info if available
            if folder.get("dateCreated"):
                response += f"- Created: {folder.get('dateCreated')}\n"
            if folder.get("dateModified"):
                response += f"- Modified: {folder.get('dateModified')}\n"
            
            # Enhanced sample items display
            if sample_items:
                safe_items = [format_japanese_safe(item) for item in sample_items]
                response += f"- Sample items ({len(sample_items)} of {total_items}):\n"
                for i, item in enumerate(safe_items, 1):
                    response += f"  {i}. {item}\n"
            elif items_count == 0:
                response += f"- Sample items: None (folder is empty)\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error getting folder info: {e}")
    
    async def _create_folder(self, folder_name: str, parent_id: str, client: EagleClient) -> List[TextContent]:
        """Create a new folder."""
        try:
            # Prepare request data
            data = {"folderName": folder_name}
            if parent_id:
                data["parent"] = parent_id
            
            result = await client.post("/api/folder/create", data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to create folder '{folder_name}'")
            
            created_folder = result.get("data", {})
            
            response = f"Folder created successfully:\n"
            response += f"- Name: {created_folder.get('name', folder_name)}\n"
            response += f"- ID: {created_folder.get('id', 'Unknown')}\n"
            if parent_id:
                response += f"- Parent ID: {parent_id}\n"
            response += f"- Creation Time: {created_folder.get('modificationTime', 'Unknown')}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error creating folder: {e}")
    
    async def _update_folder(self, folder_id: str, folder_name: str, description: str, client: EagleClient) -> List[TextContent]:
        """Update folder properties."""
        try:
            # Prepare update data
            update_data = {"folderId": folder_id}
            
            if folder_name:
                update_data["newName"] = folder_name
            if description:
                update_data["newDescription"] = description
            
            if len(update_data) == 1:  # Only folder_id provided
                return self._error_response("No update data provided (folder_name or description required)")
            
            result = await client.post("/api/folder/update", update_data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to update folder '{folder_id}'")
            
            response = f"Folder updated successfully:\n"
            response += f"- Folder ID: {folder_id}\n"
            if folder_name:
                response += f"- New Name: {folder_name}\n"
            if description:
                response += f"- New Description: {description}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error updating folder: {e}")
    
    async def _rename_folder(self, folder_id: str, new_name: str, client: EagleClient) -> List[TextContent]:
        """Rename a folder."""
        try:
            data = {
                "folderId": folder_id,
                "newName": new_name
            }
            
            result = await client.post("/api/folder/update", data)
            
            if not result.get("status") == "success":
                return self._error_response(f"Failed to rename folder '{folder_id}'")
            
            response = f"Folder renamed successfully:\n"
            response += f"- Folder ID: {folder_id}\n"
            response += f"- New Name: {new_name}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error renaming folder: {e}")