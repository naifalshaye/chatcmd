"""
Developer tools and utilities for ChatCMD
Additional features useful for software engineers and developers
"""

import base64
import uuid
import re
import datetime
import requests
import pyperclip
from typing import Dict, List, Optional, Any
from urllib.parse import quote


class DeveloperTools:
    """Collection of developer-focused tools and utilities"""
    
    def __init__(self):
        self.qr_api_url = "https://api.qrserver.com/v1/create-qr-code/"
    
    
    def generate_regex_pattern(self, description: str) -> str:
        """
        Generate regex patterns for common use cases
        
        Args:
            description: Description of what the regex should match
            
        Returns:
            Generated regex pattern
        """
        from chatcmd import Colors, colored_print
        
        colored_print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Generate Regex Pattern
        """, Colors.BRIGHT_GREEN)
        
        # Common regex patterns
        patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[\d\s\-\(\)]{10,}$',
            'url': r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$',
            'ip': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            'date': r'^\d{4}-\d{2}-\d{2}$',
            'time': r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',
            'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            'username': r'^[a-zA-Z0-9_]{3,20}$',
            'credit_card': r'^\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}$',
            'zip_code': r'^\d{5}(-\d{4})?$'
        }
        
        description_lower = description.lower()
        
        # Try to match description to known patterns
        for key, pattern in patterns.items():
            if key in description_lower:
                regex = pattern
                break
        else:
            # Generate a basic pattern based on description
            if 'number' in description_lower:
                regex = r'\d+'
            elif 'word' in description_lower:
                regex = r'\w+'
            elif 'letter' in description_lower:
                regex = r'[a-zA-Z]+'
            else:
                regex = r'.*'
        
        colored_print(f"Regex Pattern: {regex}", Colors.BRIGHT_GREEN, bold=True)
        pyperclip.copy(regex)
        return regex
    
    
    def base64_encode_decode(self, text: str, operation: str = 'encode') -> str:
        """
        Encode or decode base64 strings
        
        Args:
            text: Text to encode/decode
            operation: 'encode' or 'decode'
            
        Returns:
            Encoded or decoded string
        """
        colored_print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                        Base64 {operation.upper()}
        """, Colors.BRIGHT_GREEN)
        
        try:
            if operation.lower() == 'encode':
                result = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                colored_print(f"Encoded: {result}", Colors.BRIGHT_GREEN, bold=True)
            else:  # decode
                result = base64.b64decode(text.encode('utf-8')).decode('utf-8')
                colored_print(f"Decoded: {result}", Colors.BRIGHT_GREEN, bold=True)
            
            pyperclip.copy(result)
            return result
        except Exception as e:
            error_msg = f"Error: {e}"
            colored_print(error_msg, Colors.RED, bold=True)
            return error_msg
    
    
    
    def generate_uuid(self, version: int = 4) -> str:
        """
        Generate UUIDs in different formats
        
        Args:
            version: UUID version (1, 3, 4, 5)
            
        Returns:
            Generated UUID
        """
        colored_print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Generate UUID v{version}
        """, Colors.BRIGHT_GREEN)
        
        try:
            if version == 1:
                uuid_value = str(uuid.uuid1())
            elif version == 3:
                uuid_value = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'example.com'))
            elif version == 4:
                uuid_value = str(uuid.uuid4())
            elif version == 5:
                uuid_value = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'example.com'))
            else:
                uuid_value = str(uuid.uuid4())
            
            colored_print(f"UUID v{version}: {uuid_value}", Colors.BRIGHT_GREEN, bold=True)
            pyperclip.copy(uuid_value)
            return uuid_value
        except Exception as e:
            error_msg = f"Error generating UUID: {e}"
            print(error_msg)
            return error_msg
    
    def convert_timestamp(self, timestamp: str, format_type: str = 'unix') -> str:
        """
        Convert between different timestamp formats
        
        Args:
            timestamp: Timestamp to convert
            format_type: Target format (unix, iso, readable)
            
        Returns:
            Converted timestamp
        """
        colored_print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                        Timestamp Converter
        """, Colors.BRIGHT_GREEN)
        
        try:
            # Try to parse as unix timestamp first
            if timestamp.isdigit():
                unix_time = int(timestamp)
                dt = datetime.datetime.fromtimestamp(unix_time)
            else:
                # Try to parse as ISO format
                dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                unix_time = int(dt.timestamp())
            
            if format_type.lower() == 'unix':
                result = str(unix_time)
            elif format_type.lower() == 'iso':
                result = dt.isoformat()
            elif format_type.lower() == 'readable':
                result = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                result = str(unix_time)
            
            colored_print(f"Converted timestamp: {result}", Colors.BRIGHT_GREEN, bold=True)
            pyperclip.copy(result)
            return result
        except Exception as e:
            error_msg = f"Error converting timestamp: {e}"
            print(error_msg)
            return error_msg
    
    def generate_qr_code(self, text: str) -> str:
        """
        Generate QR code for text/URL
        
        Args:
            text: Text or URL to encode in QR code
            
        Returns:
            QR code URL
        """
        colored_print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            QR Code Generator
        """, Colors.BRIGHT_GREEN)
        
        try:
            # URL encode the text
            encoded_text = quote(text)
            qr_url = f"{self.qr_api_url}?size=200x200&data={encoded_text}"
            
            colored_print(f"QR Code URL: {qr_url}", Colors.BRIGHT_GREEN, bold=True)
            colored_print(f"Text: {text}", Colors.CYAN)
            pyperclip.copy(qr_url)
            return qr_url
        except Exception as e:
            error_msg = f"Error generating QR code: {e}"
            print(error_msg)
            return error_msg
    
    


# Create instance
developer_tools = DeveloperTools()