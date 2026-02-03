"""
Generator tools for ChatCMD
UUID, password, regex, user-agent, and timestamp generators
"""

import uuid
import random
import string
import secrets
import datetime
import pyperclip
from fake_useragent import UserAgent
from chatcmd.core.display import Colors, colored_print, print_tool_header


def generate_uuid(version: int = 4) -> str:
    """
    Generate UUID in specified version

    Args:
        version: UUID version (1, 3, 4, 5)

    Returns:
        Generated UUID string
    """
    print_tool_header(f"Generate UUID v{version}")

    try:
        if version == 1:
            # Security warning: UUID v1 contains MAC address
            colored_print("Warning: UUID v1 uses MAC address. Using randomized node for privacy.", Colors.YELLOW)
            random_node = random.getrandbits(48) | 0x010000000000
            uuid_value = str(uuid.uuid1(node=random_node))
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
        colored_print(f"Error: {e}", Colors.RED, bold=True)
        return ""


def generate_password(length: int = 18) -> str:
    """
    Generate a random secure password

    Args:
        length: Password length (default 18, max 1000)

    Returns:
        Generated password
    """
    # Validate length
    length = max(1, min(length, 1000))

    password = ''.join(
        secrets.choice(string.ascii_letters + string.digits + string.punctuation)
        for _ in range(length)
    )

    colored_print(password, Colors.BRIGHT_GREEN, bold=True)
    pyperclip.copy(password)
    return password


def generate_regex_pattern(description: str) -> str:
    """
    Generate regex pattern for common use cases

    Args:
        description: Description of what the regex should match

    Returns:
        Generated regex pattern
    """
    print_tool_header("Generate Regex Pattern")

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
    regex = None
    for key, pattern in patterns.items():
        if key in description_lower:
            regex = pattern
            break

    if not regex:
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


def generate_user_agent(os_type: str = None, browser: str = None) -> str:
    """
    Generate a random user-agent string

    Args:
        os_type: Operating system (linux, windows, macos)
        browser: Browser type (firefox, chrome, safari, etc.)

    Returns:
        User-agent string
    """
    ua = UserAgent()

    if os_type == "linux":
        if browser == "firefox":
            user_agent = ua.firefox
        elif browser == "chrome":
            user_agent = ua.chrome
        elif browser == "opera":
            user_agent = ua.opera
        else:
            user_agent = ua.random
    elif os_type == "windows":
        if browser == "firefox":
            user_agent = ua.firefox
        elif browser == "chrome":
            user_agent = ua.chrome
        elif browser == "edge":
            user_agent = ua.edge
        else:
            user_agent = ua.random
    elif os_type == "macos":
        if browser == "safari":
            user_agent = ua.safari
        elif browser == "chrome":
            user_agent = ua.chrome
        elif browser == "firefox":
            user_agent = ua.firefox
        else:
            user_agent = ua.random
    else:
        user_agent = ua.random

    colored_print(user_agent, Colors.BRIGHT_GREEN, bold=True)
    pyperclip.copy(user_agent)
    return user_agent


def convert_timestamp(timestamp: str, format_type: str = 'unix') -> str:
    """
    Convert between different timestamp formats

    Args:
        timestamp: Timestamp to convert
        format_type: Target format (unix, iso, readable)

    Returns:
        Converted timestamp
    """
    print_tool_header("Timestamp Converter")

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
        colored_print(f"Error: {e}", Colors.RED, bold=True)
        return ""
