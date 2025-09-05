"""
OpenAI provider implementation for ChatCMD
Handles GPT model interactions for CLI command generation
"""

from typing import Optional
from openai import OpenAI
from .base import BaseAIProvider


class OpenAIProvider(BaseAIProvider):
    """OpenAI provider for GPT models"""
    
    def __init__(self, api_key: str, model_name: str = 'gpt-3.5-turbo', **kwargs):
        super().__init__(api_key, **kwargs)
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)
    
    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a CLI command using OpenAI models
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean CLI command string or None if generation fails
        """
        try:
            # Use optimized prompt for CLI command generation
            system_prompt = "You are a CLI command expert. Generate only the command needed to accomplish the task. Return only the command, no explanations, no markdown, no code blocks."
            user_prompt = f"Command for: {prompt}"
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.config.get('max_tokens', 100),
                temperature=self.config.get('temperature', 0.7),
                n=1
            )
            
            if response.choices and len(response.choices) > 0:
                raw_command = response.choices[0].message.content.strip()
                clean_command = self.clean_command_output(raw_command)
                
                # Validate the command
                if self.is_valid_command(clean_command):
                    return clean_command
                else:
                    # Try to extract command from response
                    return self._extract_command_from_response(raw_command)
            
            return None
            
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate OpenAI API key
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Test the API key with a simple request
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "test"}],
                max_tokens=1
            )
            return True
        except Exception:
            return False
    
    def get_model_name(self) -> str:
        """Get the model name being used"""
        return self.model_name
    
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