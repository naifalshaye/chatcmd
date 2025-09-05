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
        if helpers.validate_api_key(self, api_key) is False:
            print("Error 1009: API key is invalid or missing")
        prompt = helpers.clear_input(self, input("Prompt: "))

        if prompt == '':
            prompt(conn, cursor, api_key)
        if prompt == 'exit':
            print('bye...')
            exit()
        else:
            word_list = prompt.strip().split()
            if len(word_list) >= 3:
                command = self.lookup(self, prompt, api_key)
                if command is not None:
                    if not no_copy:
                        if platform.system() == "Linux":
                            helpers.copy_to_clipboard(self, command)
                        else:
                            pyperclip.copy(command)

                    command = helpers.clear_input(self, command)

                    if command.find('there is no command') is True and command.find(
                            'There is no specific command') is True:
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
    def lookup(self, prompt, api_key):
        try:
            if helpers.validate_api_key(self, api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()

            prompt = prompt
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
        if helpers.validate_api_key(self, api_key) is False:
            print("Error 1009: API key is invalid or missing")
        prompt = helpers.clear_input(self, input("SQL Query Prompt: "))

        if prompt == '':
            prompt(conn, cursor, api_key)
        if prompt == 'exit':
            print('bye...')
            exit()
        elif helpers.validate_input(self, prompt.strip()):
            word_list = prompt.strip().split()
            if len(word_list) >= 3:
                response = self.sql_query(self, prompt, api_key)
                if response is not None:
                    if not no_copy:
                        if platform.system() == "Linux":
                            helpers.copy_to_clipboard(self, response)
                        else:
                            pyperclip.copy(response)

                    response_text = helpers.clear_input(self, response)

                    if response_text.find('there is no query') is True and response_text.find(
                            'There is no specific query') is True:
                        print('there is no query for this!')
                    else:
                        print(" " + response_text.strip())
                        print('')

            else:
                print("\nPlease type in more than two words.\n")

    @staticmethod
    def sql_query(self, prompt, api_key):
        try:
            if helpers.validate_api_key(self, api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()

            prompt = prompt
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
        except Exception as e:
            print(f"Error 1011: Unhandled exception occurred: {e}")

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
        if helpers.validate_api_key(self, api_key) is False:
            print("Error 1009: API key is invalid or missing")
        prompt = helpers.clear_input(self, input("Color Prompt: "))

        if prompt == '':
            prompt(conn, cursor, api_key)
        if prompt == 'exit':
            print('bye...')
            exit()
        else:
            response = self.color_query(self, prompt, api_key)
            if response is not None:
                if not no_copy:
                    if platform.system() == "Linux":
                        helpers.copy_to_clipboard(self, response)
                    else:
                        pyperclip.copy(response)

                response = helpers.clear_input(self, response)

                if response.find('there is no color') is True and response.find(
                        'There is no specific color') is True:
                    print('there is no color for this!')
                else:
                    print(" " + response.strip())
                    print('')

            else:
                print("\nPlease type in more than two words.\n")

    @staticmethod
    def color_query(self, prompt, api_key):
        try:
            if helpers.validate_api_key(self, api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()

            prompt = prompt
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
        except Exception as e:
            print(f"Error 1011: Unhandled exception occurred: {e}")

    @staticmethod
    def port_lookup(self, api_key):
        try:
            if helpers.validate_api_key(self, api_key) is False:
                print("Error 1009: API key is invalid or missing")
                exit()
            prompt = helpers.clear_input(self, input("Port: "))
            prompt = prompt

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
        except Exception as e:
            print(f"Error 1011: Unhandled exception occurred: {e}")


lookup = Lookup()
