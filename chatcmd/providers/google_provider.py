"""
Google provider implementation for ChatCMD
Handles Gemini model interactions for CLI command generation
"""

from typing import Optional
import google.generativeai as genai
from .base import BaseAIProvider


class GoogleProvider(BaseAIProvider):
    """Google provider for Gemini models"""
    
    def __init__(self, api_key: str, model_name: str = 'gemini-pro', **kwargs):
        super().__init__(api_key, **kwargs)
        self.model_name = model_name
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a CLI command using Google Gemini models
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean CLI command string or None if generation fails
        """
        try:
            # Use optimized prompt for CLI command generation
            system_prompt = "You are a CLI command expert. Generate only the command needed to accomplish the task. Return only the command, no explanations, no markdown, no code blocks."
            user_prompt = f"Command for: {prompt}"
            
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.config.get('max_tokens', 100),
                    temperature=self.config.get('temperature', 0.7)
                )
            )
            
            if response.text:
                raw_command = response.text.strip()
                clean_command = self.clean_command_output(raw_command)
                
                # Validate the command
                if self.is_valid_command(clean_command):
                    return clean_command
                else:
                    # Try to extract command from response
                    return self._extract_command_from_response(raw_command)
            
            return None
            
        except Exception as e:
            print(f"Google API error: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """
        Validate Google API key
        
        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Test the API key with a simple request
            response = self.model.generate_content("test")
            return response.text is not None
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