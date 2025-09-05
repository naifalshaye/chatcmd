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
  
  # New Multi-Model Options:
  -m, --model <model>               select AI model (gpt-3.5-turbo, gpt-4, claude-3-haiku, etc.)
  --list-models                     list all available AI models
  --model-info <model>              show information about a specific model
  --set-model-key <provider>        set API key for specific provider
  --get-model-key <provider>        get API key for specific provider
  --current-model                   show current model and provider
  --performance-stats               show model performance statistics
"""

import openai
from docopt import docopt
from chatcmd.helpers import Helpers
from chatcmd.lookup import Lookup
from chatcmd.lookup.enhanced_lookup import EnhancedLookup
from chatcmd.api import API
from chatcmd.commands import CMD
from chatcmd.features import Features
from chatcmd.database.schema_manager import SchemaManager
from chatcmd.config.model_config import ModelConfig

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
        
        # Initialize enhanced database manager
        self.db_manager = SchemaManager(self.db_path)
        self.enhanced_lookup = EnhancedLookup(self.db_manager)
        self.model_config = ModelConfig()
        
        # Keep backward compatibility
        self.conn = self.db_manager.conn
        self.cursor = self.db_manager.cursor

    def cmd(self):
        try:
            helpers.get_latest_version_from_pypi()
            
            # Handle new multi-model options first
            if self.args['--list-models']:
                self.enhanced_lookup.list_available_models()
                return
            
            if self.args['--model-info']:
                model_name = self.args['--model-info']
                model_info = self.model_config.get_model_info(model_name)
                if model_info:
                    print(f"\nModel: {model_info.display_name}")
                    print(f"Provider: {model_info.provider}")
                    print(f"Description: {model_info.description}")
                    print(f"Max Tokens: {model_info.max_tokens}")
                    print(f"Temperature: {model_info.temperature}")
                else:
                    print(f"Model '{model_name}' not found")
                return
            
            if self.args['--current-model']:
                current_info = self.enhanced_lookup.get_current_model_info()
                print(f"\nCurrent Model: {current_info['model_display_name']} ({current_info['model_name']})")
                print(f"Provider: {current_info['provider_name']}")
                print(f"Configured: {'Yes' if current_info['provider_configured'] else 'No'}")
                return
            
            if self.args['--performance-stats']:
                stats = self.enhanced_lookup.get_performance_stats()
                print(f"\nPerformance Statistics (Last 7 days):")
                print(f"Total Requests: {stats['total_requests']}")
                print(f"Successful: {stats['successful_requests']}")
                print(f"Failed: {stats['failed_requests']}")
                print(f"Average Response Time: {stats['average_response_time']}s")
                print(f"Models Used: {', '.join(stats['models_used'])}")
                return
            
            if self.args['--set-model-key']:
                provider = self.args['--set-model-key']
                self._set_provider_api_key(provider)
                return
            
            if self.args['--get-model-key']:
                provider = self.args['--get-model-key']
                self._get_provider_api_key(provider)
                return
            
            if self.args['--model']:
                model_name = self.args['--model']
                if self.enhanced_lookup.set_model(model_name):
                    print(f"Model set to: {model_name}")
                else:
                    print(f"Failed to set model: {model_name}")
                return
            
            # Handle model selection for lookup commands
            selected_model = None
            if self.args['--model']:
                selected_model = self.args['--model']
            
            # Backward compatibility - get API key for OpenAI
            api_key = api.get_api_key(self, self.conn, self.cursor)
            if api_key is None:
                api_key = api.ask_for_api_key(self, self.conn, self.cursor)
            openai.api_key = api_key

            if self.args['--lookup-cmd']:
                if selected_model:
                    self.enhanced_lookup.prompt(False, selected_model)
                else:
                    # Use enhanced lookup for better multi-model support
                    self.enhanced_lookup.prompt(False)
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
                if selected_model:
                    self.enhanced_lookup.prompt(True, selected_model)
                else:
                    self.enhanced_lookup.prompt(True)
            elif self.args['--version']:
                print('ChatCMD ' + importlib.metadata.version('chatcmd'))
            else:
                print(__doc__)
                exit(0)

            self.cursor.close()
            self.conn.close()

        except Exception as e:
            print(f"Error 1001: {e}")
    
    def _set_provider_api_key(self, provider):
        """Set API key for a specific provider"""
        try:
            api_key = input(f"\nEnter API key for {provider}: ")
            if self.db_manager.add_provider(provider, api_key):
                print(f"\nAPI key for {provider} saved successfully.")
            else:
                print(f"\nFailed to save API key for {provider}.")
        except Exception as e:
            print(f"Error setting API key: {e}")
    
    def _get_provider_api_key(self, provider):
        """Get API key for a specific provider"""
        try:
            provider_info = self.db_manager.get_provider(provider)
            if provider_info and provider_info['api_key']:
                # Show only first 8 characters for security
                masked_key = provider_info['api_key'][:8] + "..." + provider_info['api_key'][-4:]
                print(f"\n{provider} API key: {masked_key}")
            else:
                print(f"\nNo API key found for {provider}")
        except Exception as e:
            print(f"Error getting API key: {e}")
