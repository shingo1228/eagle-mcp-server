# Eagle API Extension Handling Debug Report

## Issue Summary
JPEG files are being saved with `.png` extensions when using the Eagle MCP Server's image thumbnail functionality, causing format confusion for users.

## Test Item Details
- **Item ID**: MD9R46KJ58OKN
- **Original Format**: JPEG (Eagle API `ext` field: "jpg")
- **File Size**: 158,913 bytes
- **Dimensions**: 704x1408 pixels

## Root Cause Analysis

### 1. Eagle API Behavior
- Eagle stores original images in their native format (JPEG in this case)
- Eagle **always** generates PNG thumbnails regardless of original format
- The `/api/item/thumbnail` endpoint returns PNG files even for JPEG originals
- The `ext` field in `/api/item/info` reflects the original file format, not the thumbnail format

### 2. Current ImageHandler Logic Problem
```python
# Current problematic code in handlers/image.py
thumbnail_path = f"/tmp/eagle_thumbnail_{item_id}.png"  # Always PNG!
```

The code assumes all thumbnails are PNG, which is technically correct for Eagle's thumbnail system, but confusing for users who expect the original format.

### 3. API Response Analysis

#### Item Info Response
```json
{
  "status": "success",
  "data": {
    "id": "MD9R46KJ58OKN",
    "name": "画像",  // Note: garbled in Windows console
    "ext": "jpg",    // Original format
    "size": 158913,
    "width": 704,
    "height": 1408
    // ... other fields
  }
}
```

#### Thumbnail Path Response
```json
{
  "status": "success",
  "data": "E:/00EagleLibrary/.../画像_thumbnail.png"  // Always PNG
}
```

### 4. File System Reality
- Original file: `画像.jpg` (JPEG format)
- Thumbnail file: `画像_thumbnail.png` (PNG format)
- Eagle automatically converts thumbnails to PNG during generation

## Problem Scenarios

### Scenario 1: Current Behavior (Incorrect)
```
Original: image.jpg (JPEG)
Thumbnail: Always saved as eagle_thumbnail_ID.png
Result: User confusion - expects .jpg but gets .png
```

### Scenario 2: Using Original Extension (Also Incorrect)
```
Original: image.jpg (JPEG)
Thumbnail: Saved as eagle_thumbnail_ID.jpg
Result: PNG content with JPG extension = corrupted file
```

## Recommended Solution

### Option A: Use Actual Thumbnail Format (Recommended)
Detect the actual thumbnail format and use the appropriate extension:

```python
async def get_thumbnail_with_correct_extension(item_id: str):
    # Download thumbnail content
    response = await eagle_client.get(f"/api/item/thumbnail", params={"id": item_id})
    content = await response.aread()
    
    # Detect format from magic bytes
    if content.startswith(b'\xff\xd8\xff'):
        ext = '.jpg'
        format_name = 'JPEG'
    elif content.startswith(b'\x89PNG\r\n\x1a\n'):
        ext = '.png'
        format_name = 'PNG'
    elif content.startswith(b'GIF8'):
        ext = '.gif'
        format_name = 'GIF'
    else:
        ext = '.png'  # fallback
        format_name = 'PNG'
    
    thumbnail_path = f"/tmp/eagle_thumbnail_{item_id}{ext}"
    return thumbnail_path, content, format_name
```

### Option B: Always Use PNG with Clear Naming
Accept that Eagle thumbnails are always PNG and make this clear:

```python
thumbnail_path = f"/tmp/eagle_thumbnail_{item_id}.png"  # Always PNG (Eagle converts)
```

Add documentation explaining that thumbnails are always PNG regardless of original format.

## Implementation Impact

### Files to Modify
- `handlers/image.py` - Update thumbnail saving logic
- Documentation - Explain thumbnail format behavior

### Testing Required
1. Test with JPEG originals → PNG thumbnails
2. Test with PNG originals → PNG thumbnails
3. Test with GIF originals → PNG thumbnails
4. Verify file format detection accuracy

## Debug Scripts Created

1. **`debug_item_extension.py`** - Basic API response analysis
2. **`debug_thumbnail_path.py`** - Path and file system analysis
3. **`debug_final_analysis.py`** - Complete solution testing
4. **`debug_summary.py`** - Clean summary generation

## Conclusion

The issue is not a bug but a design choice by Eagle to standardize thumbnails as PNG. The MCP server should either:

1. **Detect actual thumbnail format** (Option A) - Most accurate
2. **Document PNG-only behavior** (Option B) - Simpler but less intuitive

**Recommendation**: Implement Option A for accuracy and user expectation alignment.