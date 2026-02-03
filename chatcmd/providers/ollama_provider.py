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
    
    def generate_sql_query(self, prompt: str) -> Optional[str]:
        """
        Generate a SQL query using local Ollama models
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean SQL query string or None if generation fails
        """
        try:
            system_prompt = "You are a database engineer. Write a SQL query that {prompt}. Return only the SQL query, no explanations, no markdown, no code blocks."
            user_prompt = system_prompt.format(prompt=prompt)
            
            full_prompt = f"{user_prompt}"
            
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.config.get('temperature', 0.7),
                        "num_predict": self.config.get('max_tokens', 200)
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data:
                    raw_query = data['response'].strip()
                    clean_query = self.clean_sql_output(raw_query)
                    
                    # Validate the query
                    if self.is_valid_sql_query(clean_query):
                        return clean_query
                    else:
                        # Try to extract query from response
                        return self._extract_sql_from_response(raw_query)
            
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