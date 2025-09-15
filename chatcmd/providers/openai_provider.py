"""
OpenAI provider implementation for ChatCMD
Handles GPT model interactions for CLI command generation
"""

from typing import Optional
from openai import OpenAI
from .base import BaseAIProvider
from chatcmd.config.model_config import ModelConfig


class OpenAIProvider(BaseAIProvider):
    """OpenAI provider for GPT models"""
    
    def __init__(self, api_key: str, model_name: str = 'gpt-3.5-turbo', **kwargs):
        super().__init__(api_key, **kwargs)
        self.model_name = model_name
        self.client = OpenAI(api_key=api_key)
        self.model_config = ModelConfig()
    
    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a CLI command using OpenAI models
        
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
            error_info = self._parse_api_error(e)
            print(f"OpenAI API Error:")
            print(f"  Code: {error_info['code']}")
            print(f"  Type: {error_info['type']}")
            print(f"  Message: {error_info['message']}")
            return None
    
    def generate_sql_query(self, prompt: str) -> Optional[str]:
        """
        Generate a SQL query using OpenAI models
        
        Args:
            prompt: User's description of what they want to do
            
        Returns:
            Clean SQL query string or None if generation fails
        """
        try:
            system_prompt = "You are a database engineer. Write a SQL query that {prompt}. Return only the SQL query, no explanations, no markdown, no code blocks."
            user_prompt = system_prompt.format(prompt=prompt)
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=self.config.get('max_tokens', 200),
                temperature=self.config.get('temperature', 0.7),
                n=1
            )
            
            if response.choices and len(response.choices) > 0:
                raw_query = response.choices[0].message.content.strip()
                clean_query = self.clean_sql_output(raw_query)
                
                # Validate the query
                if self.is_valid_sql_query(clean_query):
                    return clean_query
                else:
                    # Try to extract query from response
                    return self._extract_sql_from_response(raw_query)
            
            return None
            
        except Exception as e:
            error_info = self._parse_api_error(e)
            print(f"OpenAI API Error:")
            print(f"  Code: {error_info['code']}")
            print(f"  Type: {error_info['type']}")
            print(f"  Message: {error_info['message']}")
            return None
    
    def _extract_sql_from_response(self, response: str) -> Optional[str]:
        """Extract SQL query from response that might contain extra text"""
        lines = response.split('\n')
        query_lines = []
        found_sql_start = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for SQL keywords to start collecting
            if any(keyword in line.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER']):
                found_sql_start = True
                query_lines.append(line)
            elif found_sql_start:  # If we've started collecting query lines, continue until we hit explanatory text
                if any(phrase in line.lower() for phrase in ['this query', 'the query', 'explanation', 'note:', 'this will', 'for example', 'you can']):
                    break
                # Only add non-empty lines that look like SQL
                if line and not line.startswith(('--', '/*', '#')):  # Skip comments
                    query_lines.append(line)
        
        if query_lines:
            # Join lines and clean up
            query = ' '.join(query_lines)
            # Remove extra spaces and ensure proper formatting
            query = ' '.join(query.split())
            return query
        
        return None
    
    def validate_api_key(self) -> bool:
        """
        Validate OpenAI API key format
        
        Returns:
            True if API key format is valid, False otherwise
        """
        try:
            # Basic format validation without making API calls
            if not self.api_key or len(self.api_key) < 20:
                return False
            
            # Check if it starts with sk- (including sk-proj-)
            if not self.api_key.startswith('sk-'):
                return False
            
            # Check if it contains only valid characters
            import re
            if not re.match("^[a-zA-Z0-9-_]+$", self.api_key):
                return False
            
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
    
    def _parse_api_error(self, error) -> dict:
        """
        Parse OpenAI API error into human-readable format
        
        Args:
            error: Exception object from OpenAI API
            
        Returns:
            Dictionary with parsed error information
        """
        try:
            # Extract error details from the exception
            error_str = str(error)
            
            # Default error info
            error_info = {
                'code': 'unknown',
                'type': 'unknown_error',
                'message': error_str
            }
            
            # Try to extract error code
            if 'Error code:' in error_str:
                code_match = error_str.split('Error code:')[1].split(' -')[0].strip()
                error_info['code'] = code_match
            
            # Try to extract error details from JSON-like string
            if '{' in error_str and '}' in error_str:
                try:
                    import json
                    import re
                    
                    # Find the JSON part after "Error code: XXX -"
                    if 'Error code:' in error_str and ' - ' in error_str:
                        json_start = error_str.find(' - ') + 3
                        json_str = error_str[json_start:].strip()
                        
                        # Convert single quotes to double quotes for valid JSON
                        json_str = json_str.replace("'", '"')
                        # Convert Python None to JSON null
                        json_str = json_str.replace('None', 'null')
                        
                        try:
                            error_data = json.loads(json_str)
                            if 'error' in error_data:
                                error_obj = error_data['error']
                                error_info['code'] = error_obj.get('code', error_info['code'])
                                error_info['type'] = error_obj.get('type', error_info['type'])
                                error_info['message'] = error_obj.get('message', error_info['message'])
                        except json.JSONDecodeError:
                            pass
                except Exception:
                    pass
            
            # Map common error codes to human-readable messages
            error_messages = {
                '429': 'Rate limit exceeded - too many requests',
                '401': 'Invalid API key or authentication failed',
                '403': 'Access forbidden - check your API key permissions',
                '404': 'Model not found or endpoint not available',
                '500': 'Internal server error - try again later',
                'insufficient_quota': 'You have exceeded your current quota - please check your billing and add credits',
                'invalid_api_key': 'The API key provided is invalid',
                'rate_limit_exceeded': 'Too many requests - please wait before trying again'
            }
            
            # Special handling for quota errors
            if error_info['type'] == 'insufficient_quota' or 'quota' in error_info['message'].lower():
                error_info['message'] = 'You have exceeded your current quota - please check your billing and add credits to your OpenAI account'
            
            # Override message if we have a better one
            if error_info['code'] in error_messages:
                error_info['message'] = error_messages[error_info['code']]
            elif error_info['type'] in error_messages:
                error_info['message'] = error_messages[error_info['type']]
            
            return error_info
            
        except Exception:
            # Fallback to basic error info
            return {
                'code': 'unknown',
                'type': 'parsing_error',
                'message': str(error)
            }