"""
Tools module for ChatCMD
Consolidates all developer tools and utilities
"""

from .encoding import base64_encode, base64_decode
from .generators import (
    generate_uuid,
    generate_password,
    generate_regex_pattern,
    generate_user_agent,
    convert_timestamp
)
from .network import get_public_ip
from .lookup import lookup_http_code, HTTP_CODES

__all__ = [
    # Encoding
    'base64_encode',
    'base64_decode',
    # Generators
    'generate_uuid',
    'generate_password',
    'generate_regex_pattern',
    'generate_user_agent',
    'convert_timestamp',
    # Network
    'get_public_ip',
    # Lookup
    'lookup_http_code',
    'HTTP_CODES',
]
