import re
import inspect
import subprocess
import sys

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


def copy_to_clipboard(text):
    try:
        subprocess.run(['/usr/bin/xclip', '-selection', 'clipboard'], input=text, encoding='utf-8', check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to copy command to clipboard. Find how to avoid this error in the documentation.")

def clear_input(input):
    input = re.sub('[^a-zA-Z0-9 -_=]', '', input.strip())
    return input

def validateInput(prompt):
    pattern = r'^[A-Za-z0-9 ]+$'
    if re.match(pattern, str(prompt)):
        return True

    return False

def validate_api_key(api_key):
    if api_key[0:3] != 'sk-':
        return False
    if len(api_key) != 51:
        return False
    if not re.match("^[a-zA-Z0-9-]+$", api_key):
        return False
    return True

def get_line_number():
    frame = inspect.currentframe().f_back
    return frame.f_lineno