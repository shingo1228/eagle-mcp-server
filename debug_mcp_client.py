"""Debug MCP Client communication to simulate LM Studio/Claude Desktop behavior."""

import asyncio
import json
from main import EagleMCPServer


async def simulate_mcp_client():
    """Simulate MCP client behavior like LM Studio/Claude Desktop."""
    print("=== Simulating MCP Client Communication ===")
    
    server = EagleMCPServer()
    
    # Step 1: List tools (what LM Studio/Claude Desktop sees)
    print("\n1. Listing available tools...")
    
    # Simulate MCP list_tools call
    tools = []
    tools.extend(server.folder_handler.get_tools())
    tools.extend(server.item_handler.get_tools())
    tools.extend(server.library_handler.get_tools())
    tools.extend(server.image_handler.get_tools())
    
    # Find folder_rename tool
    folder_rename_tool = next((t for t in tools if t.name == "folder_rename"), None)
    
    if folder_rename_tool:
        print(f"[OK] folder_rename tool found")
        print(f"     Description: {folder_rename_tool.description}")
        print(f"     Required params: {folder_rename_tool.inputSchema['required']}")
    else:
        print("[ERROR] folder_rename tool not found!")
        return
    
    # Step 2: Simulate various MCP call_tool requests
    print("\n2. Simulating MCP call_tool requests...")
    
    test_calls = [
        # Case 1: Typical user error - missing required parameter
        {
            "name": "folder_rename",
            "description": "User forgets new_name parameter",
            "arguments": {"folder_id": "MDB6PLM7BVHEG"}
        },
        # Case 2: Another typical error - missing folder_id
        {
            "name": "folder_rename", 
            "description": "User forgets folder_id parameter",
            "arguments": {"new_name": "Test-Renamed"}
        },
        # Case 3: Valid call (but fake ID)
        {
            "name": "folder_rename",
            "description": "Valid parameters but fake ID",
            "arguments": {"folder_id": "FAKE_ID", "new_name": "Test-Renamed"}
        },
        # Case 4: Valid call with real ID from folder list
        {
            "name": "folder_rename",
            "description": "Valid call with real folder ID",
            "arguments": {"folder_id": "MDB6PLM7BVHEG", "new_name": "AI-Test-Folder-Renamed-v3"}
        }
    ]
    
    for i, call in enumerate(test_calls, 1):
        print(f"\nTest {i}: {call['description']}")
        print(f"  Call: {call['name']}({call['arguments']})")
        
        try:
            # Simulate exact MCP call_tool behavior
            async with server.eagle_client as client:
                if call['name'].startswith("folder_"):
                    result = await server.folder_handler.handle_call(
                        call['name'], call['arguments'], client
                    )
                else:
                    result = [{"type": "text", "text": "Unknown tool category"}]
                
                print(f"  Result: {result[0].text}")
                
        except Exception as e:
            print(f"  Exception: {type(e).__name__}: {e}")
            print(f"  This might be what LM Studio/Claude Desktop is seeing!")
    
    print("\n=== Test completed ===")


if __name__ == "__main__":
    asyncio.run(simulate_mcp_client())