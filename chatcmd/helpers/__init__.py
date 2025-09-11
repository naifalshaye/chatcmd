import re
import inspect
import subprocess
import requests
import importlib.metadata
import platform
try:
    import pyperclip
except Exception:
    pyperclip = None


class Helpers:

    @staticmethod
    def get_latest_version_from_pypi():
        try:
            # Add timeout to prevent hanging
            response = requests.get(f"https://pypi.org/pypi/chatcmd/json", timeout=3)
            response.raise_for_status()  # Raise exception for HTTP errors
            data = response.json()
            latest_version = data["info"]["version"]
            installed_version = importlib.metadata.version('chatcmd')

            if installed_version != latest_version:
                print(f"New version {latest_version} is available! You are currently using version {installed_version}.")
                print("Consider upgrading using: pip3 install --upgrade chatcmd")
        except (requests.RequestException, KeyError, ValueError) as e:
            # Silently fail version check to avoid disrupting user workflow
            pass

    @staticmethod
    def library_info():
        print(
            "----------------------------------------------------------------\n"
            "  Library Name: ChatCMD\n"
            "  Library Source [PyPi]: https://pypi.org/naifalshaye/chatcmd\n"
            "  Library Source [Github]: https://github.com/naifalshaye/chatcmd\n"
            "  Documentation: https://github.com/naifalshaye/chatcmd#readme\n"
            "  Bug Tracker: https://github.com/naifalshaye/chatcmd/issues\n"
            "  Published Date: 2023-05-15\n"
            "  License: MIT\n"
            "  Author: Naif Alshaye\n"
            "  Author Email: naif@naif.io\n"
            "  Author Website: https://naif.io\n"
            "----------------------------------------------------------------"
        )

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
                    pass
            # Native fallbacks per OS
            if system == "Darwin":
                try:
                    subprocess.run(['pbcopy'], input=text, encoding='utf-8', check=True)
                    return
                except Exception:
                    pass
            elif system == "Linux":
                # Try xclip, then xsel
                for cmd in (['xclip', '-selection', 'clipboard'], ['xsel', '--clipboard', '--input']):
                    try:
                        subprocess.run(cmd, input=text, encoding='utf-8', check=True)
                        return
                    except Exception:
                        continue
            elif system == "Windows":
                try:
                    subprocess.run(['clip'], input=text, encoding='utf-8', check=True)
                    return
                except Exception:
                    pass
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
