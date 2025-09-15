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
        from chatcmd import Colors, colored_print
        
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

        colored_print(user_agent, Colors.BRIGHT_GREEN, bold=True)
        pyperclip.copy(user_agent)

    @staticmethod
    def get_public_ip_address():
        from chatcmd import Colors, colored_print
        
        try:
            # Use a reliable service to get your public IP address
            response = requests.get("https://api.ipify.org?format=json")

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response to extract the IP address
                ip_data = response.json()
                public_ip = ip_data["ip"]
                colored_print(public_ip, Colors.BRIGHT_GREEN, bold=True)
                pyperclip.copy(public_ip)

            else:
                colored_print("Unable to retrieve public IP address, please try again.", Colors.RED)
        except requests.RequestException as e:
            colored_print(f"An error occurred: {e}", Colors.RED)

    @staticmethod
    def generate_random_password(length=18):
        """
        Generate a random password with specified length
        
        Args:
            length (int): Length of the password (default: 18)
        """
        # Validate length
        if length < 1:
            length = 18
        elif length > 1000:  # Reasonable upper limit
            length = 1000
        
        from chatcmd import Colors, colored_print
        
        password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                           for _ in range(length))
        pyperclip.copy(password)
        colored_print(password, Colors.BRIGHT_GREEN, bold=True)

    @staticmethod
    def lookup_http_code():
        from chatcmd import Colors, colored_print
        
        colored_print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Lookup HTTP Code by code
        """, Colors.BRIGHT_GREEN)
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
            colored_print(http_codes[code], Colors.BRIGHT_GREEN, bold=True)
        else:
            colored_print('Unknown HTTP Code', Colors.RED)
    
    def generate_regex_pattern(self, description: str):
        """Generate regex patterns for common use cases"""
        return self.dev_tools.generate_regex_pattern(description)
    
    
    def base64_encode_decode(self, text: str, operation: str = 'encode'):
        """Encode or decode base64 strings"""
        return self.dev_tools.base64_encode_decode(text, operation)
    
    
    def generate_uuid(self, version: int = 4):
        """Generate UUIDs in different formats"""
        return self.dev_tools.generate_uuid(version)
    
    def convert_timestamp(self, timestamp: str, format_type: str = 'unix'):
        """Convert between different timestamp formats"""
        return self.dev_tools.convert_timestamp(timestamp, format_type)
    
    def generate_qr_code(self, text: str):
        """Generate QR code for text/URL"""
        return self.dev_tools.generate_qr_code(text)

