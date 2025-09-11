"""
Ollama provider implementation for ChatCMD
Handles local Ollama model interactions for CLI command generation
"""

from typing import Optional
import requests
import json
from .base import BaseAIProvider
from chatcmd.config.model_config import ModelConfig


class OllamaProvider(BaseAIProvider):
    """Ollama provider for local models"""
    
    def __init__(self, api_key: str = "", model_name: str = 'llama2', **kwargs):
        super().__init__(api_key, **kwargs)
        self.model_name = model_name
        self.base_url = kwargs.get('base_url', 'http://localhost:11434')
        self.model_config = ModelConfig()
    
    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a CLI command using local Ollama models
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean CLI command string or None if generation fails
        """
        try:
            # Use model-specific prompt template
            template = self.model_config.get_model_prompt_template(self.model_name)
            user_prompt = template.format(prompt=prompt)
            system_prompt = "You are a CLI command expert. Return only the command, no explanations, no markdown, no code blocks."
            
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.config.get('temperature', 0.7),
                        "num_predict": self.config.get('max_tokens', 100)
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    raw_command = data['response'].strip()
                    clean_command = self.clean_command_output(raw_command)
                    
                    # Validate the command
                    if self.is_valid_command(clean_command):
                        return clean_command
                    else:
                        # Try to extract command from response
                        return self._extract_command_from_response(raw_command)
            
            return None
            
        except Exception as e:
            print(f"Ollama API error: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate Ollama connection (no API key needed for local)
        
        Returns:
            True if Ollama is accessible, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def get_model_name(self) -> str:
        """Get the model name being used"""
        return self.model_name
    
    def is_model_available(self) -> bool:
        """
        Check if the specified model is available in Ollama
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                models = [model['name'] for model in data.get('models', [])]
                return self.model_name in models
            return False
        except Exception:
            return False
    
    def _extract_command_from_response(self, response: str) -> Optional[str]:
        """
        Extract command from response when validation fails
        
        Args:
            response: Raw AI response
            
        Returns:
            Extracted command or None
        """
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Remove common prefixes
            prefixes = ['$', '>', 'Command:', 'Command is:', 'Use:', 'Try:']
            for prefix in prefixes:
                if line.startswith(prefix):
                    line = line[len(prefix):].strip()
            
            # Check if this line looks like a command
            if self.is_valid_command(line):
                return line
        
        return None