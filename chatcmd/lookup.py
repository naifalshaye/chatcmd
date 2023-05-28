from .commands import *
import openai
import pyperclip
import platform

def prompt(conn, cursor, api_key, no_copy):
    print("""

     ######  ##     ##    ###    ########  ######  ##     ## ########
    ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
    ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
    ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
    ##       ##     ## #########    ##    ##       ##     ## ##     ##
    ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
     ######  ##     ## ##     ##    ##     ######  ##     ## ########

    """)
    if validate_api_key(api_key) is False:
        print("Error 1009: API key is invalid or missing")
    prompt = clear_input(input("Prompt: "))

    if prompt == '':
        prompt(conn, cursor, api_key)
    if prompt == 'exit':
        print('bye...')
        exit()
    elif validateInput(prompt.strip()):
        word_list = prompt.strip().split()
        if len(word_list) >= 3:
            command = lookup(prompt, api_key)
            if command is not None:
                if no_copy == False:
                    if platform.system() == "Linux":
                        copy_to_clipboard(command)
                    else:
                        pyperclip.copy(command)

                command = clear_input(command)

                if command.find('there is no command') is True and command.find('There is no specific command') is True:
                    print('there is no command for this!')
                else:
                    history = add_cmd(conn, cursor, prompt, command.strip())
                    if history is False:
                        print("Error 1008 Failed to add command to history")
                    print(" " + command.strip())
                    print('')
        else:
            print("\nPlease type in more than two words.\n")
    else:
        print("\nOnly English characters allowed.\n")


def lookup(prompt, api_key):
    try:
        if validate_api_key(api_key) is False:
            print("Error 1009: API key is invalid or missing")
            exit()

        prompt = prompt
        print("Looking up...\n")

        stop_keywords = ["###", "END", "stop", "Command:", "Syntax:", "Usage:","Windows is:","is:"]
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=f"Please help me with a CLI command lookup, I only need the command without any extra information: Show me the command for {prompt}",
            max_tokens=70,
            n=1,
            stop=None,
            temperature=0.7)
        message = response.choices[0].text.strip()
        return message

    except openai.error.OpenAIError as e:
        print(f"Error 1010: OpenAI API error occurred: {e}. Please double check your API Key.")
    except Exception as e:
        print(f"Error 1011: Unhandled exception occurred: {e}")
