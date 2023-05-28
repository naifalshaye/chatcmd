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
  -i, --library-info                display library information.
"""

import sqlite3
from docopt import docopt
from .helpers import *
from .lookup import *
from .api import *

no_copy = False

def main():
    try:
        args = docopt(__doc__)
        try:
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))
            db_path = os.path.join(BASE_DIR, "chatcmd/db.sqlite")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
        except sqlite3.Error as e:
            print(f"Error 1002: Failed to connect to database: {e}")

        api_key = get_api_key(conn, cursor)

        if api_key is None:
            api_key = ask_for_api_key(conn, cursor)

        openai.api_key = api_key

        if args['--version']:
            print('ChatCMD'+' 1.1.8')
        elif args['--set-key']:
            ask_for_api_key(conn, cursor)
        elif args['--get-key']:
            output_api_key(conn, cursor)
        elif args['--get-cmd']:
            get_cmd(conn, cursor)
        elif args['--get-last']:
            get_last_num_cmd(conn, cursor, args['--get-last'])
        elif args['--cmd-total']:
            print(f'\nTotal of {get_commands_count(conn, cursor)} commands\n')
        elif args['--delete-cmd']:
            delete_cmd(conn, cursor)
        elif args['--delete-last-cmd']:
            delete_last_num_cmd(conn, cursor, args['--delete-last-cmd'])
        elif args['--clear-history']:
            clear_history(conn, cursor)
        elif args['--db-size']:
            get_db_size(db_path)
        elif args['--library-info']:
            library_info()
        elif args['--no-copy']:
            prompt(conn, cursor, api_key, True)
        else:
            prompt(conn, cursor, api_key, False)

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error 1001: {e}")


if __name__ == '__main__':
    main()
