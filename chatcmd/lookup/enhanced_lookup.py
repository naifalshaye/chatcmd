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
        print("""

         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Lookup CLI Commands
        """)
        
        # Get current model configuration
        current_config = self.db_manager.get_current_model()
        selected_model = model_name or current_config['current_model']
        selected_provider = current_config['current_provider']
        
        # Get provider and validate
        provider_info = self.db_manager.get_provider(selected_provider)
        if not provider_info or not provider_info['api_key']:
            print(f"Error: No API key found for provider '{selected_provider}'")
            print("Use --set-model-key to configure your API key")
            return
        
        # Create provider instance
        provider = self.provider_factory.create_provider(
            selected_model, 
            provider_info['api_key'],
            base_url=provider_info.get('base_url')
        )
        
        if not provider:
            print(f"Error: Could not create provider for model '{selected_model}'")
            return
        
        # Validate API key
        if not provider.validate_api_key():
            print(f"Error: Invalid API key for provider '{selected_provider}'")
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
        print("Looking up...\n")
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
            
            print(" " + command.strip())
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
        print("\nAvailable AI Models:\n")
        
        providers = self.model_config.get_providers()
        for provider in providers:
            print(f"{provider.upper()}:")
            models = self.model_config.get_models_by_provider(provider)
            for model in models:
                status = "✓" if self._is_model_available(model.name, provider) else "✗"
                print(f"  {status} {model.display_name} ({model.name})")
            print()
    
    def _is_model_available(self, model_name: str, provider_name: str) -> bool:
        """Check if a model is available (has API key configured)"""
        provider_info = self.db_manager.get_provider(provider_name)
        return provider_info is not None and provider_info['api_key'] is not None
    
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
        
        if not provider_info or not provider_info['api_key']:
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