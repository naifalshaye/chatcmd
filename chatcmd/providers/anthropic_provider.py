"""
Anthropic provider implementation for ChatCMD
Handles Claude model interactions for CLI command generation
"""

from typing import Optional
import anthropic
from .base import BaseAIProvider
from chatcmd.config.model_config import ModelConfig


class AnthropicProvider(BaseAIProvider):
    """Anthropic provider for Claude models"""
    
    def __init__(self, api_key: str, model_name: str = 'claude-3-haiku-20240307', **kwargs):
        super().__init__(api_key, **kwargs)
        self.model_name = model_name
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model_config = ModelConfig()
    
    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a CLI command using Anthropic Claude models
        
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
            
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=self.config.get('max_tokens', 100),
                temperature=self.config.get('temperature', 0.7),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            if response.content and len(response.content) > 0:
                raw_command = response.content[0].text.strip()
                clean_command = self.clean_command_output(raw_command)
                
                # Validate the command
                if self.is_valid_command(clean_command):
                    return clean_command
                else:
                    # Try to extract command from response
                    return self._extract_command_from_response(raw_command)
            
            return None
            
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate Anthropic API key
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Basic format check to avoid network dependency here
            return bool(self.api_key and len(self.api_key) > 20)
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