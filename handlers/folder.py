"""Folder handler for Eagle MCP Server with CRUD operations."""

import json
from typing import Any, Dict, List

from mcp.types import Tool, TextContent
from eagle_client import EagleClient
from handlers.base import BaseHandler


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
            return await self._get_folder_info(arguments["folder_id"], client)
        elif name == "folder_create":
            return await self._create_folder(
                arguments["folder_name"],
                arguments.get("parent_id", ""),
                client
            )
        elif name == "folder_update":
            return await self._update_folder(
                arguments["folder_id"],
                arguments.get("folder_name"),
                arguments.get("description"),
                client
            )
        elif name == "folder_rename":
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
            
            # Format response with ASCII-safe output
            response = f"Found {len(folders)} folders:\n\n"
            for folder in folders:
                name = folder.get('name', 'Unknown')
                # Convert to ASCII to avoid encoding issues
                safe_name = name.encode('ascii', 'replace').decode('ascii')
                response += f"- {safe_name} (ID: {folder.get('id', 'Unknown')})\n"
            
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
            
            # Filter by keyword
            matching_folders = [
                f for f in folders 
                if keyword.lower() in f.get("name", "").lower()
            ]
            
            if not matching_folders:
                return self._success_response(f"No folders found matching '{keyword}'")
            
            # Format response with ASCII-safe output
            response = f"Found {len(matching_folders)} folders matching '{keyword}':\n\n"
            for folder in matching_folders:
                name = folder.get('name', 'Unknown')
                # Convert to ASCII to avoid encoding issues
                safe_name = name.encode('ascii', 'replace').decode('ascii')
                response += f"- {safe_name} (ID: {folder.get('id', 'Unknown')})\n"
            
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
            
            # Get items in folder
            items_result = await client.get("/api/item/list", {"folders": folder_id, "limit": 10})
            items_count = 0
            sample_items = []
            
            if items_result.get("status") == "success":
                items = items_result.get("data", [])
                items_count = len(items)
                sample_items = [item.get("name", "Unknown") for item in items[:5]]
            
            # Format response with ASCII-safe output
            name = folder.get('name', 'Unknown')
            safe_name = name.encode('ascii', 'replace').decode('ascii')
            
            response = f"Folder Information:\n"
            response += f"- Name: {safe_name}\n"
            response += f"- ID: {folder.get('id', 'Unknown')}\n"
            response += f"- Items: {items_count}\n"
            
            if folder.get("description"):
                desc = folder.get('description')
                safe_desc = desc.encode('ascii', 'replace').decode('ascii')
                response += f"- Description: {safe_desc}\n"
            
            if sample_items:
                safe_items = [item.encode('ascii', 'replace').decode('ascii') for item in sample_items]
                response += f"- Sample items: {', '.join(safe_items)}\n"
            
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
            update_data = {"id": folder_id}
            
            if folder_name:
                update_data["folderName"] = folder_name
            if description:
                update_data["description"] = description
            
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
                "id": folder_id,
                "folderName": new_name
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