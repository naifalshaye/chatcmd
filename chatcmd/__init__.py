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
  -l, --lookup-cmd                  looking up a CLI command.
  -q, --sql-query                   generate SQL query.
  -u, --random-useragent            generate a random user-agent
  -i, --get-ip                      get your public IP address.
  -p, --random-password             generate a random password.
  -c, --color-code                  get a color Hex code.
  -a, --lookup-http-code            lookup HTTP Code by code number.
  -z, --port-lookup                 lookup any port number.
  -k, --set-key                     set or update ChatGPT API key.
  -o, --get-key                     display ChatGPT API key.
  -g, --get-cmd                     display the last command.
  -G, --get-last=<value>            display the last [number] of commands.
  -d, --delete-cmd                  delete the last command.
  -D, --delete-last-cmd=<value>     delete the last [number] of commands.
  -t, --cmd-total                   display the total number of commands.
  -r, --clear-history               clear all history records.
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

import os
import sqlite3
import importlib.metadata

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
            helpers.get_latest_version_from_pypi()
            api_key = api.get_api_key(self, self.conn, self.cursor)

            if api_key is None:
                api_key = api.ask_for_api_key(self, self.conn, self.cursor)

            openai.api_key = api_key

            if self.args['--lookup-cmd']:
                lookup.prompt(self.conn, self.cursor, api_key, False)
            elif self.args['--sql-query']:
                lookup.prompt_sql(self.conn, self.cursor, api_key, False)
            elif self.args['--get-ip']:
                features.get_public_ip_address()
            elif self.args['--random-useragent']:
                features.generate_user_agent()
            elif self.args['--random-password']:
                features.generate_random_password()
            elif self.args['--color-code']:
                lookup.prompt_color(self.conn, self.cursor, api_key, False)
            elif self.args['--lookup-http-code']:
                features.lookup_http_code()
            elif self.args['--port-lookup']:
                lookup.port_lookup(self, api_key)
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
            elif self.args['--version']:
                print('ChatCMD ' + importlib.metadata.version('chatcmd'))
            else:
                print(__doc__)
                exit(0)

            self.cursor.close()
            self.conn.close()

        except Exception as e:
            print(f"Error 1001: {e}")
