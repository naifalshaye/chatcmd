from openai import OpenAI
import pyperclip
import platform
from chatcmd.commands import CMD
from chatcmd.helpers import Helpers

cmd = CMD()
helpers = Helpers()


class Lookup:

    def prompt(self, conn, cursor, api_key, no_copy):
        print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Lookup CLI Commands
        """)
        if helpers.validate_api_key(api_key) is False:
            print("Error 1009: API key is invalid or missing")
        prompt = helpers.clear_input(input("Prompt: "))

        if prompt == '':
            self.prompt(conn, cursor, api_key, no_copy)
            return
        if prompt == 'exit':
            print('bye...')
            return
        else:
            word_list = prompt.strip().split()
            if len(word_list) >= 3:
                command = self.lookup(prompt, api_key)
                if command is not None:
                    if not no_copy:
                        if platform.system() == "Linux":
                            helpers.copy_to_clipboard(command)
                        else:
                            pyperclip.copy(command)

                    command = helpers.clear_input(command)

                    if command.find('there is no command') != -1 and command.find(
                            'There is no specific command') != -1:
                        print('there is no command for this!')
                    else:
                        history = cmd.add_cmd(conn, cursor, prompt, command.strip())
                        if history is False:
                            print("Error 1008 Failed to add command to history")
                        print(" " + command.strip())
                        print('')
            else:
                print("\nPlease type in more than two words.\n")

    @staticmethod
    def lookup(prompt, api_key):
        try:
            if helpers.validate_api_key(api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()

            print("Looking up...\n")

            client = OpenAI(
                # This is the default and can be omitted
                api_key=api_key,
            )
            # stop_keywords = ["###", "END", "stop", "Command:", "Syntax:", "Usage:", "Windows is:", "is:"]
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                # prompt=f"Please help me with a CLI command lookup, I only need the command without"
                #        f" any extra information: Show me the command for {prompt}",
                messages=[
                    {
                        "role": "user",
                        "content": f" any extra information: Show me the command for {prompt}",
                    }
                ],
                max_tokens=70,
                n=1,
                stop=None,
                temperature=0.7)
            message = completion.choices[0].message.content.strip()
            return message

        except Exception as e:
            print(f"Error 1011: OpenAI API error occurred: {e}")

    def prompt_sql(self, conn, cursor, api_key, no_copy):
        print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Write SQL Queries
        """)
        if helpers.validate_api_key(api_key) is False:
            print("Error 1009: API key is invalid or missing")
        prompt = helpers.clear_input(input("SQL Query Prompt: "))

        if prompt == '':
            self.prompt(conn, cursor, api_key, no_copy)
            return
        if prompt == 'exit':
            print('bye...')
            return
        elif helpers.validate_input(prompt.strip()):
            word_list = prompt.strip().split()
            if len(word_list) >= 3:
                response = self.sql_query(prompt, api_key)
                if response is not None:
                    if not no_copy:
                        if platform.system() == "Linux":
                            helpers.copy_to_clipboard(response)
                        else:
                            pyperclip.copy(response)

                    response_text = helpers.clear_input(response)

                    if response_text.find('there is no query') != -1 and response_text.find(
                            'There is no specific query') != -1:
                        print('there is no query for this!')
                    else:
                        print(" " + response_text.strip())
                        print('')

            else:
                print("\nPlease type in more than two words.\n")

    @staticmethod
    def sql_query(prompt, api_key):
        try:
            if helpers.validate_api_key(api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()

            print("Writing SQL query...\n")

            client = OpenAI(
                api_key=api_key,
            )
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"Act like a database engineer and write a query that {prompt}",
                    }
                ],
                max_tokens=70,
                n=1,
                stop=None,
                temperature=0.7)
            response = completion.choices[0].message.content.strip()
            return response

        except Exception as e:
            print(f"Error 1010: OpenAI API error occurred: {e}. Please double check your API Key.")

    def prompt_color(self, conn, cursor, api_key, no_copy):
        print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Get Colors Hex code
        """)
        if helpers.validate_api_key(api_key) is False:
            print("Error 1009: API key is invalid or missing")
        prompt = helpers.clear_input(input("Color Prompt: "))

        if prompt == '':
            self.prompt(conn, cursor, api_key, no_copy)
            return
        if prompt == 'exit':
            print('bye...')
            return
        else:
            response = self.color_query(prompt, api_key)
            if response is not None:
                if not no_copy:
                    if platform.system() == "Linux":
                        helpers.copy_to_clipboard(response)
                    else:
                        pyperclip.copy(response)

                response = helpers.clear_input(response)

                if response.find('there is no color') != -1 and response.find(
                        'There is no specific color') != -1:
                    print('there is no color for this!')
                else:
                    print(" " + response.strip())
                    print('')

            else:
                print("\nPlease type in more than two words.\n")

    @staticmethod
    def color_query(prompt, api_key):
        try:
            if helpers.validate_api_key(api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()

            print("Getting color code...\n")

            client = OpenAI(
                api_key=api_key,
            )
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"What is the HEX code for this color, return code only: {prompt}",
                    }
                ],
                max_tokens=70,
                n=1,
                stop=None,
                temperature=0.7)
            response = completion.choices[0].message.content.strip()
            return response

        except Exception as e:
            print(f"Error 1010: OpenAI API error occurred: {e}. Please double check your API Key.")

    @staticmethod
    def port_lookup(api_key):
        try:
            if helpers.validate_api_key(api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()
            prompt = helpers.clear_input(input("Port: "))

            client = OpenAI(
                api_key=api_key,
            )
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"lookup this port: {prompt}",
                    }
                ],
                max_tokens=70,
                n=1,
                stop=None,
                temperature=0.7)
            response = completion.choices[0].message.content
            print(response)

        except Exception as e:
            print(f"Error 1010: OpenAI API error occurred: {e}. Please double check your API Key.")


lookup = Lookup()
