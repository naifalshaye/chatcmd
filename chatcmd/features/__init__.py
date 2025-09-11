from fake_useragent import UserAgent
import requests
import pyperclip
import string
import secrets
from .developer_tools import DeveloperTools


class Features:

    def __init__(self):
        self.dev_tools = DeveloperTools()

    @staticmethod
    def generate_user_agent(os=None, browser=None):
        ua = UserAgent()
        if os == "linux":
            if browser == "firefox":
                user_agent = ua.firefox
            elif browser == "chrome":
                user_agent = ua.chrome
            elif browser == "opera":
                user_agent = ua.opera
            # Add more browser options for Linux as needed
            else:
                user_agent = ua.random
        elif os == "windows":
            if browser == "firefox":
                user_agent = ua.firefox
            elif browser == "chrome":
                user_agent = ua.chrome
            elif browser == "edge":
                user_agent = ua.edge
            # Add more browser options for Windows as needed
            else:
                user_agent = ua.random
        elif os == "macos":
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

        print(user_agent)
        pyperclip.copy(user_agent)

    @staticmethod
    def get_public_ip_address():
        try:
            # Use a reliable service to get your public IP address
            response = requests.get("https://api.ipify.org?format=json")

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response to extract the IP address
                ip_data = response.json()
                public_ip = ip_data["ip"]
                print(public_ip)
                pyperclip.copy(public_ip)

            else:
                print("Unable to retrieve public IP address, please try again.")
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def generate_random_password():
        length = 16
        password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                           for _ in range(length))
        pyperclip.copy(password)
        print(password)

    @staticmethod
    def lookup_http_code():
        print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Lookup HTTP Code by code
        """)
        code = input("HTTP Code: ")
        http_codes = {
            '100': "Continue",
            '101': "Switching Protocols",
            '200': "OK",
            '201': "Created",
            '202': "Accepted",
            '203': "Non-Authoritative Information",
            '204': "No Content",
            '205': "Reset Content",
            '206': "Partial Content",
            '300': "Multiple Choices",
            '301': "Moved Permanently",
            '302': "Found",
            '303': "See Other",
            '304': "Not Modified",
            '305': "Use Proxy",
            '307': "Temporary Redirect",
            '400': "Bad Request",
            '401': "Unauthorized",
            '402': "Payment Required",
            '403': "Forbidden",
            '404': "Not Found",
            '405': "Method Not Allowed",
            '406': "Not Acceptable",
            '407': "Proxy Authentication Required",
            '408': "Request Timeout",
            '409': "Conflict",
            '410': "Gone",
            '411': "Length Required",
            '412': "Precondition Failed",
            '413': "Payload Too Large",
            '414': "URI Too Long",
            '415': "Unsupported Media Type",
            '416': "Range Not Satisfiable",
            '417': "Expectation Failed",
            '500': "Internal Server Error",
            '501': "Not Implemented",
            '502': "Bad Gateway",
            '503': "Service Unavailable",
            '504': "Gateway Timeout",
            '505': "HTTP Version Not Supported"
        }
        if code in http_codes:
            print(http_codes[code])
        else:
            print('Unknown HTTP Code')
    
    def generate_regex_pattern(self, description: str):
        """Generate regex patterns for common use cases"""
        return self.dev_tools.generate_regex_pattern(description)
    
    
    def base64_encode_decode(self, text: str, operation: str = 'encode'):
        """Encode or decode base64 strings"""
        return self.dev_tools.base64_encode_decode(text, operation)
    
    def generate_git_commands(self, operation: str):
        """Generate common git commands"""
        return self.dev_tools.generate_git_commands(operation)
    
    def generate_docker_commands(self, operation: str):
        """Generate common Docker commands"""
        return self.dev_tools.generate_docker_commands(operation)
    
    def generate_uuid(self, version: int = 4):
        """Generate UUIDs in different formats"""
        return self.dev_tools.generate_uuid(version)
    
    def convert_timestamp(self, timestamp: str, format_type: str = 'unix'):
        """Convert between different timestamp formats"""
        return self.dev_tools.convert_timestamp(timestamp, format_type)
    
    def generate_qr_code(self, text: str):
        """Generate QR code for text/URL"""
        return self.dev_tools.generate_qr_code(text)

