#!/usr/bin/env python3
"""
Debug script to test Eagle API responses for item MD9R46KJ58OKN
and understand file extension handling issues.
"""

import asyncio
import json
import httpx
from pathlib import Path


async def debug_item_extension():
    """Debug Eagle API responses for item extension handling."""
    
    item_id = "MD9R46KJ58OKN"
    base_url = "http://localhost:41595"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=" * 60)
        print(f"DEBUGGING ITEM: {item_id}")
        print("=" * 60)
        
        # Test 1: Get item info
        print("\n1. TESTING /api/item/info")
        print("-" * 40)
        
        try:
            info_response = await client.get(f"{base_url}/api/item/info", params={"id": item_id})
            info_response.raise_for_status()
            info_data = info_response.json()
            
            print(f"Status Code: {info_response.status_code}")
            print(f"Raw Response: {json.dumps(info_data, indent=2, ensure_ascii=False)}")
            
            # Extract key fields
            if "data" in info_data:
                item_data = info_data["data"]
                print(f"\nKey Fields:")
                print(f"  name: {item_data.get('name', 'N/A')}")
                print(f"  ext: {item_data.get('ext', 'N/A')}")
                print(f"  path: {item_data.get('path', 'N/A')}")
                print(f"  size: {item_data.get('size', 'N/A')}")
                print(f"  mtime: {item_data.get('mtime', 'N/A')}")
                
                # Analyze path and extension
                if item_data.get('path'):
                    file_path = Path(item_data['path'])
                    print(f"\nPath Analysis:")
                    print(f"  Full path: {file_path}")
                    print(f"  File name: {file_path.name}")
                    print(f"  Suffix: {file_path.suffix}")
                    print(f"  Stem: {file_path.stem}")
                
        except Exception as e:
            print(f"ERROR in item info: {e}")
        
        # Test 2: Get thumbnail info
        print("\n\n2. TESTING /api/item/thumbnail")
        print("-" * 40)
        
        try:
            thumbnail_response = await client.get(f"{base_url}/api/item/thumbnail", params={"id": item_id})
            thumbnail_response.raise_for_status()
            
            print(f"Status Code: {thumbnail_response.status_code}")
            print(f"Content Type: {thumbnail_response.headers.get('content-type', 'N/A')}")
            print(f"Content Length: {thumbnail_response.headers.get('content-length', 'N/A')}")
            
            # Check if it's JSON error or binary data
            content_type = thumbnail_response.headers.get('content-type', '')
            if 'application/json' in content_type:
                thumbnail_data = thumbnail_response.json()
                print(f"JSON Response: {json.dumps(thumbnail_data, indent=2, ensure_ascii=False)}")
            else:
                print(f"Binary content received (thumbnail image)")
                print(f"First 20 bytes: {thumbnail_response.content[:20]}")
                
                # Check image format by magic bytes
                content = thumbnail_response.content
                if content.startswith(b'\xff\xd8\xff'):
                    print("Image format detected: JPEG")
                elif content.startswith(b'\x89PNG\r\n\x1a\n'):
                    print("Image format detected: PNG")
                elif content.startswith(b'GIF8'):
                    print("Image format detected: GIF")
                elif content.startswith(b'\x00\x00\x01\x00'):
                    print("Image format detected: ICO")
                else:
                    print("Image format: Unknown")
                
        except Exception as e:
            print(f"ERROR in thumbnail: {e}")
        
        # Test 3: Current ImageHandler logic simulation
        print("\n\n3. CURRENT IMAGEHANDLER LOGIC SIMULATION")
        print("-" * 40)
        
        try:
            # Simulate current logic from handlers/image.py
            info_response = await client.get(f"{base_url}/api/item/info", params={"id": item_id})
            if info_response.status_code == 200:
                info_data = info_response.json()
                if "data" in info_data:
                    item_data = info_data["data"]
                    item_name = item_data.get("name", "")
                    
                    print(f"Item name from API: '{item_name}'")
                    
                    # Current logic: check if name ends with common extensions
                    if item_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
                        # Extract extension from name
                        name_ext = Path(item_name).suffix.lower()
                        print(f"Extension from name: '{name_ext}'")
                        
                        # Current problematic path construction
                        current_path = f"/tmp/eagle_thumbnail_{item_id}.png"  # Always PNG!
                        print(f"Current path (WRONG): {current_path}")
                        
                        # Corrected path construction
                        correct_path = f"/tmp/eagle_thumbnail_{item_id}{name_ext}"
                        print(f"Correct path (FIXED): {correct_path}")
                        
                        print(f"\nPROBLEM IDENTIFIED:")
                        print(f"  Current code always uses .png extension")
                        print(f"  Should use actual extension: {name_ext}")
                    else:
                        print("Item is not an image file")
                
        except Exception as e:
            print(f"ERROR in logic simulation: {e}")
        
        # Test 4: Alternative approaches
        print("\n\n4. ALTERNATIVE EXTENSION DETECTION")
        print("-" * 40)
        
        try:
            # Method 1: From item path
            info_response = await client.get(f"{base_url}/api/item/info", params={"id": item_id})
            if info_response.status_code == 200:
                info_data = info_response.json()
                if "data" in info_data:
                    item_data = info_data["data"]
                    
                    # Try different fields for extension
                    name_ext = Path(item_data.get("name", "")).suffix.lower()
                    path_ext = Path(item_data.get("path", "")).suffix.lower() if item_data.get("path") else ""
                    api_ext = item_data.get("ext", "").lower()
                    
                    print(f"Extension from 'name': '{name_ext}'")
                    print(f"Extension from 'path': '{path_ext}'")
                    print(f"Extension from 'ext' field: '{api_ext}'")
                    
                    # Determine best extension
                    best_ext = name_ext or path_ext or api_ext or ".png"
                    print(f"Best extension to use: '{best_ext}'")
        
        except Exception as e:
            print(f"ERROR in alternative detection: {e}")


if __name__ == "__main__":
    asyncio.run(debug_item_extension())