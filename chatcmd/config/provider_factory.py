"""
Factory for creating AI providers
Handles instantiation of different AI model providers
"""

from typing import Optional, Dict, Any
from chatcmd.providers.base import BaseAIProvider
from chatcmd.providers.openai_provider import OpenAIProvider
from chatcmd.providers.anthropic_provider import AnthropicProvider
from chatcmd.providers.google_provider import GoogleProvider
from chatcmd.providers.cohere_provider import CohereProvider
from chatcmd.providers.ollama_provider import OllamaProvider
from chatcmd.config.model_config import ModelConfig


class ProviderFactory:
    """Factory for creating AI providers"""
    
    def __init__(self):
        self.model_config = ModelConfig()
        self._provider_cache = {}
    
    def create_provider(self, model_name: str, api_key: str, **kwargs) -> Optional[BaseAIProvider]:
        """
        Create an AI provider for the specified model
        
        Args:
            model_name: Name of the AI model
            api_key: API key for the provider
            **kwargs: Additional configuration parameters
            
        Returns:
            AI provider instance or None if creation fails
        """
        model_info = self.model_config.get_model_info(model_name)
        if not model_info:
            return None
        
        # Check cache first
        cache_key = f"{model_name}_{api_key[:10]}"
        if cache_key in self._provider_cache:
            return self._provider_cache[cache_key]
        
        provider = None
        
        try:
            if model_info.provider == 'openai':
                provider = OpenAIProvider(api_key, model_name=model_name, **kwargs)
            elif model_info.provider == 'anthropic':
                provider = AnthropicProvider(api_key, model_name=model_name, **kwargs)
            elif model_info.provider == 'google':
                provider = GoogleProvider(api_key, model_name=model_name, **kwargs)
            elif model_info.provider == 'cohere':
                provider = CohereProvider(api_key, model_name=model_name, **kwargs)
            elif model_info.provider == 'ollama':
                provider = OllamaProvider(api_key, model_name=model_name, **kwargs)
            else:
                return None
            
            # Cache the provider
            if provider:
                self._provider_cache[cache_key] = provider
            
            return provider
            
        except Exception as e:
            print(f"Error creating provider for {model_name}: {e}")
            return None
    
    def get_provider_for_model(self, model_name: str, api_keys: Dict[str, str]) -> Optional[BaseAIProvider]:
        """
        Get provider for a model using stored API keys
        
        Args:
            model_name: Name of the AI model
            api_keys: Dictionary of provider -> API key mappings
            
        Returns:
            AI provider instance or None if not available
        """
        model_info = self.model_config.get_model_info(model_name)
        if not model_info:
            return None
        
        api_key = api_keys.get(model_info.provider)
        if not api_key:
            return None
        
        return self.create_provider(model_name, api_key)
    
    def clear_cache(self):
        """Clear the provider cache"""
        self._provider_cache.clear()
    
    def get_supported_providers(self) -> list:
        """Get list of supported providers"""
        return self.model_config.get_providers()
    
    def get_models_for_provider(self, provider: str) -> list:
        """Get models available for a specific provider"""
        return self.model_config.get_models_by_provider(provider)