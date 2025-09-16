"""
Model configuration management for ChatCMD
Handles AI model selection and settings
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import difflib


@dataclass
class ModelInfo:
    """Information about an AI model"""
    name: str
    display_name: str
    provider: str
    max_tokens: int = 100
    temperature: float = 0.7
    cost_per_token: Optional[float] = None
    description: str = ""


class ModelConfig:
    """Configuration manager for AI models"""
    
    # Common aliases to normalize user-provided model names to canonical keys
    # e.g., "llama-3.2-3b" -> "llama3.2:3b"
    ALIASES: Dict[str, str] = {
        # OpenAI
        'gpt4': 'gpt-4',
        'gpt-4o': 'gpt-4',
        'gpt3.5': 'gpt-3.5-turbo',
        'gpt-3.5': 'gpt-3.5-turbo',
        # Anthropic
        'claude-haiku': 'claude-3-haiku',
        'claude-sonnet': 'claude-3-sonnet',
        'claude-opus': 'claude-3-opus',
        # Google
        'gemini': 'gemini-pro',
        # Cohere
        'command-light': 'command-light',
        'command-lightnight': 'command-light',
        # Ollama - Llama 3.2 3B
        'llama-3.2-3b': 'llama3.2:3b',
        'llama3_2_3b': 'llama3.2:3b',
        'llama32-3b': 'llama3.2:3b',
        'llama3.2-3b': 'llama3.2:3b',
    }

    # Supported models configuration
    SUPPORTED_MODELS = {
        # OpenAI Models
        'gpt-3.5-turbo': ModelInfo(
            name='gpt-3.5-turbo',
            display_name='GPT-3.5 Turbo',
            provider='openai',
            max_tokens=100,
            temperature=0.7,
            description='Fast and efficient for CLI commands'
        ),
        'gpt-4': ModelInfo(
            name='gpt-4',
            display_name='GPT-4',
            provider='openai',
            max_tokens=100,
            temperature=0.7,
            description='Most capable model for complex commands'
        ),
        'gpt-4-turbo': ModelInfo(
            name='gpt-4-turbo',
            display_name='GPT-4 Turbo',
            provider='openai',
            max_tokens=100,
            temperature=0.7,
            description='Latest GPT-4 with improved performance'
        ),
        
        # Anthropic Models
        'claude-3-haiku': ModelInfo(
            name='claude-3-haiku-20240307',
            display_name='Claude 3 Haiku',
            provider='anthropic',
            max_tokens=100,
            temperature=0.7,
            description='Fast and efficient Claude model'
        ),
        'claude-3-sonnet': ModelInfo(
            name='claude-3-sonnet-20240229',
            display_name='Claude 3 Sonnet',
            provider='anthropic',
            max_tokens=100,
            temperature=0.7,
            description='Balanced Claude model for most tasks'
        ),
        'claude-3-opus': ModelInfo(
            name='claude-3-opus-20240229',
            display_name='Claude 3 Opus',
            provider='anthropic',
            max_tokens=100,
            temperature=0.7,
            description='Most capable Claude model'
        ),
        
        # Google Models
        'gemini-pro': ModelInfo(
            name='gemini-pro',
            display_name='Gemini Pro',
            provider='google',
            max_tokens=100,
            temperature=0.7,
            description='Google\'s advanced language model'
        ),
        
        # Cohere Models
        'command': ModelInfo(
            name='command',
            display_name='Cohere Command',
            provider='cohere',
            max_tokens=100,
            temperature=0.7,
            description='Cohere\'s instruction-following model'
        ),
        'command-light': ModelInfo(
            name='command-light',
            display_name='Cohere Command Light',
            provider='cohere',
            max_tokens=100,
            temperature=0.7,
            description='Faster Cohere model for simple tasks'
        ),
        
        # Ollama Models (Local)
        'llama2': ModelInfo(
            name='llama2',
            display_name='Llama 2 (Local)',
            provider='ollama',
            max_tokens=100,
            temperature=0.7,
            description='Local Llama 2 model via Ollama'
        ),
        'codellama': ModelInfo(
            name='codellama',
            display_name='Code Llama (Local)',
            provider='ollama',
            max_tokens=100,
            temperature=0.7,
            description='Local Code Llama model for coding tasks'
        ),
        'mistral': ModelInfo(
            name='mistral',
            display_name='Mistral (Local)',
            provider='ollama',
            max_tokens=100,
            temperature=0.7,
            description='Local Mistral model via Ollama'
        ),
        'llama3.2:3b': ModelInfo(
            name='llama3.2:3b',
            display_name='Llama 3.2 3B (Local)',
            provider='ollama',
            max_tokens=100,
            temperature=0.7,
            description='Local Llama 3.2 3B model via Ollama'
        )
    }
    
    # Default model
    DEFAULT_MODEL = 'gpt-3.5-turbo'
    
    def __init__(self):
        self.current_model = self.DEFAULT_MODEL
    
    def normalize_model_name(self, model_name: str) -> Optional[str]:
        """Normalize user-entered model name to a supported canonical name."""
        if not model_name:
            return None
        key = model_name.strip().lower()
        # Exact match
        if key in (name.lower() for name in self.SUPPORTED_MODELS.keys()):
            # Return the canonical with original casing from SUPPORTED_MODELS
            for canonical in self.SUPPORTED_MODELS.keys():
                if canonical.lower() == key:
                    return canonical
        # Alias match
        if key in self.ALIASES:
            return self.ALIASES[key]
        return None
    
    def get_model_info(self, model_name: str) -> Optional[ModelInfo]:
        """Get information about a specific model"""
        normalized = self.normalize_model_name(model_name) or model_name
        return self.SUPPORTED_MODELS.get(normalized)
    
    def get_available_models(self) -> List[ModelInfo]:
        """Get list of all available models"""
        return list(self.SUPPORTED_MODELS.values())
    
    def get_models_by_provider(self, provider: str) -> List[ModelInfo]:
        """Get models for a specific provider"""
        return [model for model in self.SUPPORTED_MODELS.values() 
                if model.provider == provider]
    
    def get_providers(self) -> List[str]:
        """Get list of all supported providers"""
        providers = set(model.provider for model in self.SUPPORTED_MODELS.values())
        return list(providers)
    
    def is_model_supported(self, model_name: str) -> bool:
        """Check if a model is supported (with normalization)."""
        normalized = self.normalize_model_name(model_name) or model_name
        return normalized in self.SUPPORTED_MODELS
    
    def get_default_model(self) -> str:
        """Get the default model name"""
        return self.DEFAULT_MODEL
    
    def set_current_model(self, model_name: str) -> bool:
        """Set the current model (with normalization)."""
        normalized = self.normalize_model_name(model_name) or model_name
        if self.is_model_supported(normalized):
            self.current_model = normalized
            return True
        return False

    def suggest_model(self, model_name: str) -> Optional[str]:
        """Suggest closest valid model for an unknown name."""
        choices = list(self.SUPPORTED_MODELS.keys()) + list(self.ALIASES.keys())
        matches = difflib.get_close_matches(model_name, choices, n=1, cutoff=0.6)
        return matches[0] if matches else None
    
    def get_current_model(self) -> str:
        """Get the current model name"""
        return self.current_model
    
    def get_model_prompt_template(self, model_name: str) -> str:
        """Get the optimized prompt template for a model"""
        model_info = self.get_model_info(model_name)
        if not model_info:
            return self._get_default_prompt_template()
        
        # Model-specific prompt optimizations
        if model_info.provider == 'openai':
            return self._get_openai_prompt_template()
        elif model_info.provider == 'anthropic':
            return self._get_anthropic_prompt_template()
        elif model_info.provider == 'google':
            return self._get_google_prompt_template()
        elif model_info.provider == 'cohere':
            return self._get_cohere_prompt_template()
        elif model_info.provider == 'ollama':
            return self._get_ollama_prompt_template()
        else:
            return self._get_default_prompt_template()
    
    def _get_default_prompt_template(self) -> str:
        """Default prompt template for CLI command generation"""
        return "Generate a single CLI command for: {prompt}. Return only the command, no explanations."
    
    def _get_openai_prompt_template(self) -> str:
        """OpenAI optimized prompt template"""
        return "Show me the CLI command for: {prompt}. Return only the command."
    
    def _get_anthropic_prompt_template(self) -> str:
        """Anthropic optimized prompt template"""
        return "What CLI command would I use to: {prompt}? Provide only the command."
    
    def _get_google_prompt_template(self) -> str:
        """Google optimized prompt template"""
        return "CLI command for: {prompt}. Command only."
    
    def _get_cohere_prompt_template(self) -> str:
        """Cohere optimized prompt template"""
        return "Generate a command line command for: {prompt}. Return just the command."
    
    def _get_ollama_prompt_template(self) -> str:
        """Ollama optimized prompt template"""
        return "Command: {prompt}"