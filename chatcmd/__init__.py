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
Open Source AI-driven CLI command lookup, SQL Generator and other tools using multiple AI models
          Boost Your Productivity, Say Goodbye to Manual Searches
   --------------------------------------------------------------------

Usage:
    chatcmd [options]

Core Features:
  -c, --cmd                         looking up a CLI command.
  -q, --sql                         generate SQL query.

Tools:
  --random-useragent                generate a random user-agent
  --get-ip                          get your public IP address.
  --random-password [<length>]       generate a random password (default: 18).
  --color-code                      get a color Hex code.
  --lookup-http-code                lookup HTTP Code by code number.
  --port-lookup                     lookup any port number.
  --regex-pattern                   generate regex pattern for description.
  --base64-encode                   encode text to base64.
  --base64-decode                   decode base64 text.
  --generate-uuid <version>         generate UUID (1, 3, 4, 5).
  --timestamp-convert <format>      convert timestamp (unix, iso, readable).

Library Options:
  -k, --set-key                     set or update API key (legacy OpenAI only).
  -o, --get-key                     display API key (legacy OpenAI only).
  -m, --model <model>               select AI model (gpt-3.5-turbo, gpt-4, claude-3-haiku, etc.)
  --list-models                     list all available AI models
  --model-info <model>              show information about a specific model
  --set-model-key <provider>        set API key for specific provider
  --get-model-key <provider>        get API key for specific provider
  --current-model                   show current model and provider
  --performance-stats               show model performance statistics
  --reset-config                    clear config, stored keys (with confirmation)
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

from docopt import docopt
import requests
import sys

# Re-export from core.display for backward compatibility
from chatcmd.core.display import Colors, colored_print, print_header

# All CLI option keys for initialization
CLI_OPTIONS = [
    '--cmd', '--sql', '--get-ip', '--random-useragent', '--random-password',
    '--color-code', '--lookup-http-code', '--port-lookup', '--set-key', '--get-key',
    '--get-cmd', '--get-last', '--delete-cmd', '--delete-last-cmd', '--cmd-total',
    '--clear-history', '--db-size', '--no-copy', '--help', '--version', '--library-info',
    '--regex-pattern', '--base64-encode', '--base64-decode', '--generate-uuid',
    '--timestamp-convert', '--model', '--list-models', '--model-info',
    '--set-model-key', '--get-model-key', '--current-model', '--performance-stats',
    '--reset-config'
]


def print_colored_usage():
    """Print colored usage information"""
    import os
    if os.environ.get('CHATCMD_QUIET') == '1':
        return

    colored_print("Usage:", Colors.YELLOW)
    colored_print("    chatcmd [options]", Colors.WHITE)
    print()

    # Core Features
    colored_print("Core Features:", Colors.YELLOW)
    _print_option("-c, --cmd", "looking up a CLI command.")
    _print_option("-q, --sql", "generate SQL query.")
    print()

    # Tools
    colored_print("Tools:", Colors.YELLOW)
    _print_option("--random-useragent", "generate a random user-agent")
    _print_option("--get-ip", "get your public IP address.")
    _print_option("--random-password [<length>]", "generate a random password (default: 18).")
    _print_option("--color-code", "get a color Hex code.")
    _print_option("--lookup-http-code", "lookup HTTP Code by code number.")
    _print_option("--port-lookup", "lookup any port number.")
    _print_option("--regex-pattern", "generate regex pattern for description.")
    _print_option("--base64-encode", "encode text to base64.")
    _print_option("--base64-decode", "decode base64 text.")
    _print_option("--generate-uuid <version>", "generate UUID (1, 3, 4, 5).")
    _print_option("--timestamp-convert <format>", "convert timestamp (unix, iso, readable).")
    print()

    # Library Options
    colored_print("Library Options:", Colors.YELLOW)
    _print_option("-k, --set-key", "set or update API key (legacy OpenAI only).")
    _print_option("-o, --get-key", "display API key (legacy OpenAI only).")
    _print_option("-m, --model <model>", "select AI model (gpt-3.5-turbo, gpt-4, claude-3-haiku, etc.)")
    _print_option("--list-models", "list all available AI models")
    _print_option("--model-info <model>", "show information about a specific model")
    _print_option("--set-model-key <provider>", "set API key for specific provider")
    _print_option("--get-model-key <provider>", "get API key for specific provider")
    _print_option("--current-model", "show current model and provider")
    _print_option("--performance-stats", "show model performance statistics")
    _print_option("--reset-config", "clear config and stored keys (with confirmation)")
    _print_option("-g, --get-cmd", "display the last command.")
    _print_option("-G, --get-last=<value>", "display the last [number] of commands.")
    _print_option("-d, --delete-cmd", "delete the last command.")
    _print_option("-D, --delete-last-cmd=<value>", "delete the last [number] of commands.")
    _print_option("-t, --cmd-total", "display the total number of commands.")
    _print_option("-r, --clear-history", "clear all history records.")
    _print_option("-s, --db-size", "display the database size.")
    _print_option("-n, --no-copy", "disable copy feature.")
    _print_option("-h, --help", "display this screen.")
    _print_option("-v, --version", "display ChatCMD version.")
    _print_option("-x, --library-info", "display library information.")


