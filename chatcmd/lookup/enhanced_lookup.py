"""
Enhanced lookup module for ChatCMD
Supports multiple AI providers for CLI command generation
"""

import time
import pyperclip
import platform
from typing import Optional, Dict, Any
from chatcmd.config.provider_factory import ProviderFactory
from chatcmd.config.model_config import ModelConfig
from chatcmd.database.schema_manager import SchemaManager
from chatcmd.commands import CMD
from chatcmd.helpers import Helpers

cmd = CMD()
helpers = Helpers()


class EnhancedLookup:
    """Enhanced lookup class supporting multiple AI providers"""
    
    def __init__(self, db_manager: SchemaManager):
        self.db_manager = db_manager
        self.provider_factory = ProviderFactory()
        self.model_config = ModelConfig()
        self.performance_stats = {}
    
    def prompt(self, no_copy: bool = False, model_name: str = None):
        """
        Main prompt function for CLI command lookup
        
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
        
        # Get current model configuration
        current_config = self.db_manager.get_current_model()
        # Normalize model name to handle aliases/user variants
        selected_model = self.model_config.normalize_model_name(model_name or current_config['current_model']) or (model_name or current_config['current_model'])
        selected_provider = current_config['current_provider']
        
        # Get provider and validate (Ollama does not require API key)
        provider_info = self.db_manager.get_provider(selected_provider)
        if not provider_info:
            colored_print(f"Error: Provider '{selected_provider}' is not configured", Colors.RED, bold=True)
            return
        if selected_provider != 'ollama' and not provider_info['api_key']:
            colored_print(f"Error: No API key found for provider '{selected_provider}'", Colors.RED, bold=True)
            colored_print("Use --set-model-key to configure your API key", Colors.YELLOW)
            return
        
        # Create provider instance
        provider = self.provider_factory.create_provider(
            selected_model, 
            provider_info.get('api_key') or "",
            base_url=provider_info.get('base_url')
        )
        
        if not provider:
            colored_print(f"Error: Could not create provider for model '{selected_model}'", Colors.RED, bold=True)
            return
        
        # Validate API key for non-Ollama providers
        if selected_provider != 'ollama':
            if not provider.validate_api_key():
                colored_print(f"Error: Invalid API key for provider '{selected_provider}'", Colors.RED, bold=True)
                print("Use --set-model-key to update your API key")
                return
        
        # Get user prompt with proper loop instead of recursion
        while True:
            prompt = helpers.clear_input(input("Prompt: "))
            
            if prompt == 'exit':
                print('bye...')
                return
            if prompt != '':
                break
            print("Please enter a valid prompt or 'exit' to quit.")
        
        # Validate input
        if not helpers.validate_input(prompt.strip()):
            print("\nPlease enter a valid prompt.\n")
            return
        
        word_list = prompt.strip().split()
        if len(word_list) < 3:
            print("\nPlease type in more than two words.\n")
            return
        
        # Generate command
        colored_print("Looking up...\n", Colors.YELLOW)
        start_time = time.time()
        
        command = provider.generate_command(prompt)
        response_time = time.time() - start_time
        
        if command is not None:
            # Track usage statistics
            self._track_usage(provider_info['id'], selected_model, response_time, True)
            
            # Copy to clipboard if enabled
            if not no_copy:
                if platform.system() == "Linux":
                    helpers.copy_to_clipboard(command)
                else:
                    pyperclip.copy(command)
            
            # Clean and validate command
            command = helpers.clear_input(command)
            # Hardened sanitization: reject multi-line and dangerous operators unless explicitly enabled
            dangerous_tokens = [';', '&&', '||', '|', '>', '>>', '2>', '2>>']
            if '\n' in command:
                print('Error: Multi-line commands are disabled. Enable raw mode to allow.')
                return
            if any(tok in command for tok in dangerous_tokens):
                print('Error: Potentially dangerous command detected. Please refine your request.')
                return
            
            # Check for invalid responses
            if self._is_invalid_response(command):
                print('No command found for this request!')
                return
            
            # Add to history
            history = cmd.add_cmd(
                self.db_manager.conn, 
                self.db_manager.cursor, 
                prompt, 
                command.strip(),
                model_name=selected_model,
                provider_name=selected_provider
            )
            
            if not history:
                print("Error: Failed to add command to history")
            
            colored_print(" " + command.strip(), Colors.BRIGHT_GREEN, bold=True)
            print('')
        else:
            # Track failed usage
            self._track_usage(provider_info['id'], selected_model, response_time, False)
            print("Error: Could not generate command. Please try again.")
    
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
    
    def _is_invalid_response(self, command: str) -> bool:
        """Check if the response indicates no command was found"""
        if not command:
            return True
        
        command_lower = command.lower()
        invalid_phrases = [
            'there is no command',
            'no specific command',
            'not a command',
            'cannot find',
            'unable to',
            'sorry,',
            'i cannot',
            'i don\'t know',
            'no command exists',
            'command not found'
        ]
        
        for phrase in invalid_phrases:
            if phrase in command_lower:
                return True
        
        return False
    
    def list_available_models(self):
        """List all available AI models"""
        from chatcmd import Colors, colored_print
        
        colored_print("\nAvailable AI Models:\n", Colors.GOLD, bold=True)
        
        providers = self.model_config.get_providers()
        for provider in providers:
            colored_print(f"{provider.upper()}:", Colors.GREEN, bold=True)
            models = self.model_config.get_models_by_provider(provider)
            for model in models:
                status = "✓" if self._is_model_available(model.name, provider) else "✗"
                status_color = Colors.GREEN if self._is_model_available(model.name, provider) else Colors.GREEN
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
    
    def prompt_sql(self, no_copy: bool = False, model_name: str = None):
        """
        SQL query generation prompt function
        
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
        
        # Get current model configuration
        current_config = self.db_manager.get_current_model()
        selected_model = self.model_config.normalize_model_name(model_name or current_config['current_model']) or (model_name or current_config['current_model'])
        selected_provider = current_config['current_provider']
        
        # Get provider and validate (Ollama does not require API key)
        provider_info = self.db_manager.get_provider(selected_provider)
        if not provider_info:
            colored_print(f"Error: Provider '{selected_provider}' is not configured", Colors.RED, bold=True)
            return
        if selected_provider != 'ollama' and not provider_info['api_key']:
            colored_print(f"Error: No API key found for provider '{selected_provider}'", Colors.RED, bold=True)
            colored_print("Use --set-model-key to configure your API key", Colors.YELLOW)
            return
        
        # Create provider instance
        provider = self.provider_factory.create_provider(
            selected_model, 
            provider_info.get('api_key') or "",
            base_url=provider_info.get('base_url')
        )
        
        if not provider:
            colored_print(f"Error: Could not create provider for model '{selected_model}'", Colors.RED, bold=True)
            return
        
        # Validate API key for non-Ollama providers
        if selected_provider != 'ollama':
            if not provider.validate_api_key():
                colored_print(f"Error: Invalid API key for provider '{selected_provider}'", Colors.RED, bold=True)
                print("Use --set-model-key to update your API key")
                return
        
        # Get user prompt with proper loop instead of recursion
        while True:
            prompt = helpers.clear_input(input("SQL Query Prompt: "))
            
            if prompt == 'exit':
                print('bye...')
                return
            if prompt != '':
                break
            print("Please enter a valid prompt or 'exit' to quit.")
        
        # Validate input
        if not helpers.validate_input(prompt.strip()):
            print("\nPlease enter a valid prompt.\n")
            return
        
        word_list = prompt.strip().split()
        if len(word_list) < 3:
            print("\nPlease type in more than two words.\n")
            return
        
        # Generate SQL query
        colored_print("Writing SQL query...\n", Colors.YELLOW)
        start_time = time.time()
        
        sql_query = provider.generate_sql_query(prompt)
        response_time = time.time() - start_time
        
        if sql_query is not None:
            # Track usage statistics
            self._track_usage(provider_info['id'], selected_model, response_time, True)
            
            # Copy to clipboard if enabled
            if not no_copy:
                if platform.system() == "Linux":
                    helpers.copy_to_clipboard(sql_query)
                else:
                    pyperclip.copy(sql_query)
            
            # Clean and validate SQL query
            sql_query = helpers.clear_input(sql_query)
            # Harden SQL: reject DDL/DML unless user requested explicitly in prompt
            upper_query = sql_query.strip().upper()
            forbidden_sql = ['DROP ', 'TRUNCATE ', 'ALTER ', 'DELETE ', 'UPDATE ']
            if any(keyword in upper_query for keyword in forbidden_sql) and 'SELECT' not in upper_query:
                print('Error: Destructive SQL is blocked. Ask explicitly with clear intent to proceed.')
                return
            
            # Check for invalid responses
            if self._is_invalid_sql_response(sql_query):
                print('No SQL query found for this request!')
                return
            
            # Add to history
            history = cmd.add_cmd(
                self.db_manager.conn, 
                self.db_manager.cursor, 
                prompt, 
                sql_query.strip(),
                model_name=selected_model,
                provider_name=selected_provider
            )
            
            if not history:
                print("Error: Failed to add SQL query to history")
            
            colored_print(" " + sql_query.strip(), Colors.BRIGHT_GREEN, bold=True)
            print('')
        else:
            # Track failed usage
            self._track_usage(provider_info['id'], selected_model, response_time, False)
            print("Error: Could not generate SQL query. Please try again.")
    
    def _is_invalid_sql_response(self, sql_query: str) -> bool:
        """Check if the response indicates no SQL query was found"""
        if not sql_query:
            return True
        
        query_lower = sql_query.lower()
        invalid_phrases = [
            'there is no query',
            'no specific query',
            'not a query',
            'cannot find',
            'unable to',
            'sorry,',
            'i cannot',
            'i don\'t know',
            'no query exists',
            'query not found'
        ]
        
        for phrase in invalid_phrases:
            if phrase in query_lower:
                return True
        
        return False

    def get_performance_stats(self, days: int = 7) -> Dict[str, Any]:
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

    def port_lookup(self):
        """Lookup a port using the currently selected model/provider"""
        # Get current model configuration
        current_config = self.db_manager.get_current_model()
        selected_model = current_config['current_model']
        selected_provider = current_config['current_provider']

        # Get provider and validate (Ollama does not require API key)
        provider_info = self.db_manager.get_provider(selected_provider)
        if not provider_info:
            colored_print(f"Error: Provider '{selected_provider}' is not configured", Colors.RED, bold=True)
            return
        if selected_provider != 'ollama' and not provider_info['api_key']:
            colored_print(f"Error: No API key found for provider '{selected_provider}'", Colors.RED, bold=True)
            colored_print("Use --set-model-key to configure your API key", Colors.YELLOW)
            return

        # Create provider instance
        provider = self.provider_factory.create_provider(
            selected_model,
            provider_info.get('api_key') or "",
            base_url=provider_info.get('base_url')
        )
        if not provider:
            colored_print(f"Error: Could not create provider for model '{selected_model}'", Colors.RED, bold=True)
            return

        # Validate API key for non-Ollama providers
        if selected_provider != 'ollama':
            if not provider.validate_api_key():
                colored_print(f"Error: Invalid API key for provider '{selected_provider}'", Colors.RED, bold=True)
                print("Use --set-model-key to update your API key")
                return

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

    def color_code(self):
        """Get color HEX code using the currently selected model/provider"""
        # Get current model configuration
        current_config = self.db_manager.get_current_model()
        selected_model = current_config['current_model']
        selected_provider = current_config['current_provider']

        # Get provider and validate (Ollama does not require API key)
        provider_info = self.db_manager.get_provider(selected_provider)
        if not provider_info:
            colored_print(f"Error: Provider '{selected_provider}' is not configured", Colors.RED, bold=True)
            return
        if selected_provider != 'ollama' and not provider_info['api_key']:
            colored_print(f"Error: No API key found for provider '{selected_provider}'", Colors.RED, bold=True)
            colored_print("Use --set-model-key to configure your API key", Colors.YELLOW)
            return

        # Create provider instance
        provider = self.provider_factory.create_provider(
            selected_model,
            provider_info.get('api_key') or "",
            base_url=provider_info.get('base_url')
        )
        if not provider:
            colored_print(f"Error: Could not create provider for model '{selected_model}'", Colors.RED, bold=True)
            return

        # Validate API key for non-Ollama providers
        if selected_provider != 'ollama':
            if not provider.validate_api_key():
                colored_print(f"Error: Invalid API key for provider '{selected_provider}'", Colors.RED, bold=True)
                print("Use --set-model-key to update your API key")
                return

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