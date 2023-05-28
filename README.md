# ChatCMD #
#### **ChatCMD** is an open source AI-driven CLI-based command lookup using ChatGPT to lookup relevant CLI commands based on user input. ####

#### Boost Your Productivity, ***Say Goodbye*** to Manual Searches ####

## Features ##
- CLI-based command lookup using ChatGPT.
- Auto copy command to clipboard.
- Disable copy feature.
- Store Data in Sqlite Database.
- Add or update ChatGPT API key.
- Validate ChatGPT API key.
- Display ChatGPT API Key.
- Display last command.
- Display last {number} of commands.
- Delete last Command.
- Delete last {number} of commands.
- Display the total number of commands.
- Clear all history records.
- Display the database file size.
- Clear and validate user inputs.
- Clear and validate lookup results to ensure only valid CLI commands are returned.
- Error handling
- Display library information.

## Requirements ##
    Python >= 3.8.9
    OpenAI account and valid API key
    https://platform.openai.com/signup
## Installation ##
    pip3 install chatcmd
    
If pip not installed:

    python3 -m pip install chatcmd

Installation output should display:

    Collecting chatcmd
    Using cached chatcmd-1.1.8-py3-none-any.whl (6.8 kB)
    Installing collected packages: chatcmd
    Successfully installed chatcmd-1.1.8

### Upgrade ###
    pip3 install --upgrade chatcmd

If pip not installed:

    python3 -m pip install --upgrade chatcmd

### Uninstall ###
    pip3 uninstall chatcmd

If pip not installed:

    python3 -m pip uninstall chatcmd
## Usage ##

```
Usage:

chatcmd [options]
  
Options:
  -k, --set-key                     set or update ChatGPT API key.
  -o, --get-key                     display ChatGPT API key.
  -g, --get-cmd                     display the last command.
  -G, --get-last=<value>            display the last [number] of commands.
  -d, --delete-cmd                  delete the last command.
  -D, --delete-last-cmd=<value>     delete the last [number] of commands.
  -t, --cmd-total                   display the total number of commands.
  -c, --clear-history               clear all history records.
  -s, --db-size                     display the database size.
  -h, --help                        display this screen.
  -n, --no-copy                     disable copy feature.
  -v, --version                     display ChatCMD version.
  -i, --library-info                display library information.

```

## Error Codes ##
Include an exception message for each error if occurs.

| Code |             Description             |
|------|:-----------------------------------:|
| 1001 |          General exception          |
| 1002 |    Failed to connect to database    |
| 1003 | Failed to get API key from database |
| 1004 |      Failed to output API key       |
| 1005 | Failed to save API key to database  |
| 1006 |       Invalid ChatGPT API key       |
| 1007 |      Failed requesting API key      |
| 1008 |        Failed to add command        |
| 1009 |    API key is invalid or missing    |
| 1010 |      OpenAI API error occurred      |
| 1011 |      Lookup exception occurred      |
| 1012 |        Failed to add command        |
| 1013 |     Failed to get last command      |
| 1014 |    Failed to get list of command    |
| 1015 |    Failed deleting last command     |
| 1016 |     Failed to get last command      |
| 1017 |       Failed clearing history       |
| 1018 |       Failed to copy command        |

### Linux copy command issue
In order to perform a Graphics-related job in a Unix environment,
the DISPLAY variable needs to be set initially.
An error can occur when connecting to Linux via SSH, particularly if there is no copy/paste mechanism like Xclip installed.
To resolve this, you can try installing Xclip using the following command: "sudo apt-get install xclip".
Additionally, you need to export the DISPLAY variable by running: "export DISPLAY=:0.0".

To avoid the error message, you can use the "-no-copy" option when looking up a command, as it disables the copy feature.

## Screenshots ##
### Help screen: ###
<img src="https://github.com/naifalshaye/chatcmd/raw/master/chatcmd/images/help.png" alt="Help Screen" style="width:550px;"/>

### Library Info: ###
<img src="https://github.com/naifalshaye/chatcmd/raw/master/chatcmd/images/library-info.png" alt="Lookup Screen" style="width:500px;"/>

### Command Lookup screen: ###
<img src="https://github.com/naifalshaye/chatcmd/raw/master/chatcmd/images/lookup.png" alt="Lookup Screen" style="width:500px;"/>

### Tested on: ###
 - Ubuntu 22.04
 - Windows Server 2022
 - macOS Ventura 13.0

## Support ##
[Issues](https://github.com/naifalshaye/chatcmd/issues)


Developed and maintained by:\
Naif Alshaye\
[https://naif.io](https://naif.io)\
naif@naif.io



## License
The MIT License (MIT). Please see License File [MIT License](https://choosealicense.com/licenses/mit/) for more information.