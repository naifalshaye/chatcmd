"""
Display utilities for ChatCMD
Centralized colors, headers, and formatted output
"""

import sys
import os


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    BRIGHT_GREEN = '\033[1;92m'
    YELLOW = '\033[93m'
    GOLD = '\033[38;5;220m'
    BRIGHT_YELLOW = '\033[1;93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    RESET = '\033[0m'


# Main ASCII header
CHATCMD_HEADER = """
            ######  ##     ##    ###    ########  ######  ##     ## ########
           ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
           ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
           ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
           ##       ##     ## #########    ##    ##       ##     ## ##     ##
           ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
            ######  ##     ## ##     ##    ##     ######  ##     ## ########
        ------------------------------------------------------------------------
Open Source AI-driven CLI command lookup, SQL Generator and other tools using multiple AI models
                  Boost Your Productivity, Say Goodbye to Manual Searches
        ------------------------------------------------------------------------
"""

# Tool-specific header (shorter version for individual tools)
TOOL_HEADER = """
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
"""


def _should_use_color() -> bool:
    """Check if colored output should be used"""
    if os.environ.get('CHATCMD_QUIET') == '1':
        return False
    if os.environ.get('CHATCMD_NO_COLOR') == '1':
        return False
    if os.environ.get('CHATCMD_JSON') == '1':
        return False
    if not sys.stdout.isatty():
        return False
    return True


def colored_print(text, color=Colors.GREEN, bold=False, end="\n"):
    """Print colored text to terminal"""
    if os.environ.get('CHATCMD_QUIET') == '1':
        return

    if not _should_use_color():
        print(text, end=end)
        return

    prefix = Colors.BOLD if bold else ""
    print(f"{prefix}{color}{text}{Colors.END}", end=end)


def print_header():
    """Print the main ChatCMD header"""
    if os.environ.get('CHATCMD_QUIET') == '1':
        return
    colored_print(CHATCMD_HEADER, Colors.WHITE)


def print_tool_header(tool_name: str):
    """Print header for a specific tool"""
    if os.environ.get('CHATCMD_QUIET') == '1':
        return
    colored_print(TOOL_HEADER, Colors.BRIGHT_GREEN)
    colored_print(f"                            {tool_name}", Colors.BRIGHT_GREEN)
    print()


def print_success(message: str):
    """Print success message"""
    colored_print(message, Colors.GREEN, bold=True)


def print_error(message: str):
    """Print error message"""
    colored_print(message, Colors.RED, bold=True)


def print_warning(message: str):
    """Print warning message"""
    colored_print(message, Colors.YELLOW)


def print_info(message: str):
    """Print info message"""
    colored_print(message, Colors.CYAN)
