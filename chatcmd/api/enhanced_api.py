"""
Enhanced API module for ChatCMD
Handles multiple AI provider API key management with secure storage
"""

from typing import Optional, Dict, Any
import os
import json
from pathlib import Path
from chatcmd.database.schema_manager import SchemaManager
from chatcmd.helpers.secure_storage import secure_storage


class EnhancedAPI:
    """Enhanced API management for multiple providers"""
    
    def __init__(self, db_manager: SchemaManager):
        self.db_manager = db_manager
        # Config file path (non-interactive configuration support)
        from chatcmd.helpers.platform_utils import platform_utils
        self.config_path = os.path.join(platform_utils.get_user_data_dir(), 'config.json')
    
    def get_provider_api_key(self, provider_name: str) -> Optional[str]:
        """
        Get API key for a specific provider from secure storage
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            API key string or None if not found
        """
        # 1) Environment variables (non-interactive)
        #    Supported forms: CHATCMD_<PROVIDER>_API_KEY, CHATCMD_API_KEY_<PROVIDER>
        candidates = [
            f"CHATCMD_{provider_name.upper()}_API_KEY",
            f"CHATCMD_API_KEY_{provider_name.upper()}"
        ]
        for env_key in candidates:
            if os.environ.get(env_key):
                return os.environ.get(env_key)

        # 2) Config file (non-interactive)
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                if isinstance(config, dict):
                    # Expected format: {"providers": {"openai": {"api_key": "..."}}}
                    providers = config.get('providers') or {}
                    provider_cfg = providers.get(provider_name) or {}
                    api_key = provider_cfg.get('api_key')
                    if api_key:
                        return api_key
        except Exception:
            # Silent fail, fall back to secure storage/database
            pass

        # 3) Secure storage first
        if secure_storage.is_available():
            api_key = secure_storage.get_api_key(provider_name)
            if api_key:
                return api_key
        
        # 4) Fallback to database storage
        provider_info = self.db_manager.get_provider(provider_name)
        if provider_info and provider_info['api_key']:
            return provider_info['api_key']
        return None
    
    def set_provider_api_key(self, provider_name: str, api_key: str) -> bool:
        """
        Set API key for a specific provider in secure storage
        
        Args:
            provider_name: Name of the provider
            api_key: API key to set
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Store in secure storage first
            if secure_storage.is_available():
                if not secure_storage.store_api_key(provider_name, api_key):
                    print(f"Warning: Could not store API key in secure storage for {provider_name}")
            
            # Also store in database for backward compatibility
            existing_provider = self.db_manager.get_provider(provider_name)
            if existing_provider:
                # Update existing provider
                return self.db_manager.update_provider_api_key(provider_name, api_key)
            else:
                # Add new provider
                provider_id = self.db_manager.add_provider(provider_name, api_key)
                saved = provider_id is not None

            # Also persist to config file for non-interactive usage
            try:
                Path(os.path.dirname(self.config_path)).mkdir(parents=True, exist_ok=True)
                config: Dict[str, Any] = {}
                if os.path.exists(self.config_path):
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f) or {}
                providers = config.setdefault('providers', {})
                providers.setdefault(provider_name, {})['api_key'] = api_key
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2)
            except Exception:
                pass

            return saved
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

    def reset_configuration(self) -> bool:
        """Safely clear config.json, secure/local stored keys, and DB provider keys."""
        try:
            # 1) Delete config.json
            try:
                if os.path.exists(self.config_path):
                    os.remove(self.config_path)
            except Exception:
                pass

            # 2) Delete secure storage keys and local encrypted files
            try:
                providers = self.db_manager.get_all_providers()
                for p in providers:
                    try:
                        secure_storage.delete_api_key(p['provider_name'])
                    except Exception:
                        continue
                # Attempt to delete local encrypted files used by fallback storage
                user_dir = platform_utils.get_user_data_dir()
                for fn in ['api_keys.enc', '.encryption_key']:
                    fpath = os.path.join(user_dir, fn)
                    try:
                        if os.path.exists(fpath):
                            os.remove(fpath)
                    except Exception:
                        continue
            except Exception:
                pass

            # 3) Clear DB provider api_key values
            try:
                providers = self.db_manager.get_all_providers()
                for p in providers:
                    # set to empty string to avoid NULL constraint differences
                    self.db_manager.update_provider_api_key(p['provider_name'], '')
            except Exception:
                pass

            return True
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