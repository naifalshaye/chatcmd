import re
import inspect
import subprocess
import requests
import importlib.metadata
import platform
import os
import time
try:
    import pyperclip
except Exception:
    pyperclip = None


class Helpers:

    @staticmethod
    def _compare_versions(version1, version2):
        """Compare two version strings. Returns 1 if v1 > v2, -1 if v1 < v2, 0 if equal."""
        def normalize(v):
            return [int(x) for x in v.split('.')]
        
        v1_parts = normalize(version1)
        v2_parts = normalize(version2)
        
        # Pad shorter version with zeros
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        for i in range(max_len):
            if v1_parts[i] > v2_parts[i]:
                return 1
            elif v1_parts[i] < v2_parts[i]:
                return -1
        return 0

    @staticmethod
    def get_latest_version_from_pypi():
        try:
            # Add timeout to prevent hanging
            response = requests.get(f"https://pypi.org/pypi/chatcmd/json", timeout=3)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
            latest_version = data["info"]["version"]
            installed_version = importlib.metadata.version('chatcmd')

            # Only notify if PyPI has a newer version than installed
            comparison = Helpers._compare_versions(latest_version, installed_version)
            if comparison > 0:  # latest > installed
                print(f"New version {latest_version} is available! You are currently using version {installed_version}.")
                print("Consider upgrading using: pip3 install --upgrade chatcmd")
            # If installed >= latest, don't show any message
        except (requests.RequestException, KeyError, ValueError) as e:
            # Silently fail version check to avoid disrupting user workflow
            pass

    @staticmethod
    def library_info():
        from chatcmd import Colors, colored_print
        try:
            current_version = importlib.metadata.version('chatcmd')
        except Exception:
            current_version = "unknown"
        
        colored_print("----------------------------------------------------------------", Colors.GOLD)
        colored_print("  Library Name: ChatCMD", Colors.BRIGHT_GREEN, bold=True)
        colored_print("  Library Source [PyPi]: https://pypi.org/naifalshaye/chatcmd", Colors.BLUE)
        colored_print("  Library Source [Github]: https://github.com/naifalshaye/chatcmd", Colors.BLUE)
        colored_print("  Documentation: https://github.com/naifalshaye/chatcmd#readme", Colors.BLUE)
        colored_print("  Bug Tracker: https://github.com/naifalshaye/chatcmd/issues", Colors.BLUE)
        colored_print(f"  Current Version: {current_version}", Colors.BRIGHT_YELLOW)
        colored_print("  Published Date: 2023-05-15", Colors.YELLOW)
        colored_print("  License: MIT", Colors.GREEN)
        colored_print("  Author: Naif Alshaye", Colors.WHITE)
        colored_print("  Author Email: naif@naif.io", Colors.WHITE)
        colored_print("  Author Website: https://naif.io", Colors.WHITE)
        colored_print("----------------------------------------------------------------", Colors.GOLD)

    @staticmethod
    def print_error(message: str, remediation: str = None):
        """Print a standardized error with optional remediation step."""
        from chatcmd import Colors, colored_print
        if os.environ.get('CHATCMD_JSON') == '1':
            import json
            out = {"type": "error", "message": message}
            if remediation:
                out["action"] = remediation
            print(json.dumps(out))
            return
        colored_print(f"Error: {message}", Colors.RED, bold=True)
        if remediation:
            colored_print(f"Action: {remediation}", Colors.YELLOW)

    @staticmethod
    def json_mode() -> bool:
        return os.environ.get('CHATCMD_JSON') == '1'

    @staticmethod
    def copy_to_clipboard(text):
        try:
            system = platform.system()
            # Prefer pyperclip if available
            if pyperclip is not None:
                try:
                    pyperclip.copy(text)
                    return
                except Exception:
                    # Fall through to OS-specific helpers
                    ...
            # Native fallbacks per OS
            if system == "Darwin":
                try:
                    subprocess.run(['pbcopy'], input=text, encoding='utf-8', check=True)
                    return
                except Exception:
                    print("Tip: On macOS, ensure 'pbcopy' is available (Xcode command line tools).")
            elif system == "Linux":
                # Try xclip, then xsel
                for cmd in (['xclip', '-selection', 'clipboard'], ['xsel', '--clipboard', '--input']):
                    try:
                        subprocess.run(cmd, input=text, encoding='utf-8', check=True)
                        return
                    except Exception:
                        continue
                print("Tip: On Linux, install xclip or xsel for clipboard support: sudo apt-get install xclip")
            elif system == "Windows":
                try:
                    subprocess.run(['clip'], input=text, encoding='utf-8', check=True)
                    return
                except Exception:
                    print("Tip: On Windows, 'clip' should be available in standard shells.")
            # If all fallbacks fail
            print(f"Failed to copy to clipboard. Use --no-copy to disable auto copy.")
        except Exception:
            print(f"Failed to copy to clipboard. Use --no-copy to disable auto copy.")

    @staticmethod
    def clear_input(input):
        input = input.strip()
        return input

    @staticmethod
    def validate_input(prompt):
        # Allow common natural language and shell characters
        pattern = r'^[A-Za-z0-9\s_\-@\$\.,:;\/#\+\*=()\[\]{}<>!\\|&"\'?~`]+$'
        return re.match(pattern, str(prompt)) is not None

    @staticmethod
    def validate_api_key(api_key):
        if not api_key.startswith('sk-'):
            return False
        # if len(api_key) != 51:
        #     return False
        if not re.match("^[a-zA-Z0-9-_]+$", api_key):
            return False
        return True

    @staticmethod
    def get_line_number():
        frame = inspect.currentframe().f_back
        return frame.f_lineno


helpers = Helpers()
