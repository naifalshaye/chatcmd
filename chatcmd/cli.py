"""
CLI command router for ChatCMD
Handles command routing and execution
"""

import os
import json
import importlib.metadata
from typing import Optional

from chatcmd.core.display import Colors, colored_print, print_header
from chatcmd.tools import (
    base64_encode, base64_decode,
    generate_uuid, generate_password, generate_regex_pattern,
    generate_user_agent, convert_timestamp,
    get_public_ip, lookup_http_code
)
from chatcmd.constants import (
    DEFAULT_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH,
    DEFAULT_STATS_LOOKBACK_DAYS, SUPPORTED_PROVIDERS,
    API_KEY_MASK_PREFIX_LENGTH, API_KEY_MASK_SUFFIX_LENGTH,
    API_KEY_MIN_LENGTH_FOR_MASK
)


class CommandRouter:
    """Routes CLI commands to appropriate handlers"""

    def __init__(self, args, db_manager, enhanced_lookup, enhanced_api, model_config):
        self.args = args
        self.db_manager = db_manager
        self.enhanced_lookup = enhanced_lookup
        self.enhanced_api = enhanced_api
        self.model_config = model_config
        self.conn = db_manager.conn
        self.cursor = db_manager.cursor

    def route(self) -> bool:
        """
        Route command to appropriate handler.

        Returns:
            True if command was handled, False otherwise
        """
        # Help takes priority
        if self.args.get('--help'):
            return self._handle_help()

        # Try each category in order
        return (
            self._route_model_management() or
            self._route_ai_commands() or
            self._route_tools() or
            self._route_history() or
            self._route_configuration() or
            self._route_info() or
            self._handle_help()  # Default to help
        )

    def _route_model_management(self) -> bool:
        """Route model management commands."""
        if self.args['--list-models']:
            return self._handle_list_models()
        if self.args['--model-info']:
            return self._handle_model_info()
        if self.args['--current-model']:
            return self._handle_current_model()
        if self.args['--performance-stats']:
            return self._handle_performance_stats()
        if self.args['--set-model-key']:
            return self._handle_set_model_key()
        if self.args['--get-model-key']:
            return self._handle_get_model_key()
        if self.args['--model']:
            return self._handle_set_model()
        return False

    def _route_ai_commands(self) -> bool:
        """Route AI-powered commands."""
        if self.args['--cmd']:
            return self._handle_cmd_lookup()
        if self.args['--sql']:
            return self._handle_sql_lookup()
        if self.args['--color-code']:
            return self._handle_color_code()
        if self.args['--port-lookup']:
            return self._handle_port_lookup()
        if self.args['--no-copy']:
            return self._handle_no_copy()
        return False

    def _route_tools(self) -> bool:
        """Route tool commands (encoding, generators, network, lookup)."""
        # Encoding
        if self.args['--base64-encode']:
            return self._handle_base64_encode()
        if self.args['--base64-decode']:
            return self._handle_base64_decode()
        # Generators
        if self.args['--generate-uuid']:
            return self._handle_generate_uuid()
        if self.args['--random-password'] is not None:
            return self._handle_random_password()
        if self.args['--regex-pattern']:
            return self._handle_regex_pattern()
        if self.args['--random-useragent']:
            return self._handle_random_useragent()
        if self.args['--timestamp-convert']:
            return self._handle_timestamp_convert()
        # Network
        if self.args['--get-ip']:
            return self._handle_get_ip()
        # Lookup
        if self.args['--lookup-http-code']:
            return self._handle_http_code_lookup()
        return False

    def _route_history(self) -> bool:
        """Route history management commands."""
        if self.args['--get-cmd']:
            return self._handle_get_cmd()
        if self.args['--get-last']:
            return self._handle_get_last()
        if self.args['--delete-cmd']:
            return self._handle_delete_cmd()
        if self.args['--delete-last-cmd']:
            return self._handle_delete_last_cmd()
        if self.args['--cmd-total']:
            return self._handle_cmd_total()
        if self.args['--clear-history']:
            return self._handle_clear_history()
        if self.args['--db-size']:
            return self._handle_db_size()
        return False

    def _route_configuration(self) -> bool:
        """Route configuration commands."""
        if self.args['--set-key']:
            return self._handle_set_key_legacy()
        if self.args['--get-key']:
            return self._handle_get_key_legacy()
        if self.args['--reset-config']:
            return self._handle_reset_config()
        return False

    def _route_info(self) -> bool:
        """Route info commands."""
        if self.args['--library-info']:
            return self._handle_library_info()
        if self.args['--version']:
            return self._handle_version()
        return False

    # ==================== Help ====================
    def _handle_help(self) -> bool:
        from chatcmd import print_colored_usage
        print_header()
        print_colored_usage()
        return True

    # ==================== Model Management ====================
    def _handle_list_models(self) -> bool:
        if os.environ.get('CHATCMD_JSON') == '1':
            models = []
            for provider in self.model_config.get_providers():
                for m in self.model_config.get_models_by_provider(provider):
                    models.append({
                        'name': m.name,
                        'display_name': m.display_name,
                        'provider': m.provider
                    })
            print(json.dumps({'models': models}))
        else:
            self.enhanced_lookup.list_available_models()
        return True

    def _handle_model_info(self) -> bool:
        model_name = self.args['--model-info']
        model_info = self.model_config.get_model_info(model_name)
        if model_info:
            if os.environ.get('CHATCMD_JSON') == '1':
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
        return True

    def _handle_current_model(self) -> bool:
        current_info = self.enhanced_lookup.get_current_model_info()
        if os.environ.get('CHATCMD_JSON') == '1':
            print(json.dumps({'current': current_info}))
        else:
            colored_print(f"\nCurrent Model: {current_info['model_display_name']} ({current_info['model_name']})", Colors.GREEN, bold=True)
            colored_print(f"Provider: {current_info['provider_name']}", Colors.BLUE)
            status_color = Colors.GREEN if current_info['provider_configured'] else Colors.RED
            colored_print(f"Configured: {'Yes' if current_info['provider_configured'] else 'No'}", status_color)
        return True

    def _handle_performance_stats(self) -> bool:
        stats = self.enhanced_lookup.get_performance_stats()
        if os.environ.get('CHATCMD_JSON') == '1':
            print(json.dumps({'stats': stats}))
        else:
            colored_print(f"\nPerformance Statistics (Last {DEFAULT_STATS_LOOKBACK_DAYS} days):", Colors.CYAN, bold=True)
            colored_print(f"Total Requests: {stats['total_requests']}", Colors.GREEN)
            colored_print(f"Successful: {stats['successful_requests']}", Colors.GREEN)
            colored_print(f"Failed: {stats['failed_requests']}", Colors.RED)
            colored_print(f"Average Response Time: {stats['average_response_time']}s", Colors.YELLOW)
            colored_print(f"Models Used: {', '.join(stats['models_used'])}", Colors.BLUE)
        return True

    def _handle_set_model_key(self) -> bool:
        provider = self.args['--set-model-key']
        self._set_provider_api_key(provider)
        return True

    def _handle_get_model_key(self) -> bool:
        provider = self.args['--get-model-key']
        self._get_provider_api_key(provider)
        return True

    def _handle_set_model(self) -> bool:
        model_name = self.args['--model']
        normalized = self.model_config.normalize_model_name(model_name) or model_name
        if self.enhanced_lookup.set_model(normalized):
            colored_print(f"Model set to: {normalized}", Colors.GREEN, bold=True)
        else:
            suggestion = self.model_config.suggest_model(model_name) or ""
            if suggestion:
                colored_print(f"Unknown model '{model_name}'. Did you mean '{suggestion}'?", Colors.YELLOW)
            else:
                colored_print(f"Failed to set model: {model_name}", Colors.RED)
        return True

    # ==================== AI-Powered Commands ====================
    def _ensure_provider_configured(self) -> None:
        """Ensure at least one AI provider is configured."""
        if not self._is_any_provider_configured():
            self._setup_initial_provider()

    def _handle_cmd_lookup(self) -> bool:
        self._ensure_provider_configured()
        selected_model = self._get_selected_model()
        self.enhanced_lookup.prompt(False, selected_model)
        return True

    def _handle_sql_lookup(self) -> bool:
        self._ensure_provider_configured()
        selected_model = self._get_selected_model()
        self.enhanced_lookup.prompt_sql(False, selected_model)
        return True

    def _handle_color_code(self) -> bool:
        self.enhanced_lookup.color_code()
        return True

    def _handle_port_lookup(self) -> bool:
        self.enhanced_lookup.port_lookup()
        return True

    # ==================== Encoding Tools ====================
    def _handle_base64_encode(self) -> bool:
        text = input("Text to encode: ")
        base64_encode(text)
        return True

    def _handle_base64_decode(self) -> bool:
        text = input("Base64 text to decode: ")
        base64_decode(text)
        return True

    # ==================== Generator Tools ====================
    def _handle_generate_uuid(self) -> bool:
        version = int(self.args['--generate-uuid'])
        generate_uuid(version)
        return True

    def _handle_random_password(self) -> bool:
        length_str = self.args['--random-password']
        try:
            length = int(length_str) if length_str else DEFAULT_PASSWORD_LENGTH
            length = max(MIN_PASSWORD_LENGTH, min(length, MAX_PASSWORD_LENGTH))
        except (ValueError, TypeError):
            length = DEFAULT_PASSWORD_LENGTH
        generate_password(length)
        return True

    def _handle_regex_pattern(self) -> bool:
        description = input("Regex description: ")
        generate_regex_pattern(description)
        return True

    def _handle_random_useragent(self) -> bool:
        generate_user_agent()
        return True

    def _handle_timestamp_convert(self) -> bool:
        format_type = self.args['--timestamp-convert']
        timestamp = input("Timestamp to convert: ")
        convert_timestamp(timestamp, format_type)
        return True

    # ==================== Network Tools ====================
    def _handle_get_ip(self) -> bool:
        get_public_ip()
        return True

    # ==================== Lookup Tools ====================
    def _handle_http_code_lookup(self) -> bool:
        lookup_http_code()
        return True

    # ==================== History Management ====================
    def _handle_get_cmd(self) -> bool:
        from chatcmd.commands import CMD
        CMD.get_cmd(self.cursor)
        return True

    def _handle_get_last(self) -> bool:
        from chatcmd.commands import CMD
        CMD.get_last_num_cmd(self.cursor, self.args['--get-last'])
        return True

    def _handle_delete_cmd(self) -> bool:
        from chatcmd.commands import CMD
        CMD.delete_cmd(self.conn, self.cursor)
        return True

    def _handle_delete_last_cmd(self) -> bool:
        from chatcmd.commands import CMD
        CMD.delete_last_num_cmd(self.conn, self.cursor, self.args['--delete-last-cmd'])
        return True

    def _handle_cmd_total(self) -> bool:
        from chatcmd.commands import CMD
        count = CMD.get_commands_count(self.cursor)
        colored_print(f'\nTotal of {count} commands\n', Colors.CYAN, bold=True)
        return True

    def _handle_clear_history(self) -> bool:
        from chatcmd.commands import CMD
        CMD.clear_history(self.conn, self.cursor)
        return True

    def _handle_db_size(self) -> bool:
        from chatcmd.commands import CMD
        CMD.get_db_size(self.db_manager.db_path)
        return True

    # ==================== Configuration ====================
    def _handle_set_key_legacy(self) -> bool:
        self.enhanced_api.ask_for_provider_api_key('openai')
        return True

    def _handle_get_key_legacy(self) -> bool:
        self._get_provider_api_key('openai')
        return True

    def _handle_reset_config(self) -> bool:
        auto_yes = os.environ.get('CHATCMD_YES') == '1'
        if not auto_yes:
            try:
                confirm = input("This will clear local config and stored API keys. Proceed? (y/N): ").strip().lower()
                if confirm not in ('y', 'yes'):
                    colored_print("Cancelled.", Colors.YELLOW)
                    return True
            except KeyboardInterrupt:
                colored_print("\nCancelled.", Colors.YELLOW)
                return True
        if self.enhanced_api.reset_configuration():
            colored_print("Configuration reset successfully.", Colors.GREEN, bold=True)
        else:
            colored_print("Failed to reset configuration.", Colors.RED)
        return True

    # ==================== Info ====================
    def _handle_library_info(self) -> bool:
        from chatcmd.helpers import Helpers
        Helpers.library_info()
        return True

    def _handle_version(self) -> bool:
        version = importlib.metadata.version('chatcmd')
        colored_print('ChatCMD ' + version, Colors.BRIGHT_GREEN, bold=True)
        return True

    # ==================== No-copy Mode ====================
    def _handle_no_copy(self) -> bool:
        selected_model = self._get_selected_model()
        if selected_model:
            self.enhanced_lookup.prompt(True, selected_model)
        else:
            self.enhanced_lookup.prompt(True)
        return True

    # ==================== Helper Methods ====================
    def _get_selected_model(self) -> Optional[str]:
        """Get selected model from args."""
        if self.args['--model']:
            return self.model_config.normalize_model_name(self.args['--model']) or self.args['--model']
        return None

    def _is_any_provider_configured(self) -> bool:
        """Check if any AI provider has an API key configured."""
        for provider in SUPPORTED_PROVIDERS:
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
                    '1': 'openai', '2': 'anthropic', '3': 'google',
                    '4': 'cohere', '5': 'ollama'
                }
                if choice in provider_map:
                    self._set_provider_api_key(provider_map[choice])
                    break
                else:
                    colored_print("Invalid choice. Please select 1-5.", Colors.RED)
            except KeyboardInterrupt:
                colored_print("\nSetup cancelled.", Colors.YELLOW)
                exit(0)

    def _set_provider_api_key(self, provider: str) -> None:
        """Set API key for a specific provider."""
        try:
            colored_print(f"\nEnter API key for {provider}: ", Colors.CYAN, bold=True)
            api_key = input()
            if self.enhanced_api.set_provider_api_key(provider, api_key):
                colored_print(f"\nAPI key for {provider} saved successfully.", Colors.GREEN, bold=True)
            else:
                colored_print(f"\nFailed to save API key for {provider}.", Colors.RED)
        except Exception as e:
            colored_print(f"Error setting API key: {e}", Colors.RED)

    def _get_provider_api_key(self, provider: str) -> None:
        """Get and display masked API key for a specific provider."""
        try:
            api_key = self.enhanced_api.get_provider_api_key(provider)
            if api_key:
                masked_key = self._mask_api_key(api_key)
                colored_print(f"\n{provider} API key: {masked_key}", Colors.GREEN)
            else:
                colored_print(f"\nNo API key found for {provider}", Colors.RED)
        except Exception as e:
            colored_print(f"Error getting API key: {e}", Colors.RED)

    @staticmethod
    def _mask_api_key(api_key: str) -> str:
        """Mask an API key for safe display."""
        if len(api_key) > API_KEY_MIN_LENGTH_FOR_MASK:
            return f"{api_key[:API_KEY_MASK_PREFIX_LENGTH]}...{api_key[-API_KEY_MASK_SUFFIX_LENGTH:]}"
        return "***masked***"
