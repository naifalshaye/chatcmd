"""
Encoding tools for ChatCMD
Base64 encoding/decoding and related utilities
"""

import base64
import pyperclip
from chatcmd.core.display import Colors, colored_print, print_tool_header


def base64_encode(text: str) -> str:
    """
    Encode text to base64

    Args:
        text: Text to encode

    Returns:
        Base64 encoded string
    """
    print_tool_header("Base64 ENCODE")

    try:
        result = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        colored_print(f"Encoded: {result}", Colors.BRIGHT_GREEN, bold=True)
        pyperclip.copy(result)
        return result
    except Exception as e:
        colored_print(f"Error: {e}", Colors.RED, bold=True)
        return ""


def base64_decode(text: str) -> str:
    """
    Decode base64 text

    Args:
        text: Base64 text to decode

    Returns:
        Decoded string
    """
    print_tool_header("Base64 DECODE")

    try:
        result = base64.b64decode(text.encode('utf-8')).decode('utf-8')
        colored_print(f"Decoded: {result}", Colors.BRIGHT_GREEN, bold=True)
        pyperclip.copy(result)
        return result
    except Exception as e:
        colored_print(f"Error: {e}", Colors.RED, bold=True)
        return ""
