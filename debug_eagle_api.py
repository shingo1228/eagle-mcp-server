"""Debug Eagle API folder update parameters."""

import asyncio
import json
from eagle_client import EagleClient


async def test_eagle_api_params():
    """Test different parameter combinations for Eagle API."""
    print("=== Testing Eagle API Folder Update Parameters ===")
    
    async with EagleClient() as client:
        # First, get a real folder to test with
        folders_result = await client.get("/api/folder/list")
        if folders_result.get("status") == "success":
            folders = folders_result.get("data", [])
            test_folder = next((f for f in folders if f.get("name") == "AI-Test-Folder"), None)
            
            if not test_folder:
                print("No test folder found, using first available folder")
                test_folder = folders[0] if folders else None
            
            if test_folder:
                folder_id = test_folder.get("id")
                folder_name = test_folder.get("name")
                print(f"Testing with folder: {folder_name} (ID: {folder_id})")
                
                # Test different parameter combinations
                test_params = [
                    # Current implementation
                    {"folderId": folder_id, "newName": "Test-Name-1"},
                    # Alternative forms from documentation
                    {"id": folder_id, "folderName": "Test-Name-2"},
                    {"id": folder_id, "newName": "Test-Name-3"},
                    {"folderId": folder_id, "folderName": "Test-Name-4"},
                    # Try with all possible combinations
                    {"id": folder_id, "name": "Test-Name-5"},
                    {"folderId": folder_id, "name": "Test-Name-6"},
                ]
                
                for i, params in enumerate(test_params, 1):
                    print(f"\nTest {i}: {params}")
                    try:
                        result = await client.post("/api/folder/update", params)
                        print(f"  SUCCESS: {result}")
                        # If successful, rename back
                        if result.get("status") == "success":
                            await client.post("/api/folder/update", {
                                list(params.keys())[0]: folder_id,
                                list(params.keys())[1]: folder_name
                            })
                        break  # Stop on first success
                    except Exception as e:
                        print(f"  FAILED: {e}")
            else:
                print("No folders available for testing")
        else:
            print("Failed to get folder list")


if __name__ == "__main__":
    asyncio.run(test_eagle_api_params())