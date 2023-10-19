import re
import inspect
import subprocess
import requests
import importlib.metadata


class Helpers:

    @staticmethod
    def get_latest_version_from_pypi():
        response = requests.get(f"https://pypi.org/pypi/chatcmd/json")
        data = response.json()
        latest_version = data["info"]["version"]
        installed_version = importlib.metadata.version('chatcmd')

        if installed_version != latest_version:
            print(f"New version {latest_version} is available! You are currently using version {installed_version}.")
            print("Consider upgrading using: pip3 install --upgrade chatcmd")

    @staticmethod
    def library_info(self):
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
    def copy_to_clipboard(self, text):
        try:
            subprocess.run(['/usr/bin/xclip', '-selection', 'clipboard'], input=text, encoding='utf-8', check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to copy command to clipboard. Find how to avoid this error in the documentation.")

    @staticmethod
    def clear_input(self, input):
        input = input.strip()
        return input

    @staticmethod
    def validate_input(self, prompt):
        pattern = r'^[A-Za-z0-9 _\-@$\.]+$'
        if re.match(pattern, str(prompt)):
            return True

        return False

    @staticmethod
    def validate_api_key(self, api_key):
        if api_key[0:3] != 'sk-':
            return False
        if len(api_key) != 51:
            return False
        if not re.match("^[a-zA-Z0-9-]+$", api_key):
            return False
        return True

    @staticmethod
    def get_line_number(self):
        frame = inspect.currentframe().f_back
        return frame.f_lineno


helpers = Helpers()
