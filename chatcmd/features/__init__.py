from fake_useragent import UserAgent
import requests
import pyperclip


class Features:

    @staticmethod
    def generate_user_agent(self, os=None, browser=None):
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
    def get_public_ip_address(self):
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
