"""
Google provider implementation for ChatCMD
Handles Gemini model interactions for CLI command generation
"""

from typing import Optional
from .base import BaseAIProvider
from chatcmd.config.model_config import ModelConfig

# Try new google.genai package first, fall back to deprecated google.generativeai
try:
    from google import genai
    from google.genai import types
    USING_NEW_API = True
except ImportError:
    try:
        import google.generativeai as genai_legacy
        USING_NEW_API = False
    except ImportError:
        genai_legacy = None
        USING_NEW_API = False


class GoogleProvider(BaseAIProvider):
    """Google provider for Gemini models"""

    def __init__(self, api_key: str, model_name: str = 'gemini-pro', **kwargs):
        super().__init__(api_key, **kwargs)
        self.model_name = model_name
        self.model_config = ModelConfig()

        if USING_NEW_API:
            # New google.genai API
            self.client = genai.Client(api_key=api_key)
        elif genai_legacy:
            # Legacy google.generativeai API (deprecated)
            genai_legacy.configure(api_key=api_key)
            self.model = genai_legacy.GenerativeModel(model_name)
        else:
            raise ImportError("No Google AI package available. Install google-genai: pip install google-genai")

    def generate_command(self, prompt: str) -> Optional[str]:
        """
        Generate a CLI command using Google Gemini models

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

            if USING_NEW_API:
                # New API
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=self.config.get('max_tokens', 100),
                        temperature=self.config.get('temperature', 0.7)
                    )
                )
                response_text = response.text if hasattr(response, 'text') else None
            else:
                # Legacy API
                response = self.model.generate_content(
                    full_prompt,
                    generation_config=genai_legacy.types.GenerationConfig(
                        max_output_tokens=self.config.get('max_tokens', 100),
                        temperature=self.config.get('temperature', 0.7)
                    )
                )
                response_text = response.text if hasattr(response, 'text') else None

            if response_text:
                raw_command = response_text.strip()
                clean_command = self.clean_command_output(raw_command)

                # Validate the command
                if self.is_valid_command(clean_command):
                    return clean_command
                else:
                    # Try to extract command from response
                    return self._extract_command_from_response(raw_command)

            return None

        except Exception:
            print("Google API error. Please check your API key and try again.")
            return None

    def generate_sql_query(self, prompt: str) -> Optional[str]:
        """
        Generate a SQL query using Google Gemini models

        Args:
            prompt: User's description of what they want to do

        Returns:
            Clean SQL query string or None if generation fails
        """
        try:
            system_prompt = "You are a database engineer. Write a SQL query that {prompt}. Return only the SQL query, no explanations, no markdown, no code blocks."
            user_prompt = system_prompt.format(prompt=prompt)

            if USING_NEW_API:
                # New API
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        max_output_tokens=self.config.get('max_tokens', 200),
                        temperature=self.config.get('temperature', 0.7)
                    )
                )
                response_text = response.text if hasattr(response, 'text') else None
            else:
                # Legacy API
                response = self.model.generate_content(
                    user_prompt,
                    generation_config=genai_legacy.types.GenerationConfig(
                        max_output_tokens=self.config.get('max_tokens', 200),
                        temperature=self.config.get('temperature', 0.7)
                    )
                )
                response_text = response.text if hasattr(response, 'text') else None

            if response_text:
                raw_query = response_text.strip()
                clean_query = self.clean_sql_output(raw_query)

                # Validate the query
                if self.is_valid_sql_query(clean_query):
                    return clean_query
                else:
                    # Try to extract query from response
                    return self._extract_sql_from_response(raw_query)

            return None

        except Exception:
            print("Google API error. Please check your API key and try again.")
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
        Validate Google API key (format-only to avoid network dependency)
        """
        try:
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
