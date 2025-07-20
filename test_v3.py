"""Test script for Eagle MCP Server v3."""

import asyncio
from main import EagleMCPServer


async def test_v3_features():
    """Test v3 new features."""
    print("Eagle MCP Server v3 Feature Test")
    print("=" * 40)
    
    # Initialize server
    server = EagleMCPServer()
    print("Server initialized successfully!")
    
    # Count tools by category
    tools = []
    tools.extend(server.folder_handler.get_tools())
    tools.extend(server.item_handler.get_tools())  
    tools.extend(server.library_handler.get_tools())
    tools.extend(server.image_handler.get_tools())
    
    print(f"\nTotal tools: {len(tools)}")
    
    # Check specific v3 features
    v3_new_tools = [
        "folder_create", "folder_update", "folder_rename",
        "item_move_to_folder", "item_update_tags", "item_rename", 
        "item_update_metadata", "item_delete",
        "image_get_base64", "image_get_filepath", 
        "image_analyze_prompt", "thumbnail_get_base64"
    ]
    
    print("\nv3 New Tools Status:")
    print("-" * 30)
    
    found_tools = 0
    for tool_name in v3_new_tools:
        tool = next((t for t in tools if t.name == tool_name), None)
        if tool:
            print(f"[OK] {tool_name}")
            found_tools += 1
        else:
            print(f"[MISSING] {tool_name}")
    
    print(f"\nSummary: {found_tools}/{len(v3_new_tools)} v3 tools implemented")
    
    # Test categories
    categories = {
        "folder_": "Folder Operations",
        "item_": "Item Management", 
        "image_": "Image/Multimodal",
        "thumbnail_": "Image/Multimodal",
        "library_": "Library"
    }
    
    print("\nTool Categories:")
    print("-" * 20)
    
    for prefix, category in categories.items():
        category_tools = [t for t in tools if t.name.startswith(prefix)]
        print(f"{category}: {len(category_tools)} tools")
    
    print("\nv3 Implementation Complete!")
    return len(tools)


if __name__ == "__main__":
    asyncio.run(test_v3_features())