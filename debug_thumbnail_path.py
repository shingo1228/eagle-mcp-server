#!/usr/bin/env python3
"""
Enhanced debug script to test Eagle thumbnail path handling
and file extension issues.
"""

import asyncio
import json
import httpx
from pathlib import Path
import os


async def debug_thumbnail_path():
    """Debug Eagle thumbnail path and extension handling."""
    
    item_id = "MD9R46KJ58OKN"
    base_url = "http://localhost:41595"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=" * 60)
        print(f"DEBUGGING THUMBNAIL PATH FOR ITEM: {item_id}")
        print("=" * 60)
        
        # Get item info first
        try:
            info_response = await client.get(f"{base_url}/api/item/info", params={"id": item_id})
            info_response.raise_for_status()
            info_data = info_response.json()
            
            if "data" in info_data:
                item_data = info_data["data"]
                print(f"Item Info:")
                print(f"  ID: {item_data.get('id')}")
                print(f"  Name: {repr(item_data.get('name'))}")  # Use repr to show actual characters
                print(f"  Extension (ext field): {item_data.get('ext')}")
                print(f"  Size: {item_data.get('size')} bytes")
                print(f"  Dimensions: {item_data.get('width')}x{item_data.get('height')}")
                
        except Exception as e:
            print(f"ERROR getting item info: {e}")
            return
        
        # Get thumbnail path
        print(f"\n{'='*40}")
        print("THUMBNAIL PATH ANALYSIS")
        print(f"{'='*40}")
        
        try:
            thumbnail_response = await client.get(f"{base_url}/api/item/thumbnail", params={"id": item_id})
            thumbnail_response.raise_for_status()
            thumbnail_data = thumbnail_response.json()
            
            if thumbnail_data.get("status") == "success":
                thumbnail_path = thumbnail_data["data"]
                print(f"Thumbnail path from API: {thumbnail_path}")
                
                # Analyze the path
                path_obj = Path(thumbnail_path)
                print(f"\nPath Analysis:")
                print(f"  Full path: {path_obj}")
                print(f"  Parent directory: {path_obj.parent}")
                print(f"  Filename: {path_obj.name}")
                print(f"  Stem: {path_obj.stem}")
                print(f"  Suffix: {path_obj.suffix}")
                print(f"  Exists: {path_obj.exists()}")
                
                # Check if file exists and get its properties
                if path_obj.exists():
                    stat = path_obj.stat()
                    print(f"  File size: {stat.st_size} bytes")
                    print(f"  Modified: {stat.st_mtime}")
                    
                    # Check actual file format by reading magic bytes
                    with open(path_obj, 'rb') as f:
                        magic_bytes = f.read(20)
                        print(f"  Magic bytes: {magic_bytes}")
                        
                        if magic_bytes.startswith(b'\xff\xd8\xff'):
                            actual_format = "JPEG"
                        elif magic_bytes.startswith(b'\x89PNG\r\n\x1a\n'):
                            actual_format = "PNG"
                        elif magic_bytes.startswith(b'GIF8'):
                            actual_format = "GIF"
                        else:
                            actual_format = "Unknown"
                        
                        print(f"  Actual format: {actual_format}")
                        print(f"  Extension mismatch: {actual_format.lower() != path_obj.suffix[1:]}")
                
                # Check directory structure
                print(f"\nDirectory Structure:")
                if path_obj.parent.exists():
                    for item in path_obj.parent.iterdir():
                        print(f"  {item.name} ({'file' if item.is_file() else 'dir'})")
                
                # Test different extension scenarios
                print(f"\n{'='*40}")
                print("EXTENSION HANDLING SCENARIOS")
                print(f"{'='*40}")
                
                # Scenario 1: Use API ext field
                api_ext = item_data.get('ext', '')
                if api_ext:
                    corrected_path_1 = f"/tmp/eagle_thumbnail_{item_id}.{api_ext}"
                    print(f"Scenario 1 - Use API ext field:")
                    print(f"  Extension: {api_ext}")
                    print(f"  Path: {corrected_path_1}")
                
                # Scenario 2: Use actual thumbnail extension
                if path_obj.suffix:
                    corrected_path_2 = f"/tmp/eagle_thumbnail_{item_id}{path_obj.suffix}"
                    print(f"Scenario 2 - Use thumbnail extension:")
                    print(f"  Extension: {path_obj.suffix}")
                    print(f"  Path: {corrected_path_2}")
                
                # Scenario 3: Detect from content
                if path_obj.exists():
                    with open(path_obj, 'rb') as f:
                        magic_bytes = f.read(10)
                        if magic_bytes.startswith(b'\xff\xd8\xff'):
                            content_ext = ".jpg"
                        elif magic_bytes.startswith(b'\x89PNG'):
                            content_ext = ".png"
                        elif magic_bytes.startswith(b'GIF8'):
                            content_ext = ".gif"
                        else:
                            content_ext = ".png"  # fallback
                    
                    corrected_path_3 = f"/tmp/eagle_thumbnail_{item_id}{content_ext}"
                    print(f"Scenario 3 - Detect from content:")
                    print(f"  Extension: {content_ext}")
                    print(f"  Path: {corrected_path_3}")
                
                # Current problematic approach
                print(f"\nCurrent (WRONG) approach:")
                current_wrong_path = f"/tmp/eagle_thumbnail_{item_id}.png"
                print(f"  Always PNG: {current_wrong_path}")
                
                # Recommended fix
                print(f"\nRECOMMENDED FIX:")
                recommended_ext = api_ext if api_ext else (path_obj.suffix if path_obj.suffix else ".png")
                recommended_path = f"/tmp/eagle_thumbnail_{item_id}.{recommended_ext.lstrip('.')}"
                print(f"  Use API ext field as primary source: {recommended_ext}")
                print(f"  Final path: {recommended_path}")
                
        except Exception as e:
            print(f"ERROR getting thumbnail: {e}")


if __name__ == "__main__":
    asyncio.run(debug_thumbnail_path())