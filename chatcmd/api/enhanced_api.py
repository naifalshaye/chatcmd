"""
Enhanced API module for ChatCMD
Handles multiple AI provider API key management
"""

from typing import Optional, Dict, Any
from chatcmd.database.schema_manager import SchemaManager


class EnhancedAPI:
    """Enhanced API management for multiple providers"""
    
    def __init__(self, db_manager: SchemaManager):
        self.db_manager = db_manager
    
    def get_provider_api_key(self, provider_name: str) -> Optional[str]:
        """
        Get API key for a specific provider
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            API key string or None if not found
        """
        provider_info = self.db_manager.get_provider(provider_name)
        if provider_info and provider_info['api_key']:
            return provider_info['api_key']
        return None
    
    def set_provider_api_key(self, provider_name: str, api_key: str) -> bool:
        """
        Set API key for a specific provider
        
        Args:
            provider_name: Name of the provider
            api_key: API key to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Check if provider exists
            existing_provider = self.db_manager.get_provider(provider_name)
            if existing_provider:
                # Update existing provider
                return self.db_manager.update_provider_api_key(provider_name, api_key)
            else:
                # Add new provider
                provider_id = self.db_manager.add_provider(provider_name, api_key)
                return provider_id is not None
        except Exception as e:
            print(f"Error setting API key for {provider_name}: {e}")
            return False
    
    def validate_provider_api_key(self, provider_name: str, api_key: str) -> bool:
        """
        Validate API key for a specific provider
        
        Args:
            provider_name: Name of the provider
            api_key: API key to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            from chatcmd.config.provider_factory import ProviderFactory
            from chatcmd.config.model_config import ModelConfig
            
            factory = ProviderFactory()
            model_config = ModelConfig()
            
            # Get a model for this provider
            models = model_config.get_models_by_provider(provider_name)
            if not models:
                return False
            
            # Test with the first available model
            test_model = models[0].name
            provider = factory.create_provider(test_model, api_key)
            
            if provider:
                return provider.validate_api_key()
            
            return False
        except Exception:
            return False
    
    def get_all_providers(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all configured providers
        
        Returns:
            Dictionary of provider information
        """
        providers = self.db_manager.get_all_providers()
        result = {}
        
        for provider in providers:
            result[provider['provider_name']] = {
                'id': provider['id'],
                'api_key_configured': provider['api_key'] is not None,
                'base_url': provider['base_url'],
                'is_active': provider['is_active']
            }
        
        return result
    
    def ask_for_provider_api_key(self, provider_name: str) -> Optional[str]:
        """
        Prompt user for API key for a specific provider
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            API key string or None if cancelled
        """
        try:
            while True:
                api_key = input(f"\nEnter API key for {provider_name}: ")
                if not api_key.strip():
                    print("API key cannot be empty. Try again or press Ctrl+C to cancel.")
                    continue
                
                # Validate the API key
                if self.validate_provider_api_key(provider_name, api_key):
                    # Save the API key
                    if self.set_provider_api_key(provider_name, api_key):
                        print(f"\n{provider_name} API key saved successfully.")
                        return api_key
                    else:
                        print(f"Failed to save API key for {provider_name}. Try again.")
                        continue
                else:
                    print(f"Invalid API key for {provider_name}. Please check and try again.")
                    continue
        except KeyboardInterrupt:
            print("\nCancelled.")
            return None
        except Exception as e:
            print(f"Error getting API key: {e}")
            return None
    
    def get_current_provider_info(self) -> Optional[Dict[str, Any]]:
        """
        Get current provider information
        
        Returns:
            Current provider info or None
        """
        current_config = self.db_manager.get_current_model()
        provider_name = current_config['current_provider']
        
        provider_info = self.db_manager.get_provider(provider_name)
        if provider_info:
            return {
                'provider_name': provider_name,
                'api_key_configured': provider_info['api_key'] is not None,
                'base_url': provider_info['base_url'],
                'is_active': provider_info['is_active']
            }
        
        return None