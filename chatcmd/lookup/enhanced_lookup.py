"""
Enhanced lookup module for ChatCMD
Supports multiple AI providers for CLI command generation
"""

import time
import pyperclip
import platform
from typing import Optional, Dict, Any, Tuple
from chatcmd.config.provider_factory import ProviderFactory
from chatcmd.config.model_config import ModelConfig
from chatcmd.database.schema_manager import SchemaManager
from chatcmd.commands import CMD
from chatcmd.helpers import Helpers
from chatcmd.constants import MIN_PROMPT_WORDS, DEFAULT_STATS_LOOKBACK_DAYS

cmd = CMD()
helpers = Helpers()

# Common phrases indicating invalid AI responses
INVALID_RESPONSE_PHRASES = [
    'there is no',
    'no specific',
    'not a command',
    'not a query',
    'cannot find',
    'unable to',
    'sorry',
    'i cannot',
    "i don't know",
    'not found',
    'no command exists',
    'no query exists',
    'command not found',
]


class EnhancedLookup:
    """Enhanced lookup class supporting multiple AI providers"""

    def __init__(self, db_manager: SchemaManager):
        self.db_manager = db_manager
        self.provider_factory = ProviderFactory()
        self.model_config = ModelConfig()
        self.performance_stats = {}

    def _get_validated_provider(self, model_name: Optional[str] = None) -> Optional[Tuple[Any, str, str, Dict]]:
        """
        Get and validate AI provider for the current/specified model.

        Args:
            model_name: Optional specific model to use

        Returns:
            Tuple of (provider, selected_model, selected_provider, provider_info) or None if validation fails
        """
        from chatcmd import Colors, colored_print

        # Get current model configuration
        current_config = self.db_manager.get_current_model()
        selected_model = self.model_config.normalize_model_name(
            model_name or current_config['current_model']
        ) or (model_name or current_config['current_model'])
        selected_provider = current_config['current_provider']

        # Get provider and validate
        provider_info = self.db_manager.get_provider(selected_provider)
        if not provider_info:
            colored_print(f"Error: Provider '{selected_provider}' is not configured", Colors.RED, bold=True)
            return None

        # Ollama doesn't require API key
        if selected_provider != 'ollama' and not provider_info['api_key']:
            colored_print(f"Error: No API key found for provider '{selected_provider}'", Colors.RED, bold=True)
            colored_print("Use --set-model-key to configure your API key", Colors.YELLOW)
            return None

        # Create provider instance
        provider = self.provider_factory.create_provider(
            selected_model,
            provider_info.get('api_key') or "",
            base_url=provider_info.get('base_url')
        )

        if not provider:
            colored_print(f"Error: Could not create provider for model '{selected_model}'", Colors.RED, bold=True)
            return None

        # Validate API key for non-Ollama providers
        if selected_provider != 'ollama' and not provider.validate_api_key():
            colored_print(f"Error: Invalid API key for provider '{selected_provider}'", Colors.RED, bold=True)
            print("Use --set-model-key to update your API key")
            return None

        return provider, selected_model, selected_provider, provider_info

    def _get_user_prompt(self, prompt_text: str = "Prompt: ") -> Optional[str]:
        """
        Get and validate user input prompt.

        Args:
            prompt_text: Text to display when prompting user

        Returns:
            Validated prompt string or None if user exits
        """
        while True:
            prompt = helpers.clear_input(input(prompt_text))

            if prompt == 'exit':
                print('bye...')
                return None
            if prompt != '':
                break
            print("Please enter a valid prompt or 'exit' to quit.")

        # Validate input
        if not helpers.validate_input(prompt.strip()):
            print("\nPlease enter a valid prompt.\n")
            return None

        prompt_words = prompt.strip().split()
        if len(prompt_words) < MIN_PROMPT_WORDS:
            print(f"\nPlease type in more than {MIN_PROMPT_WORDS - 1} words.\n")
            return None

        return prompt

    def _is_invalid_response(self, response: str) -> bool:
        """Check if the AI response indicates no valid result was found."""
        if not response:
            return True

        response_lower = response.lower()
        return any(phrase in response_lower for phrase in INVALID_RESPONSE_PHRASES)

    def _copy_to_clipboard(self, text: str, no_copy: bool) -> None:
        """Copy text to clipboard if enabled."""
        if no_copy:
            return
        if platform.system() == "Linux":
            helpers.copy_to_clipboard(text)
        else:
            pyperclip.copy(text)
    
    def prompt(self, no_copy: bool = False, model_name: Optional[str] = None) -> None:
        """
        Main prompt function for CLI command lookup.

        Args:
            no_copy: Whether to disable clipboard copying
            model_name: Specific model to use (optional)
        """
        from chatcmd import Colors, colored_print

        colored_print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Lookup CLI Commands
        """, Colors.BRIGHT_GREEN)

        # Get validated provider
        result = self._get_validated_provider(model_name)
        if not result:
            return
        provider, selected_model, selected_provider, provider_info = result

        # Get user prompt
        prompt = self._get_user_prompt("Prompt: ")
        if not prompt:
            return

        # Generate command
        colored_print("Looking up...\n", Colors.YELLOW)
        start_time = time.time()
        command = provider.generate_command(prompt)
        response_time = time.time() - start_time

        if command is None:
            self._track_usage(provider_info['id'], selected_model, response_time, False)
            print("Error: Could not generate command. Please try again.")
            return

        # Track successful usage
        self._track_usage(provider_info['id'], selected_model, response_time, True)

        # Clean and validate command
        command = helpers.clear_input(command)

        # Security: Reject dangerous commands
        if not self._validate_command_safety(command):
            return

        # Check for invalid responses
        if self._is_invalid_response(command):
            print('No command found for this request!')
            return

        # Copy to clipboard after validation
        self._copy_to_clipboard(command, no_copy)

        # Add to history
        if not cmd.add_cmd(
            self.db_manager.conn,
            self.db_manager.cursor,
            prompt,
            command.strip(),
            model_name=selected_model,
            provider_name=selected_provider
        ):
            print("Error: Failed to add command to history")

        colored_print(" " + command.strip(), Colors.BRIGHT_GREEN, bold=True)
        print('')

    def _validate_command_safety(self, command: str) -> bool:
        """
        Validate command for security issues.

        Args:
            command: Command string to validate

        Returns:
            True if safe, False if dangerous
        """
        # Dangerous tokens including unicode variants
        dangerous_tokens = [
            ';', '&&', '||', '|', '>', '>>', '2>', '2>>',
            '`', '$(', '${',          # Command substitution
            '\x00', '\r',             # Null byte and carriage return injection
            '<<',                      # Here-doc
            '\uff1b', '\uff06',        # Unicode variants of ; and &
        ]

        # Reject multi-line commands
        if '\n' in command:
            print('Error: Multi-line commands are disabled.')
            return False

        # Reject dangerous tokens
        for tok in dangerous_tokens:
            if tok in command:
                print('Error: Potentially dangerous command detected. Please refine your request.')
                return False

        return True
    
    def _track_usage(self, provider_id: int, model_name: str, response_time: float, success: bool):
        """Track usage statistics"""
        try:
            self.db_manager.add_usage_stat(
                provider_id=provider_id,
                model_name=model_name,
                tokens_used=0,  # We don't track tokens for now
                response_time=response_time,
                success=success
            )
        except Exception as e:
            print(f"Warning: Could not track usage: {e}")
    
    def list_available_models(self) -> None:
        """List all available AI models."""
        from chatcmd import Colors, colored_print

        colored_print("\nAvailable AI Models:\n", Colors.GOLD, bold=True)

        providers = self.model_config.get_providers()
        for provider in providers:
            colored_print(f"{provider.upper()}:", Colors.GREEN, bold=True)
            models = self.model_config.get_models_by_provider(provider)
            for model in models:
                is_available = self._is_model_available(model.name, provider)
                status = "✓" if is_available else "✗"
                status_color = Colors.GREEN if is_available else Colors.RED
                colored_print(f"  {status} {model.display_name} ({model.name})", status_color)
            print()
    
    def _is_model_available(self, model_name: str, provider_name: str) -> bool:
        """Check if a model is available

        For Ollama, availability is based on provider config only (no API key required).
        For other providers, requires an API key.
        """
        provider_info = self.db_manager.get_provider(provider_name)
        if not provider_info:
            return False
        if provider_name == 'ollama':
            return True
        return provider_info['api_key'] is not None
    
    def set_model(self, model_name: str) -> bool:
        """
        Set the current AI model
        
        Args:
            model_name: Name of the model to set
            
        Returns:
            True if successful, False otherwise
        """
        if not self.model_config.is_model_supported(model_name):
            print(f"Error: Model '{model_name}' is not supported")
            return False
        
        model_info = self.model_config.get_model_info(model_name)
        provider_info = self.db_manager.get_provider(model_info.provider)
        
        if not provider_info:
            print(f"Error: Provider '{model_info.provider}' is not configured")
            return False
        if model_info.provider != 'ollama' and not provider_info['api_key']:
            print(f"Error: No API key configured for provider '{model_info.provider}'")
            print(f"Use --set-model-key {model_info.provider} to configure your API key")
            return False
        
        success = self.db_manager.set_current_model(model_name, model_info.provider)
        if success:
            print(f"Current model set to: {model_info.display_name}")
        else:
            print("Error: Failed to set current model")
        
        return success
    
    def get_current_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        current_config = self.db_manager.get_current_model()
        model_info = self.model_config.get_model_info(current_config['current_model'])
        provider_info = self.db_manager.get_provider(current_config['current_provider'])
        
        return {
            'model_name': current_config['current_model'],
            'model_display_name': model_info.display_name if model_info else 'Unknown',
            'provider_name': current_config['current_provider'],
            'provider_configured': provider_info is not None and provider_info['api_key'] is not None
        }
    
    def prompt_sql(self, no_copy: bool = False, model_name: Optional[str] = None) -> None:
        """
        SQL query generation prompt function.

        Args:
            no_copy: Whether to disable clipboard copying
            model_name: Specific model to use (optional)
        """
        from chatcmd import Colors, colored_print

        colored_print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Write SQL Queries
        """, Colors.BRIGHT_GREEN)

        # Get validated provider
        result = self._get_validated_provider(model_name)
        if not result:
            return
        provider, selected_model, selected_provider, provider_info = result

        # Get user prompt
        prompt = self._get_user_prompt("SQL Query Prompt: ")
        if not prompt:
            return

        # Generate SQL query
        colored_print("Writing SQL query...\n", Colors.YELLOW)
        start_time = time.time()
        sql_query = provider.generate_sql_query(prompt)
        response_time = time.time() - start_time

        if sql_query is None:
            self._track_usage(provider_info['id'], selected_model, response_time, False)
            print("Error: Could not generate SQL query. Please try again.")
            return

        # Track successful usage
        self._track_usage(provider_info['id'], selected_model, response_time, True)

        # Clean and validate SQL query
        sql_query = helpers.clear_input(sql_query)

        # Security: Reject destructive SQL
        if not self._validate_sql_safety(sql_query):
            return

        # Check for invalid responses
        if self._is_invalid_response(sql_query):
            print('No SQL query found for this request!')
            return

        # Copy to clipboard after validation
        self._copy_to_clipboard(sql_query, no_copy)

        # Add to history
        if not cmd.add_cmd(
            self.db_manager.conn,
            self.db_manager.cursor,
            prompt,
            sql_query.strip(),
            model_name=selected_model,
            provider_name=selected_provider
        ):
            print("Error: Failed to add SQL query to history")

        colored_print(" " + sql_query.strip(), Colors.BRIGHT_GREEN, bold=True)
        print('')

    def _validate_sql_safety(self, sql_query: str) -> bool:
        """
        Validate SQL query for destructive operations.

        Args:
            sql_query: SQL query to validate

        Returns:
            True if safe, False if destructive
        """
        upper_query = sql_query.strip().upper()
        forbidden_sql = ['DROP ', 'TRUNCATE ', 'ALTER ', 'DELETE ', 'UPDATE ']

        if any(keyword in upper_query for keyword in forbidden_sql) and 'SELECT' not in upper_query:
            print('Error: Destructive SQL is blocked. Ask explicitly with clear intent to proceed.')
            return False

        return True

    def get_performance_stats(self, days: int = DEFAULT_STATS_LOOKBACK_DAYS) -> Dict[str, Any]:
        """Get performance statistics for the last N days"""
        stats = self.db_manager.get_usage_stats(days)
        
        if not stats:
            return {
                'total_requests': 0,
                'successful_requests': 0,
                'failed_requests': 0,
                'average_response_time': 0,
                'models_used': []
            }
        
        total_requests = len(stats)
        successful_requests = sum(1 for stat in stats if stat['success'])
        failed_requests = total_requests - successful_requests
        
        response_times = [stat['response_time'] for stat in stats if stat['response_time']]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        models_used = list(set(f"{stat['provider_name']}/{stat['model_name']}" for stat in stats))
        
        return {
            'total_requests': total_requests,
            'successful_requests': successful_requests,
            'failed_requests': failed_requests,
            'average_response_time': round(average_response_time, 2),
            'models_used': models_used
        }

    def port_lookup(self) -> None:
        """Lookup a port using the currently selected model/provider."""
        # Get validated provider
        result = self._get_validated_provider()
        if not result:
            return
        provider, selected_model, selected_provider, provider_info = result

        # Prompt user for port
        prompt_value = helpers.clear_input(input("Port: "))
        if not prompt_value:
            print("Please enter a valid port.")
            return

        # Ask model for port info
        print("Looking up...\n")
        start_time = time.time()
        query = f"Provide the common service name and protocol for port {prompt_value}. Return concise answer only."
        response = provider.generate_command(query)
        response_time = time.time() - start_time

        # Track usage
        self._track_usage(provider_info['id'], selected_model, response_time, bool(response))

        if response:
            print(response)
        else:
            print("Error: Could not retrieve port information.")

    def color_code(self) -> None:
        """Get color HEX code using the currently selected model/provider."""
        # Get validated provider
        result = self._get_validated_provider()
        if not result:
            return
        provider, selected_model, selected_provider, provider_info = result

        # Prompt user for color description
        prompt_value = helpers.clear_input(input("Color: "))
        if not prompt_value:
            print("Please enter a valid color description.")
            return

        # Ask model for HEX code
        print("Getting color code...\n")
        start_time = time.time()
        query = f"What is the HEX code for this color? Return the hex code only: {prompt_value}"
        response = provider.generate_command(query)
        response_time = time.time() - start_time

        # Track usage
        self._track_usage(provider_info['id'], selected_model, response_time, bool(response))

        if response:
            print(response.strip())
        else:
            print("Error: Could not retrieve color code.")