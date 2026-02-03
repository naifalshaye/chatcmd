"""
Network tools for ChatCMD
IP lookup and network utilities
"""

import os
import time
import requests
import pyperclip
from chatcmd.core.display import Colors, colored_print, print_error


def get_public_ip() -> str:
    """
    Get public IP address

    Returns:
        Public IP address string
    """
    attempts = int(os.environ.get('CHATCMD_RETRY_ATTEMPTS', '2'))
    backoff = float(os.environ.get('CHATCMD_RETRY_BACKOFF', '0.5'))

    for i in range(max(1, attempts)):
        try:
            response = requests.get("https://api.ipify.org?format=json", timeout=3)
            if response.status_code == 200:
                ip_data = response.json()
                public_ip = ip_data.get("ip", "")
                if public_ip:
                    colored_print(public_ip, Colors.BRIGHT_GREEN, bold=True)
                    try:
                        pyperclip.copy(public_ip)
                    except Exception:
                        pass
                    return public_ip
        except requests.RequestException:
            pass
        time.sleep(backoff * (2 ** i))

    print_error("Unable to retrieve public IP address. Check your network connection.")
    return ""
