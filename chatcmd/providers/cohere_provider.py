"""
Cohere provider implementation for ChatCMD
Handles Cohere model interactions for CLI command generation
"""

from typing import Optional
import cohere
from .base import BaseAIProvider
from chatcmd.config.model_config import ModelConfig


class CohereProvider(BaseAIProvider):
    """Cohere provider for Command models"""
    
    def __init__(self, api_key: str, model_name: str = 'command', **kwargs):
        super().__init__(api_key, **kwargs)
        self.model_name = model_name
        self.client = cohere.Client(api_key)
        self.model_config = ModelConfig()
    
    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a CLI command using Cohere models
        
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
            
            response = self.client.generate(
                model=self.model_name,
                prompt=full_prompt,
                max_tokens=self.config.get('max_tokens', 100),
                temperature=self.config.get('temperature', 0.7),
                num_generations=1
            )
            
            if response.generations and len(response.generations) > 0:
                raw_command = response.generations[0].text.strip()
                clean_command = self.clean_command_output(raw_command)
                
                # Validate the command
                if self.is_valid_command(clean_command):
                    return clean_command
                else:
                    # Try to extract command from response
                    return self._extract_command_from_response(raw_command)
            
            return None
            
        except Exception as e:
            print(f"Cohere API error: {e}")
            return None
    
    def generate_sql_query(self, prompt: str) -> Optional[str]:
        """
        Generate a SQL query using Cohere models
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean SQL query string or None if generation fails
        """
        try:
            system_prompt = "You are a database engineer. Write a SQL query that {prompt}. Return only the SQL query, no explanations, no markdown, no code blocks."
            user_prompt = system_prompt.format(prompt=prompt)
            
            response = self.client.generate(
                model=self.model_name,
                prompt=user_prompt,
                max_tokens=self.config.get('max_tokens', 200),
                temperature=self.config.get('temperature', 0.7),
                stop_sequences=["\n\n", "Explanation:", "Note:"]
            )
            
            if response.generations and len(response.generations) > 0:
                raw_query = response.generations[0].text.strip()
                clean_query = self.clean_sql_output(raw_query)
                
                # Validate the query
                if self.is_valid_sql_query(clean_query):
                    return clean_query
                else:
                    # Try to extract query from response
                    return self._extract_sql_from_response(raw_query)
            
            return None
            
        except Exception as e:
            print(f"Cohere API error: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate Cohere API key (format-only to avoid network dependency)
        """
        try:
            return bool(self.api_key and len(self.api_key) > 20)
        except Exception:
            return False
    
    def get_model_name(self) -> str:
        """Get the model name being used"""
        return self.model_name