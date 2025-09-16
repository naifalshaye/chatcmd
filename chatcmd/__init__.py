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
  --qr-code                         generate QR code for text/URL.

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
from chatcmd.helpers import Helpers
from chatcmd.lookup.enhanced_lookup import EnhancedLookup
from chatcmd.api.enhanced_api import EnhancedAPI
from chatcmd.commands import CMD
from chatcmd.features import Features
from chatcmd.database.schema_manager import SchemaManager
from chatcmd.config.model_config import ModelConfig

import importlib.metadata
import sys
import os

cmd = CMD()
helpers = Helpers()
features = Features()

# Color constants for terminal output
class Colors:
    GREEN = '\033[92m'
    BRIGHT_GREEN = '\033[1;92m'
    YELLOW = '\033[93m'
    GOLD = '\033[38;5;220m'  # Gold color for headers
    BRIGHT_YELLOW = '\033[1;93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    RESET = '\033[0m'

def colored_print(text, color=Colors.GREEN, bold=False, end="\n"):
    """Print colored text to terminal"""
    # Honor quiet/no-color modes and non-TTY
    if os.environ.get('CHATCMD_QUIET') == '1':
        return
    if os.environ.get('CHATCMD_JSON') == '1':
        # In JSON mode, skip colored prints; caller should print structured JSON
        print(text, end=end)
        return
    if os.environ.get('CHATCMD_NO_COLOR') == '1':
        print(text, end=end)
        return
    if not sys.stdout.isatty():
        # If not a terminal, print without colors
        print(text, end=end)
        return
    
    prefix = Colors.BOLD if bold else ""
    print(f"{prefix}{color}{text}{Colors.END}", end=end)

def print_header():
    """Print the ChatCMD header with colors"""
    if os.environ.get('CHATCMD_QUIET') == '1':
        return
    header = """
            ######  ##     ##    ###    ########  ######  ##     ## ########
           ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
           ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
           ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
           ##       ##     ## #########    ##    ##       ##     ## ##     ##
           ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
            ######  ##     ## ##     ##    ##     ######  ##     ## ########
        ------------------------------------------------------------------------
Open Source AI-driven CLI command lookup, SQL Generator and other tools using multiple AI models
                  Boost Your Productivity, Say Goodbye to Manual Searches
        ------------------------------------------------------------------------
"""
    colored_print(header, Colors.WHITE
    )

def print_colored_usage():
    """Print colored usage information"""
    if os.environ.get('CHATCMD_QUIET') == '1':
        return
    colored_print("Usage:", Colors.YELLOW)
    colored_print("    chatcmd [options]", Colors.WHITE)
    print()
    
    # Core Features
    colored_print("Core Features:", Colors.YELLOW)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-c, --cmd", Colors.GREEN, end="")
    colored_print("                         looking up a CLI command.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-q, --sql", Colors.GREEN, end="")
    colored_print("                         generate SQL query.", Colors.WHITE)
    print()
    
    # Tools
    colored_print("Tools:", Colors.YELLOW)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--random-useragent", Colors.GREEN, end="")
    colored_print("                generate a random user-agent", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--get-ip", Colors.GREEN, end="")
    colored_print("                          get your public IP address.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--random-password [<length>]", Colors.GREEN, end="")
    colored_print("       generate a random password (default: 18).", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--color-code", Colors.GREEN, end="")
    colored_print("                      get a color Hex code.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--lookup-http-code", Colors.GREEN, end="")
    colored_print("                lookup HTTP Code by code number.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--port-lookup", Colors.GREEN, end="")
    colored_print("                     lookup any port number.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--regex-pattern", Colors.GREEN, end="")
    colored_print("                   generate regex pattern for description.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--base64-encode", Colors.GREEN, end="")
    colored_print("                   encode text to base64.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--base64-decode", Colors.GREEN, end="")
    colored_print("                   decode base64 text.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--generate-uuid <version>", Colors.GREEN, end="")
    colored_print("         generate UUID (1, 3, 4, 5).", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--timestamp-convert <format>", Colors.GREEN, end="")
    colored_print("      convert timestamp (unix, iso, readable).", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--qr-code", Colors.GREEN, end="")
    colored_print("                         generate QR code for text/URL.", Colors.WHITE)
    print()
    
    # Library Options
    colored_print("Library Options:", Colors.YELLOW)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-k, --set-key", Colors.GREEN, end="")
    colored_print("                     set or update API key (legacy OpenAI only).", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-o, --get-key", Colors.GREEN, end="")
    colored_print("                     display API key (legacy OpenAI only).", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-m, --model <model>", Colors.GREEN, end="")
    colored_print("               select AI model (gpt-3.5-turbo, gpt-4, claude-3-haiku, etc.)", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--list-models", Colors.GREEN, end="")
    colored_print("                     list all available AI models", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--model-info <model>", Colors.GREEN, end="")
    colored_print("              show information about a specific model", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--set-model-key <provider>", Colors.GREEN, end="")
    colored_print("        set API key for specific provider", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--get-model-key <provider>", Colors.GREEN, end="")
    colored_print("        get API key for specific provider", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--current-model", Colors.GREEN, end="")
    colored_print("                   show current model and provider", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("--performance-stats", Colors.GREEN, end="")
    colored_print("               show model performance statistics", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-g, --get-cmd", Colors.GREEN, end="")
    colored_print("                     display the last command.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-G, --get-last=<value>", Colors.GREEN, end="")
    colored_print("            display the last [number] of commands.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-d, --delete-cmd", Colors.GREEN, end="")
    colored_print("                  delete the last command.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-D, --delete-last-cmd=<value>", Colors.GREEN, end="")
    colored_print("     delete the last [number] of commands.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-t, --cmd-total", Colors.GREEN, end="")
    colored_print("                   display the total number of commands.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-r, --clear-history", Colors.GREEN, end="")
    colored_print("               clear all history records.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-s, --db-size", Colors.GREEN, end="")
    colored_print("                     display the database size.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-n, --no-copy", Colors.GREEN, end="")
    colored_print("                     disable copy feature.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-h, --help", Colors.GREEN, end="")
    colored_print("                        display this screen.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-v, --version", Colors.GREEN, end="")
    colored_print("                     display ChatCMD version.", Colors.WHITE)
    colored_print("  ", Colors.WHITE, end="")
    colored_print("-x, --library-info", Colors.GREEN, end="")
    colored_print("                display library information.", Colors.WHITE)


class ChatCMD:
    def __init__(self):
        try:
            self.args = docopt(__doc__)
        except SystemExit:
            # Handle special case for --random-password without argument or explicit help flags
            import sys
            if any(flag in sys.argv for flag in ('--help', '-h')):
                # Minimal args dict to trigger unified help rendering in cmd()
                self.args = {'--help': True}
                # Initialize other expected keys to safe defaults
                for key in ['--cmd','--sql','--get-ip','--random-useragent','--random-password','--color-code',
                            '--lookup-http-code','--port-lookup','--set-key','--get-key','--get-cmd','--get-last',
                            '--delete-cmd','--delete-last-cmd','--cmd-total','--clear-history','--db-size','--no-copy',
                            '--version','--library-info','--regex-pattern','--base64-encode','--base64-decode',
                            '--generate-uuid','--timestamp-convert','--qr-code','--model','--list-models','--model-info',
                            '--set-model-key','--get-model-key','--current-model','--performance-stats']:
                    self.args.setdefault(key, False)
            elif len(sys.argv) == 2 and sys.argv[1] == '--random-password':
                # User provided --random-password without length, use default
                self.args = {'--random-password': '18'}
                # Set all other options to False/None
                for key in ['--cmd', '--sql', '--get-ip', '--random-useragent', '--color-code', 
                           '--lookup-http-code', '--port-lookup', '--set-key', '--get-key', 
                           '--get-cmd', '--get-last', '--delete-cmd', '--delete-last-cmd', 
                           '--cmd-total', '--clear-history', '--db-size', '--no-copy', 
                           '--help', '--version', '--library-info', '--regex-pattern', 
                           '--base64-encode', '--base64-decode', '--generate-uuid', '--timestamp-convert', 
                           '--qr-code', '--model', '--list-models', '--model-info', 
                           '--set-model-key', '--get-model-key', '--current-model', 
                           '--performance-stats']:
                    self.args[key] = False if key.startswith('--') and '=' not in key else None
            else:
                # Re-raise the exception for other cases
                raise
        self.no_copy = False

        # Initialize enhanced database manager with secure cross-platform path
        self.db_manager = SchemaManager()
        self.db_path = self.db_manager.db_path
        self.enhanced_lookup = EnhancedLookup(self.db_manager)
        self.model_config = ModelConfig()
        self.enhanced_api = EnhancedAPI(self.db_manager)
        
        # Keep backward compatibility
        self.conn = self.db_manager.conn
        self.cursor = self.db_manager.cursor

    def cmd(self):
        try:
            helpers.get_latest_version_from_pypi()
            
            # Unified help handling to show header + colored usage for --help/-h
            if self.args.get('--help'):
                print_header()
                print_colored_usage()
                return

            # Handle new multi-model options first
            if self.args['--list-models']:
                if os.environ.get('CHATCMD_JSON') == '1':
                    models = []
                    providers = self.model_config.get_providers()
                    for provider in providers:
                        for m in self.model_config.get_models_by_provider(provider):
                            models.append({
                                'name': m.name,
                                'display_name': m.display_name,
                                'provider': m.provider
                            })
                    import json
                    print(json.dumps({'models': models}))
                else:
                    self.enhanced_lookup.list_available_models()
                return
            
            if self.args['--model-info']:
                model_name = self.args['--model-info']
                model_info = self.model_config.get_model_info(model_name)
                if model_info:
                    if os.environ.get('CHATCMD_JSON') == '1':
                        import json
                        print(json.dumps({
                            'name': model_info.name,
                            'display_name': model_info.display_name,
                            'provider': model_info.provider,
                            'description': model_info.description,
                            'max_tokens': model_info.max_tokens,
                            'temperature': model_info.temperature
                        }))
                    else:
                        colored_print(f"\nModel: {model_info.display_name}", Colors.GREEN, bold=True)
                        colored_print(f"Provider: {model_info.provider}", Colors.BLUE)
                        colored_print(f"Description: {model_info.description}", Colors.WHITE)
                        colored_print(f"Max Tokens: {model_info.max_tokens}", Colors.YELLOW)
                        colored_print(f"Temperature: {model_info.temperature}", Colors.YELLOW)
                else:
                    colored_print(f"Model '{model_name}' not found", Colors.RED)
                return
            
            if self.args['--current-model']:
                current_info = self.enhanced_lookup.get_current_model_info()
                if os.environ.get('CHATCMD_JSON') == '1':
                    import json
                    print(json.dumps({'current': current_info}))
                else:
                    colored_print(f"\nCurrent Model: {current_info['model_display_name']} ({current_info['model_name']})", Colors.GREEN, bold=True)
                    colored_print(f"Provider: {current_info['provider_name']}", Colors.BLUE)
                    status_color = Colors.GREEN if current_info['provider_configured'] else Colors.RED
                    colored_print(f"Configured: {'Yes' if current_info['provider_configured'] else 'No'}", status_color)
                return
            
            if self.args['--performance-stats']:
                stats = self.enhanced_lookup.get_performance_stats()
                if os.environ.get('CHATCMD_JSON') == '1':
                    import json
                    print(json.dumps({'stats': stats}))
                else:
                    colored_print(f"\nPerformance Statistics (Last 7 days):", Colors.CYAN, bold=True)
                    colored_print(f"Total Requests: {stats['total_requests']}", Colors.GREEN)
                    colored_print(f"Successful: {stats['successful_requests']}", Colors.GREEN)
                    colored_print(f"Failed: {stats['failed_requests']}", Colors.RED)
                    colored_print(f"Average Response Time: {stats['average_response_time']}s", Colors.YELLOW)
                    colored_print(f"Models Used: {', '.join(stats['models_used'])}", Colors.BLUE)
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
                # Normalize early for better UX
                normalized = self.model_config.normalize_model_name(model_name) or model_name
                if self.enhanced_lookup.set_model(normalized):
                    colored_print(f"Model set to: {normalized}", Colors.GREEN, bold=True)
                else:
                    suggestion = self.model_config.suggest_model(model_name) or ""
                    if suggestion:
                        colored_print(f"Unknown model '{model_name}'. Did you mean '{suggestion}'?", Colors.YELLOW)
                    else:
                        colored_print(f"Failed to set model: {model_name}", Colors.RED)
                return
            
            # Handle model selection for lookup commands
            selected_model = None
            if self.args['--model']:
                selected_model = self.model_config.normalize_model_name(self.args['--model']) or self.args['--model']
            
            # Check if any AI provider is configured
            if self.args['--cmd']:
                if not self._is_any_provider_configured():
                    self._setup_initial_provider()
                
                if selected_model:
                    self.enhanced_lookup.prompt(False, selected_model)
                else:
                    # Use enhanced lookup for better multi-model support
                    self.enhanced_lookup.prompt(False)
            elif self.args['--sql']:
                if not self._is_any_provider_configured():
                    self._setup_initial_provider()
                
                if selected_model:
                    self.enhanced_lookup.prompt_sql(False, selected_model)
                else:
                    # Use enhanced lookup for SQL query generation
                    self.enhanced_lookup.prompt_sql(False)
            elif self.args['--get-ip']:
                features.get_public_ip_address()
            elif self.args['--random-useragent']:
                features.generate_user_agent()
            elif self.args['--random-password'] is not None:
                # Get length from argument, use default if not provided
                length_str = self.args['--random-password']
                try:
                    length = int(length_str)
                    if length < 1:
                        length = 18
                    elif length > 1000:  # Reasonable upper limit
                        length = 1000
                except (ValueError, TypeError):
                    length = 18
                features.generate_random_password(length)
            elif self.args['--color-code']:
                # Provider-agnostic color code using current selected model
                self.enhanced_lookup.color_code()
            elif self.args['--lookup-http-code']:
                features.lookup_http_code()
            elif self.args['--port-lookup']:
                # Provider-agnostic port lookup using current selected model
                self.enhanced_lookup.port_lookup()
            elif self.args['--set-key']:
                self.enhanced_api.ask_for_provider_api_key('openai')
            elif self.args['--get-key']:
                self._get_provider_api_key('openai')
            elif self.args['--get-cmd']:
                cmd.get_cmd(self.cursor)
            elif self.args['--get-last']:
                cmd.get_last_num_cmd(self.cursor, self.args['--get-last'])
            elif self.args['--cmd-total']:
                count = cmd.get_commands_count(self.cursor)
                colored_print(f'\nTotal of {count} commands\n', Colors.CYAN, bold=True)
            elif self.args['--delete-cmd']:
                cmd.delete_cmd(self.conn, self.cursor)
            elif self.args['--delete-last-cmd']:
                cmd.delete_last_num_cmd(self.conn, self.cursor, self.args['--delete-last-cmd'])
            elif self.args['--clear-history']:
                cmd.clear_history(self.conn, self.cursor)
            elif self.args['--db-size']:
                cmd.get_db_size(self.db_path)
            elif self.args['--library-info']:
                helpers.library_info()
            elif self.args['--reset-config']:
                auto_yes = os.environ.get('CHATCMD_YES') == '1'
                if not auto_yes:
                    try:
                        confirm = input("This will clear local config and stored API keys. Proceed? (y/N): ").strip().lower()
                        if confirm not in ('y', 'yes'):
                            colored_print("Cancelled.", Colors.YELLOW)
                            return
                    except KeyboardInterrupt:
                        colored_print("\nCancelled.", Colors.YELLOW)
                        return
                if self.enhanced_api.reset_configuration():
                    colored_print("Configuration reset successfully.", Colors.GREEN, bold=True)
                else:
                    colored_print("Failed to reset configuration.", Colors.RED)
                return
            elif self.args['--no-copy']:
                if selected_model:
                    self.enhanced_lookup.prompt(True, selected_model)
                else:
                    self.enhanced_lookup.prompt(True)
            elif self.args['--regex-pattern']:
                description = input("Regex description: ")
                features.generate_regex_pattern(description)
            elif self.args['--base64-encode']:
                text = input("Text to encode: ")
                features.base64_encode_decode(text, 'encode')
            elif self.args['--base64-decode']:
                text = input("Base64 text to decode: ")
                features.base64_encode_decode(text, 'decode')
            elif self.args['--generate-uuid']:
                version = int(self.args['--generate-uuid'])
                features.generate_uuid(version)
            elif self.args['--timestamp-convert']:
                format_type = self.args['--timestamp-convert']
                timestamp = input("Timestamp to convert: ")
                features.convert_timestamp(timestamp, format_type)
            elif self.args['--qr-code']:
                text = input("Text/URL for QR code: ")
                features.generate_qr_code(text)
            elif self.args['--version']:
                version = importlib.metadata.version('chatcmd')
                colored_print('ChatCMD ' + version, Colors.BRIGHT_GREEN, bold=True)
            else:
                print_header()
                print_colored_usage()
                exit(0)

        except KeyboardInterrupt:
            colored_print("\nOperation cancelled by user.", Colors.YELLOW, bold=True)
        except requests.RequestException as e:
            colored_print(f"Network error: {e}", Colors.RED, bold=True)
        except Exception as e:
            colored_print(f"Error 1001: {e}", Colors.RED, bold=True)
        finally:
            try:
                if hasattr(self, 'cursor') and self.cursor:
                    self.cursor.close()
                if hasattr(self, 'conn') and self.conn:
                    self.conn.close()
            except Exception:
                pass
    
    def _is_any_provider_configured(self) -> bool:
        """Check if any AI provider has an API key configured"""
        providers = ['openai', 'anthropic', 'google', 'cohere', 'ollama']
        for provider in providers:
            if self.enhanced_api.get_provider_api_key(provider):
                return True
        return False
    
    def _setup_initial_provider(self):
        """Guide user through initial provider setup"""
        print_header()
        
        colored_print("No AI provider configured yet. Let's set up your first provider!", Colors.YELLOW, bold=True)
        colored_print("\nAvailable AI Providers:", Colors.CYAN, bold=True)
        colored_print("1. OpenAI (GPT-3.5, GPT-4)", Colors.GREEN)
        colored_print("2. Anthropic (Claude 3)", Colors.BLUE)
        colored_print("3. Google (Gemini Pro)", Colors.MAGENTA)
        colored_print("4. Cohere (Command)", Colors.CYAN)
        colored_print("5. Ollama (Local models)", Colors.WHITE)
        
        while True:
            try:
                choice = input("\nSelect provider (1-5): ").strip()
                provider_map = {
                    '1': 'openai',
                    '2': 'anthropic', 
                    '3': 'google',
                    '4': 'cohere',
                    '5': 'ollama'
                }
                
                if choice in provider_map:
                    provider = provider_map[choice]
                    self._set_provider_api_key(provider)
                    break
                else:
                    colored_print("Invalid choice. Please select 1-5.", Colors.RED)
            except KeyboardInterrupt:
                colored_print("\nSetup cancelled.", Colors.YELLOW)
                exit(0)
    
    def _set_provider_api_key(self, provider):
        """Set API key for a specific provider"""
        try:
            colored_print(f"\nEnter API key for {provider}: ", Colors.CYAN, bold=True)
            api_key = input()
            if self.enhanced_api.set_provider_api_key(provider, api_key):
                colored_print(f"\nAPI key for {provider} saved successfully.", Colors.GREEN, bold=True)
            else:
                colored_print(f"\nFailed to save API key for {provider}.", Colors.RED)
        except Exception as e:
            colored_print(f"Error setting API key: {e}", Colors.RED)
    
    def _get_provider_api_key(self, provider):
        """Get API key for a specific provider"""
        try:
            api_key = self.enhanced_api.get_provider_api_key(provider)
            if api_key:
                # Show only first 8 characters for security
                masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***masked***"
                colored_print(f"\n{provider} API key: {masked_key}", Colors.GREEN)
            else:
                colored_print(f"\nNo API key found for {provider}", Colors.RED)
        except Exception as e:
            colored_print(f"Error getting API key: {e}", Colors.RED)
