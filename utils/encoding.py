"""Encoding utilities for handling Japanese text properly."""

import sys
import os
from typing import Any, Dict, List, Union


def safe_str(text: Any, fallback: str = "Unknown") -> str:
    """Safely convert any value to string with proper encoding handling."""
    if text is None:
        return fallback
    
    if isinstance(text, str):
        return text
    
    if isinstance(text, bytes):
        try:
            return text.decode('utf-8')
        except UnicodeDecodeError:
            return text.decode('utf-8', errors='replace')
    
    return str(text)


def ensure_utf8_output():
    """Ensure UTF-8 output on Windows console."""
    if sys.platform == 'win32':
        try:
            # Try to set console output to UTF-8
            os.system('chcp 65001 > nul 2>&1')
        except:
            pass


def format_japanese_safe(text: str, max_length: int = 50) -> str:
    """Format Japanese text safely for console output."""
    if not text:
        return "Unknown"
    
    # Ensure we have a proper string
    text = safe_str(text)
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length-3] + "..."
    
    return text


def clean_response_text(data: Union[Dict, List, str, Any]) -> Union[Dict, List, str, Any]:
    """Recursively clean response data to ensure proper text encoding."""
    if isinstance(data, dict):
        return {key: clean_response_text(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [clean_response_text(item) for item in data]
    elif isinstance(data, str):
        return safe_str(data)
    else:
        return data


def get_display_name(item: Dict[str, Any], fallback: str = "Unnamed Item") -> str:
    """Get a display-safe name from an Eagle API item/folder."""
    name = item.get('name', '')
    if not name:
        return fallback
    
    # Clean and format for display
    clean_name = format_japanese_safe(name)
    return clean_name if clean_name != "Unknown" else fallback


def create_safe_summary(items: List[Dict[str, Any]], item_type: str = "items") -> str:
    """Create a safe summary of items with proper Japanese text handling."""
    if not items:
        return f"No {item_type} found."
    
    summary_parts = [f"Found {len(items)} {item_type}:"]
    
    for i, item in enumerate(items[:10]):  # Show first 10 items
        display_name = get_display_name(item, f"Item {i+1}")
        item_id = item.get('id', 'Unknown ID')
        summary_parts.append(f"{i+1}. {display_name} (ID: {item_id[:8]}...)")
    
    if len(items) > 10:
        summary_parts.append(f"... and {len(items) - 10} more {item_type}")
    
    return "\n".join(summary_parts)


def ascii_safe_text(text: str) -> str:
    """Convert text to ASCII-safe representation for debugging."""
    if not text:
        return "Empty"
    
    try:
        # Try to display as-is first
        return text
    except UnicodeError:
        # Fall back to ASCII representation
        return text.encode('ascii', errors='replace').decode('ascii')


def debug_encoding_info(text: str) -> str:
    """Get detailed encoding information for debugging."""
    if not text:
        return "Empty string"
    
    info_parts = [
        f"Length: {len(text)}",
        f"Type: {type(text).__name__}",
        f"ASCII-safe: {ascii_safe_text(text)}",
        f"UTF-8 bytes: {text.encode('utf-8', errors='replace')[:50]}..."
    ]
    
    return " | ".join(info_parts)