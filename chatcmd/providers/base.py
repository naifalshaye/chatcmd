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
    def generate_sql_query(self, prompt: str) -> Optional[str]:
        """
        Generate a clean SQL query from user prompt
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean SQL query string or None if generation fails
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
        elif response.startswith('```bash') and response.endswith('```'):
            lines = response.split('\n')
            response = '\n'.join(lines[1:-1])
        elif response.startswith('```sh') and response.endswith('```'):
            lines = response.split('\n')
            response = '\n'.join(lines[1:-1])
        
        # Remove command prefixes
        prefixes_to_remove = [
            'Command:', 'Command is:', 'The command is:', 'Use:', 'Try:',
            'Here is the command:', 'Here\'s the command:', 'CLI command:',
            'Terminal command:', 'Run:', 'Execute:', 'The command:', 'Here\'s:',
            'Here is:', 'You can use:', 'Use this command:', 'Run this:'
        ]
        
        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()
        
        # Remove explanatory text after the command
        lines = response.split('\n')
        if lines:
            # Take only the command lines (until we hit explanatory text)
            command_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Stop if we hit explanatory text
                if any(phrase in line.lower() for phrase in [
                    'this command', 'the command', 'explanation', 'note:', 'note that',
                    'remember', 'keep in mind', 'also', 'additionally', 'this will',
                    'for example', 'you can', 'alternatively', 'or you can'
                ]):
                    break
                command_lines.append(line)
            
            if command_lines:
                # Join multiple lines if it's a multi-line command
                command = ' '.join(command_lines)
            else:
                # Fallback to first line
                command = lines[0].strip()
            
            # Remove any trailing punctuation
            command = command.rstrip('.,!?')
            
            # Hardened: reject command substitution/backticks/here-doc tokens by default
            unsafe_tokens = ['`', '$(', '<<']
            if any(tok in command for tok in unsafe_tokens):
                return ""
            
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
    
    def clean_sql_output(self, response: str) -> str:
        """
        Clean AI response to extract only the SQL query
        
        Args:
            response: Raw AI response
            
        Returns:
            Clean SQL query string
        """
        if not response:
            return ""
            
        # Remove common prefixes and suffixes
        response = response.strip()
        
        # Remove markdown code blocks
        if response.startswith('```') and response.endswith('```'):
            lines = response.split('\n')
            response = '\n'.join(lines[1:-1])
        elif response.startswith('```sql') and response.endswith('```'):
            lines = response.split('\n')
            response = '\n'.join(lines[1:-1])
        
        # Remove only explanatory prefixes, NOT SQL keywords
        prefixes_to_remove = [
            'Query:', 'SQL Query:', 'The query is:', 'Here is the query:', 
            'Here\'s the query:', 'SQL:', 'Here\'s the SQL:', 'Here is the SQL:',
            'The SQL query is:', 'Here\'s the SQL query:', 'Here is the SQL query:'
        ]
        
        for prefix in prefixes_to_remove:
            if response.lower().startswith(prefix.lower()):
                response = response[len(prefix):].strip()
        
        # Remove explanatory text after the query
        lines = response.split('\n')
        if lines:
            # Take only the SQL query lines (until we hit explanatory text)
            query_lines = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Stop if we hit explanatory text
                if any(phrase in line.lower() for phrase in [
                    'this query', 'the query', 'explanation', 'note:', 'note that',
                    'remember', 'keep in mind', 'also', 'additionally', 'this will',
                    'this sql', 'the above', 'for example', 'you can'
                ]):
                    break
                query_lines.append(line)
            
            if query_lines:
                response = '\n'.join(query_lines)
            
            # Remove any trailing punctuation
            response = response.rstrip('.,!?')
            
            return response
        
        return response
    
    def is_valid_sql_query(self, query: str) -> bool:
        """
        Basic validation to ensure the response looks like a SQL query
        
        Args:
            query: SQL query string to validate
            
        Returns:
            True if query appears valid, False otherwise
        """
        if not query or len(query.strip()) < 3:
            return False
            
        query = query.strip().upper()
        
        # Should not contain explanatory text
        explanatory_phrases = [
            'THERE IS NO QUERY',
            'NO SPECIFIC QUERY',
            'NOT A QUERY',
            'CANNOT FIND',
            'UNABLE TO',
            'SORRY,',
            'I CANNOT',
            'I DON\'T KNOW'
        ]
        
        for phrase in explanatory_phrases:
            if phrase in query:
                return False
        
        # Should contain SQL keywords
        sql_keywords = [
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER',
            'FROM', 'WHERE', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'OUTER',
            'GROUP BY', 'ORDER BY', 'HAVING', 'UNION', 'UNION ALL'
        ]
        
        for keyword in sql_keywords:
            if keyword in query:
                return True
        
        return False