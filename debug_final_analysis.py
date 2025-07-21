#!/usr/bin/env python3
"""
Final analysis of the Eagle API extension issue and proposed solution.
"""

import asyncio
import json
import httpx
from pathlib import Path
import urllib.parse


async def final_analysis():
    """Complete analysis of the extension handling issue."""
    
    item_id = "MD9R46KJ58OKN"
    base_url = "http://localhost:41595"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("=" * 80)
        print("FINAL ANALYSIS: Eagle API Extension Handling Issue")
        print("=" * 80)
        
        # Get item info
        info_response = await client.get(f"{base_url}/api/item/info", params={"id": item_id})
        info_data = info_response.json()
        item_data = info_data["data"]
        
        # Get thumbnail path
        thumbnail_response = await client.get(f"{base_url}/api/item/thumbnail", params={"id": item_id})
        thumbnail_data = thumbnail_response.json()
        thumbnail_path_encoded = thumbnail_data["data"]
        
        print(f"ISSUE IDENTIFICATION:")
        print(f"-" * 40)
        print(f"1. Item has extension: {item_data.get('ext')} (from API)")
        print(f"2. Item name is garbled: {repr(item_data.get('name'))}")
        print(f"3. Thumbnail path from API: {thumbnail_path_encoded}")
        
        # Decode the URL-encoded filename
        decoded_path = urllib.parse.unquote(thumbnail_path_encoded)
        print(f"4. Decoded thumbnail path: {decoded_path}")
        
        # Check actual thumbnail file
        actual_thumbnail_path = Path("E:/00EagleLibrary/SD-outputs_nsfw.library/images/MD9R46KJ58OKN.info/画像_thumbnail.png")
        print(f"5. Corrected path exists: {actual_thumbnail_path.exists()}")
        
        if actual_thumbnail_path.exists():
            # Check the actual thumbnail file format
            with open(actual_thumbnail_path, 'rb') as f:
                magic_bytes = f.read(10)
                if magic_bytes.startswith(b'\xff\xd8\xff'):
                    actual_format = "JPEG"
                elif magic_bytes.startswith(b'\x89PNG'):
                    actual_format = "PNG"
                else:
                    actual_format = "Unknown"
            
            print(f"6. Actual thumbnail format: {actual_format}")
            print(f"7. Thumbnail extension: {actual_thumbnail_path.suffix}")
        
        print(f"\nPROBLEM SUMMARY:")
        print(f"-" * 40)
        print(f"• Original image is JPEG (ext: {item_data.get('ext')})")
        print(f"• Eagle creates PNG thumbnails (always .png)")
        print(f"• Current ImageHandler code always saves as .png")
        print(f"• BUT user expects original format (.jpg)")
        print(f"• This causes format mismatch in saved thumbnails")
        
        print(f"\nSOLUTION OPTIONS:")
        print(f"-" * 40)
        print(f"Option 1: Use original format (ext field)")
        print(f"  - Save as: /tmp/eagle_thumbnail_{item_id}.jpg")
        print(f"  - Problem: File content is PNG, extension is JPG")
        print(f"  - Result: Corrupted file")
        
        print(f"\nOption 2: Always use .png (current behavior)")
        print(f"  - Save as: /tmp/eagle_thumbnail_{item_id}.png")
        print(f"  - Problem: Extension doesn't match original")
        print(f"  - Result: User confusion")
        
        print(f"\nOption 3: Detect actual thumbnail format")
        print(f"  - Check magic bytes of thumbnail")
        print(f"  - Save with correct extension")
        print(f"  - Result: Accurate file format")
        
        print(f"\nRECOMMENDED SOLUTION:")
        print(f"-" * 40)
        print(f"Use Option 3: Detect actual thumbnail format")
        print(f"1. Download thumbnail from Eagle")
        print(f"2. Check magic bytes to determine format")
        print(f"3. Use appropriate extension (.png, .jpg, .gif)")
        print(f"4. Save with correct extension")
        
        # Test the actual download and format detection
        print(f"\nTESTING RECOMMENDED SOLUTION:")
        print(f"-" * 40)
        
        try:
            # Download thumbnail as binary
            thumbnail_binary_response = await client.get(f"{base_url}/api/item/thumbnail", 
                                                       params={"id": item_id},
                                                       headers={"Accept": "image/*"})
            
            print(f"Download status: {thumbnail_binary_response.status_code}")
            print(f"Content-Type: {thumbnail_binary_response.headers.get('content-type')}")
            
            if thumbnail_binary_response.status_code == 200:
                content = thumbnail_binary_response.content
                print(f"Content length: {len(content)} bytes")
                
                # Detect format from magic bytes
                if content.startswith(b'\xff\xd8\xff'):
                    detected_format = "jpeg"
                    detected_ext = ".jpg"
                elif content.startswith(b'\x89PNG\r\n\x1a\n'):
                    detected_format = "png"
                    detected_ext = ".png"
                elif content.startswith(b'GIF8'):
                    detected_format = "gif"
                    detected_ext = ".gif"
                else:
                    detected_format = "unknown"
                    detected_ext = ".bin"
                
                print(f"Detected format: {detected_format}")
                print(f"Correct extension: {detected_ext}")
                print(f"Recommended filename: eagle_thumbnail_{item_id}{detected_ext}")
                
                # Show the fix for ImageHandler
                print(f"\nCODE FIX FOR handlers/image.py:")
                print(f"-" * 40)
                print(f"# Instead of:")
                print(f'# thumbnail_path = f"/tmp/eagle_thumbnail_{{item_id}}.png"')
                print(f"")
                print(f"# Use:")
                print(f"thumbnail_content = await response.aread()")
                print(f"if thumbnail_content.startswith(b'\\xff\\xd8\\xff'):")
                print(f"    ext = '.jpg'")
                print(f"elif thumbnail_content.startswith(b'\\x89PNG'):")
                print(f"    ext = '.png'")
                print(f"elif thumbnail_content.startswith(b'GIF8'):")
                print(f"    ext = '.gif'")
                print(f"else:")
                print(f"    ext = '.png'  # fallback")
                print(f'thumbnail_path = f"/tmp/eagle_thumbnail_{{item_id}}{{ext}}"')
            
        except Exception as e:
            print(f"Error testing solution: {e}")


if __name__ == "__main__":
    asyncio.run(final_analysis())