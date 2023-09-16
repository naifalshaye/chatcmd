#!/usr/bin/env python
"""
     ######  ##     ##    ###    ########  ######  ##     ## ########
    ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
    ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
    ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
    ##       ##     ## #########    ##    ##       ##     ## ##     ##
    ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
     ######  ##     ## ##     ##    ##     ######  ##     ## ########
   --------------------------------------------------------------------
           Open Source AI-driven CLI command lookup using ChatGPT
          Boost Your Productivity, Say Goodbye to Manual Searches
   --------------------------------------------------------------------
               Developed By: Naif Alshaye | https://naif.io

Usage:
    chatcmd [options]

Options:
  -l, --lookup                      find a CLI command.
  -u, --random-useragent            generate a random user-agent
  -i, --get-ip                      get public IP address.
  -p, --random-password             get public IP address.
  -k, --set-key                     set or update ChatGPT API key.
  -o, --get-key                     display ChatGPT API key.
  -g, --get-cmd                     display the last command.
  -G, --get-last=<value>            display the last [number] of commands.
  -d, --delete-cmd                  delete the last command.
  -D, --delete-last-cmd=<value>     delete the last [number] of commands.
  -t, --cmd-total                   display the total number of commands.
  -c, --clear-history               clear all history records.
  -s, --db-size                     display the database size.
  -n, --no-copy                     disable copy feature.
  -h, --help                        display this screen.
  -v, --version                     display ChatCMD version.
  -x, --library-info                display library information.
"""

import openai
from docopt import docopt
from chatcmd.helpers import Helpers
from chatcmd.lookup import Lookup
from chatcmd.api import API
from chatcmd.commands import CMD
from chatcmd.features import Features
import pyperclip
import string
import secrets
import os
import sqlite3

lookup = Lookup()
api = API()
cmd = CMD()
helpers = Helpers()
features = Features()


class ChatCMD:
    def __init__(self):
        self.args = docopt(__doc__)
        self.no_copy = False

        self.BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.db_path = os.path.join(self.BASE_DIR, "chatcmd/db.sqlite")
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def cmd(self):
        try:
            api_key = api.get_api_key(self, self.conn, self.cursor)

            if api_key is None:
                api_key = api.ask_for_api_key(self, self.conn, self.cursor)

            openai.api_key = api_key

            if self.args['--version']:
                print('ChatCMD' + ' 1.1.8')
            elif self.args['--set-key']:
                api.ask_for_api_key(self, self.conn, self.cursor)
            elif self.args['--get-key']:
                api.output_api_key(self, self.conn, self.cursor)
            elif self.args['--get-cmd']:
                cmd.get_cmd(self.cursor)
            elif self.args['--get-last']:
                cmd.get_last_num_cmd(self.cursor, self.args['--get-last'])
            elif self.args['--cmd-total']:
                print(f'\nTotal of {cmd.get_commands_count(self.cursor)} commands\n')
            elif self.args['--delete-cmd']:
                cmd.delete_cmd(self.conn, self.cursor)
            elif self.args['--delete-last-cmd']:
                cmd.delete_last_num_cmd(self.conn, self.cursor, self.args['--delete-last-cmd'])
            elif self.args['--clear-history']:
                cmd.clear_history(self, self.cursor)
            elif self.args['--db-size']:
                cmd.get_db_size(self.db_path)
            elif self.args['--library-info']:
                helpers.library_info(self)
            elif self.args['--no-copy']:
                lookup.prompt(self.conn, self.cursor, api_key, True)
            elif self.args['--lookup']:
                lookup.prompt(self.conn, self.cursor, api_key, False)
            elif self.args['--get-ip']:
                features.get_public_ip_address(self)
            elif self.args['--random-useragent']:
                features.generate_user_agent(self)
            elif self.args['--random-password']:
                length = 16
                password = ''.join(secrets.choice(string.ascii_letters + string.digits + string.punctuation)
                                   for _ in range(length))
                print(password)
                pyperclip.copy(password)

            else:
                print(__doc__)
                exit(0)

            self.cursor.close()
            self.conn.close()

        except Exception as e:
            print(f"Error 1001: {e}")