def _print_option(option: str, description: str):
    """Print a single option with formatting"""
    colored_print("  ", Colors.WHITE, end="")
    colored_print(option.ljust(30), Colors.GREEN, end="")
    colored_print(description, Colors.WHITE)


class ChatCMD:
    """Main ChatCMD application class"""

    def __init__(self):
        try:
            self.args = docopt(__doc__)
        except SystemExit:
            self._handle_parse_error()

        # Initialize components
        from chatcmd.database.schema_manager import SchemaManager
        from chatcmd.lookup.enhanced_lookup import EnhancedLookup
        from chatcmd.api.enhanced_api import EnhancedAPI
        from chatcmd.config.model_config import ModelConfig

        self.db_manager = SchemaManager()
        self.enhanced_lookup = EnhancedLookup(self.db_manager)
        self.enhanced_api = EnhancedAPI(self.db_manager)
        self.model_config = ModelConfig()

        # Backward compatibility
        self.db_path = self.db_manager.db_path
        self.conn = self.db_manager.conn
        self.cursor = self.db_manager.cursor

    def _handle_parse_error(self):
        """Handle docopt parse errors for special cases"""
        if any(flag in sys.argv for flag in ('--help', '-h')):
            self.args = {'--help': True}
            for key in CLI_OPTIONS:
                self.args.setdefault(key, False)
        elif len(sys.argv) == 2 and sys.argv[1] == '--random-password':
            self.args = {'--random-password': '18'}
            for key in CLI_OPTIONS:
                if key != '--random-password':
                    self.args[key] = False if key.startswith('--') and '=' not in key else None
        else:
            raise

    def cmd(self):
        """Main command handler"""
        try:
            from chatcmd.helpers import Helpers
            from chatcmd.cli import CommandRouter

            # Check for updates
            Helpers.get_latest_version_from_pypi()

            # Route command
            router = CommandRouter(
                self.args,
                self.db_manager,
                self.enhanced_lookup,
                self.enhanced_api,
                self.model_config
            )
            router.route()

        except KeyboardInterrupt:
            colored_print("\nOperation cancelled by user.", Colors.YELLOW, bold=True)
        except requests.RequestException:
            colored_print("Network error: Unable to connect. Please check your connection.", Colors.RED, bold=True)
        except Exception:
            colored_print("Error 1001: An unexpected error occurred. Please try again.", Colors.RED, bold=True)
        finally:
            self._cleanup()

    def _cleanup(self):
        """Clean up database connections"""
        try:
            if hasattr(self, 'cursor') and self.cursor:
                self.cursor.close()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception:
            pass
