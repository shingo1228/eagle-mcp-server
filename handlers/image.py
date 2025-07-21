"""Image handler for Eagle MCP Server - Multimodal support."""

import base64
import os
import urllib.parse
from typing import Any, Dict, List
from pathlib import Path

from mcp.types import Tool, TextContent, ImageContent
from eagle_client import EagleClient
from handlers.base import BaseHandler
from utils.encoding import get_display_name, clean_response_text, format_japanese_safe


class ImageHandler(BaseHandler):
    """Handler for image-related tools with multimodal support."""
    
    def get_tools(self) -> List[Tool]:
        """Get image tools."""
        return [
            Tool(
                name="image_get_base64",
                description="Get image as Base64 encoded data for LLM analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to get image data"
                        },
                        "use_thumbnail": {
                            "type": "boolean",
                            "description": "Use thumbnail instead of full image (faster, smaller)",
                            "default": True
                        }
                    },
                    "required": ["item_id"]
                }
            ),
            Tool(
                name="image_get_filepath",
                description="Get image file path for LLM analysis",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to get file path"
                        }
                    },
                    "required": ["item_id"]
                }
            ),
            Tool(
                name="image_analyze_prompt",
                description="Prepare image for LLM analysis with custom prompt",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to analyze"
                        },
                        "analysis_prompt": {
                            "type": "string",
                            "description": "Custom prompt for image analysis",
                            "default": "Describe this image in detail"
                        },
                        "use_thumbnail": {
                            "type": "boolean",
                            "description": "Use thumbnail for faster analysis",
                            "default": True
                        }
                    },
                    "required": ["item_id"]
                }
            ),
            Tool(
                name="thumbnail_get_base64",
                description="Get thumbnail image as Base64 for quick preview",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "item_id": {
                            "type": "string",
                            "description": "The ID of the item to get thumbnail"
                        }
                    },
                    "required": ["item_id"]
                }
            )
        ]
    
    async def handle_call(self, name: str, arguments: Dict[str, Any], client: EagleClient) -> List[TextContent]:
        """Handle image tool calls."""
        if name == "image_get_base64":
            if "item_id" not in arguments:
                return self._error_response("Missing required parameter: item_id")
            return await self._get_image_base64(
                arguments["item_id"],
                arguments.get("use_thumbnail", True),
                client
            )
        elif name == "image_get_filepath":
            if "item_id" not in arguments:
                return self._error_response("Missing required parameter: item_id")
            return await self._get_image_filepath(arguments["item_id"], client)
        elif name == "image_analyze_prompt":
            if "item_id" not in arguments:
                return self._error_response("Missing required parameter: item_id")
            return await self._analyze_image_prompt(
                arguments["item_id"],
                arguments.get("analysis_prompt", "Describe this image in detail"),
                arguments.get("use_thumbnail", True),
                client
            )
        elif name == "thumbnail_get_base64":
            if "item_id" not in arguments:
                return self._error_response("Missing required parameter: item_id")
            return await self._get_thumbnail_base64(arguments["item_id"], client)
        else:
            return self._error_response(f"Unknown image tool: {name}")
    
    async def _get_image_base64(self, item_id: str, use_thumbnail: bool, client: EagleClient) -> List[TextContent]:
        """Get image as Base64 encoded data."""
        try:
            # Get item info first
            item_info = await client.get("/api/item/info", {"id": item_id})
            if not item_info.get("status") == "success":
                return self._error_response(f"Failed to get item info for ID: {item_id}")
            
            item = item_info.get("data", {})
            item = clean_response_text(item)
            
            if use_thumbnail:
                # Get thumbnail path
                thumbnail_result = await client.get("/api/item/thumbnail", {"id": item_id})
                if not thumbnail_result.get("status") == "success":
                    return self._error_response(f"Failed to get thumbnail for ID: {item_id}")
                
                image_path = thumbnail_result.get("data")
                if image_path:
                    image_path = urllib.parse.unquote(image_path)
            else:
                # Construct full image path from thumbnail path using actual file extension
                thumbnail_result = await client.get("/api/item/thumbnail", {"id": item_id})
                if thumbnail_result.get("status") == "success":
                    thumbnail_path = urllib.parse.unquote(thumbnail_result.get("data", ""))
                    if thumbnail_path and "_thumbnail" in thumbnail_path:
                        # Remove _thumbnail and use actual file extension from Eagle API
                        image_path_base = thumbnail_path.replace("_thumbnail", "")
                        image_path_without_ext = os.path.splitext(image_path_base)[0]
                        original_ext = item.get('ext', 'jpg')
                        image_path = f"{image_path_without_ext}.{original_ext}"
                    else:
                        image_path = None
                else:
                    image_path = None
            
            if not image_path or not os.path.exists(image_path):
                return self._error_response(f"Image file not found: {image_path}")
            
            # Read and encode image
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Determine MIME type
            file_ext = Path(image_path).suffix.lower()
            mime_type_map = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg', 
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
                '.bmp': 'image/bmp'
            }
            mime_type = mime_type_map.get(file_ext, 'image/jpeg')
            
            # Format response with metadata
            name = get_display_name(item, 'Unnamed Image')
            response = f"Image Base64 Data for {name}:\n\n"
            response += f"- Item ID: {item_id}\n"
            response += f"- File Type: {item.get('ext', 'unknown')}\n"
            response += f"- MIME Type: {mime_type}\n"
            response += f"- Source: {'Thumbnail' if use_thumbnail else 'Full Image'}\n"
            response += f"- Image Path: {image_path}\n\n"
            response += f"Base64 Data (length: {len(image_data)} chars):\n"
            response += f"data:{mime_type};base64,{image_data}"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error getting image Base64: {e}")
    
    async def _get_image_filepath(self, item_id: str, client: EagleClient) -> List[TextContent]:
        """Get image file path."""
        try:
            # Get item info
            item_info = await client.get("/api/item/info", {"id": item_id})
            if not item_info.get("status") == "success":
                return self._error_response(f"Failed to get item info for ID: {item_id}")
            
            item = item_info.get("data", {})
            item = clean_response_text(item)
            
            # Get thumbnail path and construct full image path
            thumbnail_result = await client.get("/api/item/thumbnail", {"id": item_id})
            if not thumbnail_result.get("status") == "success":
                return self._error_response(f"Failed to get thumbnail path for ID: {item_id}")
            
            thumbnail_path = urllib.parse.unquote(thumbnail_result.get("data", ""))
            if not thumbnail_path:
                return self._error_response(f"No file path found for item: {item_id}")
            
            # Construct full image path using the actual file extension from Eagle API
            # Eagle always creates PNG thumbnails, but we need the original file extension
            file_path_base = thumbnail_path.replace("_thumbnail", "") if "_thumbnail" in thumbnail_path else thumbnail_path
            
            # Remove the thumbnail's extension and use the original file extension
            file_path_without_ext = os.path.splitext(file_path_base)[0]
            original_ext = item.get('ext', 'jpg')  # Get actual extension from Eagle API
            file_path = f"{file_path_without_ext}.{original_ext}"
            
            # Check if files exist
            file_exists = os.path.exists(file_path)
            thumbnail_exists = os.path.exists(thumbnail_path)
            
            # Format response
            name = get_display_name(item, 'Unnamed Image')
            response = f"Image File Paths for {name}:\n\n"
            response += f"- Item ID: {item_id}\n"
            response += f"- Full Image: {file_path}\n"
            response += f"- File Exists: {'Yes' if file_exists else 'No'}\n"
            response += f"- Thumbnail: {thumbnail_path}\n"
            response += f"- Thumbnail Exists: {'Yes' if thumbnail_exists else 'No'}\n"
            response += f"- File Size: {item.get('size', 0)} bytes\n"
            if item.get('width') and item.get('height'):
                response += f"- Dimensions: {item.get('width')}x{item.get('height')}\n"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error getting image file path: {e}")
    
    async def _analyze_image_prompt(self, item_id: str, analysis_prompt: str, use_thumbnail: bool, client: EagleClient) -> List[TextContent]:
        """Prepare image for LLM analysis with custom prompt."""
        try:
            # Get image Base64 data
            base64_result = await self._get_image_base64(item_id, use_thumbnail, client)
            
            if base64_result[0].type == "text" and "Error:" in base64_result[0].text:
                return base64_result  # Return error as-is
            
            # Get item info for context
            item_info = await client.get("/api/item/info", {"id": item_id})
            item = item_info.get("data", {}) if item_info.get("status") == "success" else {}
            
            # Format analysis prompt with context
            name = get_display_name(item, 'Unnamed Image')
            response = f"Image Analysis Setup for {name}:\n\n"
            response += f"Analysis Prompt: {analysis_prompt}\n\n"
            response += f"Image Context:\n"
            response += f"- Item ID: {item_id}\n"
            response += f"- Name: {name}\n"
            response += f"- Type: {item.get('ext', 'unknown')}\n"
            if item.get('tags'):
                safe_tags = [format_japanese_safe(tag) for tag in item.get('tags', [])]
                response += f"- Current Tags: {', '.join(safe_tags)}\n"
            if item.get('annotation'):
                safe_annotation = format_japanese_safe(item.get('annotation', ''))
                response += f"- Annotation: {safe_annotation}\n"
            
            response += f"\n{base64_result[0].text}"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error preparing image analysis: {e}")
    
    async def _get_thumbnail_base64(self, item_id: str, client: EagleClient) -> List[TextContent]:
        """Get thumbnail as Base64 for quick preview."""
        try:
            # Get thumbnail path
            thumbnail_result = await client.get("/api/item/thumbnail", {"id": item_id})
            if not thumbnail_result.get("status") == "success":
                return self._error_response(f"Failed to get thumbnail for ID: {item_id}")
            
            thumbnail_path = urllib.parse.unquote(thumbnail_result.get("data", ""))
            if not thumbnail_path or not os.path.exists(thumbnail_path):
                return self._error_response(f"Thumbnail file not found: {thumbnail_path}")
            
            # Read and encode thumbnail
            with open(thumbnail_path, "rb") as thumb_file:
                thumb_data = base64.b64encode(thumb_file.read()).decode('utf-8')
            
            # Get file info
            file_ext = Path(thumbnail_path).suffix.lower()
            mime_type = 'image/jpeg' if file_ext in ['.jpg', '.jpeg'] else 'image/png'
            
            response = f"Thumbnail Base64 Data for Item {item_id}:\n\n"
            response += f"- Thumbnail Path: {thumbnail_path}\n"
            response += f"- MIME Type: {mime_type}\n"
            response += f"- Data Length: {len(thumb_data)} characters\n\n"
            response += f"data:{mime_type};base64,{thumb_data}"
            
            return self._success_response(response)
            
        except Exception as e:
            return self._error_response(f"Error getting thumbnail Base64: {e}")