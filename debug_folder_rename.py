"""Debug script for folder_rename issue."""

import asyncio
import json
from main import EagleMCPServer


async def test_folder_rename():
    """Test folder_rename functionality."""
    print("=== Folder Rename Debug Test ===")
    
    server = EagleMCPServer()
    
    # Test 1: Check tool definition
    folder_tools = server.folder_handler.get_tools()
    rename_tool = next((t for t in folder_tools if t.name == "folder_rename"), None)
    
    if rename_tool:
        print("[OK] folder_rename tool found")
        print(f"Description: {rename_tool.description}")
        print(f"Input Schema: {json.dumps(rename_tool.inputSchema, indent=2)}")
        print(f"Required fields: {rename_tool.inputSchema['required']}")
    else:
        print("[ERROR] folder_rename tool NOT found")
        return
    
    # Test 2: Get folder list to find a test folder
    print("\n=== Getting folder list ===")
    try:
        async with server.eagle_client as client:
            folders_result = await server.folder_handler.handle_call(
                "folder_list", {}, client
            )
            print("Folder list result:")
            print(folders_result[0].text)
            
    except Exception as e:
        print(f"[ERROR] Error getting folder list: {e}")
        return
    
    # Test 3: Simulate folder_rename call with missing arguments
    print("\n=== Testing folder_rename with missing arguments ===")
    
    test_cases = [
        # Missing both arguments
        {},
        # Missing new_name
        {"folder_id": "test_id"},
        # Missing folder_id  
        {"new_name": "test_name"},
        # Valid arguments (but fake ID)
        {"folder_id": "fake_id", "new_name": "test_name"}
    ]
    
    for i, args in enumerate(test_cases):
        print(f"\nTest case {i+1}: {args}")
        try:
            async with server.eagle_client as client:
                result = await server.folder_handler.handle_call(
                    "folder_rename", args, client
                )
                print(f"[OK] Result: {result[0].text}")
        except Exception as e:
            print(f"[ERROR] Error: {e}")
            print(f"   Error type: {type(e).__name__}")


if __name__ == "__main__":
    asyncio.run(test_folder_rename())