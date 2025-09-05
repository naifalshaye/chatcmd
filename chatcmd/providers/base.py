"""
Abstract base class for AI providers
Ensures all providers return clean CLI commands
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseAIProvider(ABC):
    """Abstract base class for AI providers focused on CLI command generation"""
    
    def __init__(self, api_key: str, **kwargs):
        self.api_key = api_key
        self.config = kwargs
    
    @abstractmethod
    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a clean CLI command from user prompt
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean CLI command string or None if generation fails
        """
        pass
    
    @abstractmethod
    def validate_api_key(self) -> bool:
        """
        Validate the API key for this provider
        
        Returns:
            True if API key is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the model name being used
        
        Returns:
            Model name string
        """
        pass
    
    def clean_command_output(self, response: str) -> str:
        """
        Clean AI response to extract only the CLI command
        
        Args:
            response: Raw AI response
            
        Returns:
            Clean CLI command string
        """
        if not response:
            return ""
            
        # Remove common prefixes and suffixes
        response = response.strip()
        
        # Remove markdown code blocks
        if response.startswith('```') and response.endswith('```'):
            lines = response.split('\n')
            response = '\n'.join(lines[1:-1])
        
        # Remove command prefixes
        prefixes_to_remove = [
            'Command:', 'Command is:', 'The command is:', 'Use:', 'Try:',
            'Here is the command:', 'Here\'s the command:', 'CLI command:',
            'Terminal command:', 'Run:', 'Execute:'
        ]
        
        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()
        
        # Remove explanatory text after the command
        lines = response.split('\n')
        if lines:
            # Take only the first line (the command)
            command = lines[0].strip()
            
            # Remove any trailing punctuation
            command = command.rstrip('.,!?')
            
            return command
        
        return response
    
    def is_valid_command(self, command: str) -> bool:
        """
        Basic validation to ensure the response looks like a CLI command
        
        Args:
            command: Command string to validate
            
        Returns:
            True if command appears valid, False otherwise
        """
        if not command or len(command.strip()) < 2:
            return False
            
        # Check for common command patterns
        command = command.strip()
        
        # Should not contain explanatory text
        explanatory_phrases = [
            'there is no command',
            'no specific command',
            'not a command',
            'cannot find',
            'unable to',
            'sorry,',
            'i cannot',
            'i don\'t know'
        ]
        
        command_lower = command.lower()
        for phrase in explanatory_phrases:
            if phrase in command_lower:
                return False
        
        # Should look like a command (starts with common command patterns)
        command_starters = [
            'git', 'npm', 'pip', 'apt', 'yum', 'brew', 'docker', 'kubectl',
            'aws', 'gcloud', 'az', 'curl', 'wget', 'ssh', 'scp', 'rsync',
            'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'chmod', 'chown',
            'grep', 'find', 'sed', 'awk', 'sort', 'uniq', 'head', 'tail',
            'cat', 'less', 'more', 'vim', 'nano', 'emacs', 'ps', 'top',
            'kill', 'killall', 'jobs', 'bg', 'fg', 'nohup', 'screen', 'tmux'
        ]
        
        # Check if command starts with a known command starter
        for starter in command_starters:
            if command.startswith(starter):
                return True
        
        # Allow commands that start with common symbols
        if command.startswith(('sudo', 'sudo -u', 'su -', 'su -c')):
            return True
            
        # Allow commands that start with environment variables
        if '=' in command and command.split('=')[0].replace('_', '').isalnum():
            return True
        
        return False