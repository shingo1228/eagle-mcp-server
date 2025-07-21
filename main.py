"""Eagle MCP Server v2 - Modern implementation."""

import asyncio
import logging
from typing import Any, Dict, List, Optional, Sequence

from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    ListToolsRequest,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

from config import LOG_LEVEL, LOG_FORMAT, MCP_SERVER_NAME, MCP_SERVER_VERSION, MCP_SERVER_DESCRIPTION, EXPOSE_DIRECT_API_TOOLS
from eagle_client import EagleClient, EagleAPIError
from handlers.folder import FolderHandler
from handlers.item import ItemHandler
from handlers.library import LibraryHandler
from handlers.image import ImageHandler
from handlers.direct_api import DirectApiHandler
from utils.encoding import ensure_utf8_output

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class EagleMCPServer:
    """Modern Eagle MCP Server implementation."""
    
    def __init__(self):
        self.server = Server(MCP_SERVER_NAME)
        self.eagle_client = EagleClient()
        
        # Initialize handlers
        self.folder_handler = FolderHandler()
        self.item_handler = ItemHandler()
        self.library_handler = LibraryHandler()
        self.image_handler = ImageHandler()
        self.direct_api_handler = DirectApiHandler()
        
        # Register handlers
        self._register_handlers()
        
        logger.info(f"Initialized {MCP_SERVER_NAME} v{MCP_SERVER_VERSION}")
    
    def _register_handlers(self):
        """Register all tool handlers."""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools."""
            tools = []

            def add_tools_from_handler(handler):
                for tool in handler.get_tools():
                    if hasattr(tool, 'name'):
                        tools.append(tool)
                    else:
                        logger.error(f"Invalid tool without name attribute: {tool}")
            
            # Add tools from abstraction handlers
            add_tools_from_handler(self.folder_handler)
            add_tools_from_handler(self.item_handler)
            add_tools_from_handler(self.library_handler)
            add_tools_from_handler(self.image_handler)
            
            # Add Direct API tools only if configured to expose them
            if EXPOSE_DIRECT_API_TOOLS:
                add_tools_from_handler(self.direct_api_handler)
                logger.info("Direct API tools exposed (EXPOSE_DIRECT_API_TOOLS=true)")
            
            # Add health check tool
            health_tool = Tool(
                name="health_check",
                description="Check Eagle API connection status",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
            tools.append(health_tool)
            
            logger.info(f"Registered {len(tools)} tools")
            
            # Debug: Log each tool in detail
            for i, tool in enumerate(tools):
                logger.info(f"Tool {i}: name={tool.name}, type={type(tool)}")
                logger.info(f"  - description: {tool.description}")
                logger.info(f"  - inputSchema: {tool.inputSchema}")
            
            logger.info(f"Returning {len(tools)} tools as List[Tool]")
            
            return tools
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool calls."""
            logger.info(f"Tool called: {name} with args: {arguments}")
            
            try:
                async with self.eagle_client as client:
                    # Health check
                    if name == "health_check":
                        is_healthy = await client.health_check()
                        return [TextContent(
                            type="text",
                            text=f"Eagle API is {'healthy' if is_healthy else 'unhealthy'}"
                        )]
                    
                    # Route to appropriate handler
                    if name.startswith("api_"):
                        # Check if Direct API tools are exposed
                        if not EXPOSE_DIRECT_API_TOOLS:
                            raise ValueError(f"Direct API tools are not exposed. Set EXPOSE_DIRECT_API_TOOLS=true to enable.")
                        return await self.direct_api_handler.handle_call(name, arguments, client)
                    elif name.startswith("folder_"):
                        return await self.folder_handler.handle_call(name, arguments, client)
                    elif name.startswith("item_"):
                        return await self.item_handler.handle_call(name, arguments, client)
                    elif name.startswith("library_"):
                        return await self.library_handler.handle_call(name, arguments, client)
                    elif name.startswith("image_") or name.startswith("thumbnail_"):
                        return await self.image_handler.handle_call(name, arguments, client)
                    else:
                        raise ValueError(f"Unknown tool: {name}")
                        
            except EagleAPIError as e:
                logger.error(f"Eagle API error in {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"Eagle API error: {e}"
                )]
            except Exception as e:
                logger.error(f"Unexpected error in {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"Unexpected error: {e}"
                )]
    
    async def run(self):
        """Run the MCP server."""
        logger.info("Starting Eagle MCP Server")
        
        # Test Eagle connection
        async with self.eagle_client as client:
            if await client.health_check():
                logger.info("Eagle API connection verified")
            else:
                logger.warning("Eagle API connection failed - server will still start")
        
        # Start stdio server
        async with stdio_server() as (read_stream, write_stream):
            logger.info("MCP server started successfully")
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=MCP_SERVER_NAME,
                    server_version=MCP_SERVER_VERSION,
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )


async def main():
    """Main entry point."""
    # Ensure proper UTF-8 output on Windows
    ensure_utf8_output()
    
    server = EagleMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())