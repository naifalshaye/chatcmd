"""
Developer tools and utilities for ChatCMD
Additional features useful for software engineers and developers
"""

import json
import base64
import hashlib
import uuid
import re
import time
import datetime
import requests
import pyperclip
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, quote, unquote


class DeveloperTools:
    """Collection of developer-focused tools and utilities"""
    
    def __init__(self):
        self.qr_api_url = "https://api.qrserver.com/v1/create-qr-code/"
    
    def generate_code_snippet(self, language: str, description: str) -> str:
        """
        Generate code snippets in various programming languages
        
        Args:
            language: Programming language (python, javascript, java, etc.)
            description: Description of what the code should do
            
        Returns:
            Generated code snippet
        """
        print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                        Generate {language.upper()} Code Snippet
        """)
        
        # Common code templates
        templates = {
            'python': {
                'function': f'def {description.lower().replace(" ", "_")}():\n    """{description}"""\n    pass',
                'class': f'class {description.title().replace(" ", "")}:\n    """{description}"""\n    def __init__(self):\n        pass',
                'import': f'import {description.lower().replace(" ", "_")}',
                'loop': f'for item in {description.lower().replace(" ", "_")}:\n    print(item)'
            },
            'javascript': {
                'function': f'function {description.lower().replace(" ", "")}() {{\n    // {description}\n    return null;\n}}',
                'class': f'class {description.title().replace(" ", "")} {{\n    constructor() {{\n        // {description}\n    }}\n}}',
                'arrow': f'const {description.lower().replace(" ", "")} = () => {{\n    // {description}\n}};',
                'async': f'async function {description.lower().replace(" ", "")}() {{\n    // {description}\n    return await Promise.resolve();\n}}'
            },
            'java': {
                'class': f'public class {description.title().replace(" ", "")} {{\n    // {description}\n    public static void main(String[] args) {{\n        \n    }}\n}}',
                'method': f'public void {description.lower().replace(" ", "")}() {{\n    // {description}\n}}',
                'interface': f'public interface {description.title().replace(" ", "")} {{\n    // {description}\n}}'
            },
            'bash': {
                'script': f'#!/bin/bash\n# {description}\n\necho "Hello World"',
                'function': f'function {description.lower().replace(" ", "_")}() {{\n    # {description}\n    echo "Function executed"\n}}',
                'loop': f'for i in {{1..10}}; do\n    # {description}\n    echo $i\ndone'
            }
        }
        
        if language.lower() in templates:
            # Simple template selection based on description keywords
            if 'function' in description.lower():
                code = templates[language.lower()]['function']
            elif 'class' in description.lower():
                code = templates[language.lower()]['class']
            elif 'loop' in description.lower():
                code = templates[language.lower()]['loop']
            else:
                # Default to first available template
                code = list(templates[language.lower()].values())[0]
        else:
            code = f"# {description}\n# Code snippet for {language}\n# Implementation needed"
        
        print(f"Generated {language} code:")
        print(" " + code)
        pyperclip.copy(code)
        return code
    
    def generate_regex_pattern(self, description: str) -> str:
        """
        Generate regex patterns for common use cases
        
        Args:
            description: Description of what the regex should match
            
        Returns:
            Generated regex pattern
        """
        print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Generate Regex Pattern
        """)
        
        # Common regex patterns
        patterns = {
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'phone': r'^\+?[\d\s\-\(\)]{10,}$',
            'url': r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$',
            'ip': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
            'date': r'^\d{4}-\d{2}-\d{2}$',
            'time': r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$',
            'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            'username': r'^[a-zA-Z0-9_]{3,20}$',
            'credit_card': r'^\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}$',
            'zip_code': r'^\d{5}(-\d{4})?$'
        }
        
        description_lower = description.lower()
        
        # Try to match description to known patterns
        for key, pattern in patterns.items():
            if key in description_lower:
                regex = pattern
                break
        else:
            # Generate a basic pattern based on description
            if 'number' in description_lower:
                regex = r'\d+'
            elif 'word' in description_lower:
                regex = r'\w+'
            elif 'letter' in description_lower:
                regex = r'[a-zA-Z]+'
            else:
                regex = r'.*'
        
        print(f"Regex Pattern: {regex}")
        pyperclip.copy(regex)
        return regex
    
    def format_json(self, json_string: str) -> str:
        """
        Format and validate JSON string
        
        Args:
            json_string: JSON string to format
            
        Returns:
            Formatted JSON string
        """
        print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            JSON Formatter
        """)
        
        try:
            # Parse and format JSON
            parsed = json.loads(json_string)
            formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            print("Formatted JSON:")
            print(formatted)
            pyperclip.copy(formatted)
            return formatted
        except json.JSONDecodeError as e:
            error_msg = f"Invalid JSON: {e}"
            print(error_msg)
            return error_msg
    
    def base64_encode_decode(self, text: str, operation: str = 'encode') -> str:
        """
        Encode or decode base64 strings
        
        Args:
            text: Text to encode/decode
            operation: 'encode' or 'decode'
            
        Returns:
            Encoded or decoded string
        """
        print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                        Base64 {operation.upper()}
        """)
        
        try:
            if operation.lower() == 'encode':
                result = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                print(f"Encoded: {result}")
            else:  # decode
                result = base64.b64decode(text.encode('utf-8')).decode('utf-8')
                print(f"Decoded: {result}")
            
            pyperclip.copy(result)
            return result
        except Exception as e:
            error_msg = f"Error: {e}"
            print(error_msg)
            return error_msg
    
    def generate_git_commands(self, operation: str) -> str:
        """
        Generate common git commands
        
        Args:
            operation: Git operation (commit, push, pull, etc.)
            
        Returns:
            Git command string
        """
        print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Git Command Helper
        """)
        
        git_commands = {
            'init': 'git init',
            'clone': 'git clone <repository-url>',
            'add': 'git add .',
            'commit': 'git commit -m "commit message"',
            'push': 'git push origin main',
            'pull': 'git pull origin main',
            'status': 'git status',
            'log': 'git log --oneline',
            'branch': 'git branch -a',
            'checkout': 'git checkout -b new-branch',
            'merge': 'git merge branch-name',
            'rebase': 'git rebase main',
            'stash': 'git stash',
            'reset': 'git reset --hard HEAD',
            'remote': 'git remote -v',
            'fetch': 'git fetch origin',
            'diff': 'git diff',
            'blame': 'git blame filename',
            'revert': 'git revert commit-hash',
            'cherry-pick': 'git cherry-pick commit-hash'
        }
        
        operation_lower = operation.lower()
        
        # Find matching command
        for key, command in git_commands.items():
            if key in operation_lower:
                print(f"Git Command: {command}")
                pyperclip.copy(command)
                return command
        
        # Default to status if no match
        default_cmd = 'git status'
        print(f"Git Command: {default_cmd}")
        pyperclip.copy(default_cmd)
        return default_cmd
    
    def generate_docker_commands(self, operation: str) -> str:
        """
        Generate common Docker commands
        
        Args:
            operation: Docker operation (run, build, push, etc.)
            
        Returns:
            Docker command string
        """
        print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Docker Command Helper
        """)
        
        docker_commands = {
            'run': 'docker run -it <image-name>',
            'build': 'docker build -t <image-name> .',
            'push': 'docker push <image-name>',
            'pull': 'docker pull <image-name>',
            'images': 'docker images',
            'ps': 'docker ps -a',
            'exec': 'docker exec -it <container-id> /bin/bash',
            'stop': 'docker stop <container-id>',
            'start': 'docker start <container-id>',
            'rm': 'docker rm <container-id>',
            'rmi': 'docker rmi <image-id>',
            'logs': 'docker logs <container-id>',
            'inspect': 'docker inspect <container-id>',
            'network': 'docker network ls',
            'volume': 'docker volume ls',
            'compose': 'docker-compose up -d',
            'down': 'docker-compose down',
            'restart': 'docker restart <container-id>',
            'stats': 'docker stats',
            'system': 'docker system prune -a'
        }
        
        operation_lower = operation.lower()
        
        # Find matching command
        for key, command in docker_commands.items():
            if key in operation_lower:
                print(f"Docker Command: {command}")
                pyperclip.copy(command)
                return command
        
        # Default to ps if no match
        default_cmd = 'docker ps -a'
        print(f"Docker Command: {default_cmd}")
        pyperclip.copy(default_cmd)
        return default_cmd
    
    def generate_file_hash(self, text: str, algorithm: str = 'md5') -> str:
        """
        Generate file hashes
        
        Args:
            text: Text to hash
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
            
        Returns:
            Generated hash
        """
        print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                        Generate {algorithm.upper()} Hash
        """)
        
        try:
            if algorithm.lower() == 'md5':
                hash_obj = hashlib.md5()
            elif algorithm.lower() == 'sha1':
                hash_obj = hashlib.sha1()
            elif algorithm.lower() == 'sha256':
                hash_obj = hashlib.sha256()
            elif algorithm.lower() == 'sha512':
                hash_obj = hashlib.sha512()
            else:
                hash_obj = hashlib.md5()
            
            hash_obj.update(text.encode('utf-8'))
            hash_value = hash_obj.hexdigest()
            
            print(f"{algorithm.upper()} Hash: {hash_value}")
            pyperclip.copy(hash_value)
            return hash_value
        except Exception as e:
            error_msg = f"Error generating hash: {e}"
            print(error_msg)
            return error_msg
    
    def generate_uuid(self, version: int = 4) -> str:
        """
        Generate UUIDs in different formats
        
        Args:
            version: UUID version (1, 3, 4, 5)
            
        Returns:
            Generated UUID
        """
        print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Generate UUID v{version}
        """)
        
        try:
            if version == 1:
                uuid_value = str(uuid.uuid1())
            elif version == 3:
                uuid_value = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'example.com'))
            elif version == 4:
                uuid_value = str(uuid.uuid4())
            elif version == 5:
                uuid_value = str(uuid.uuid5(uuid.NAMESPACE_DNS, 'example.com'))
            else:
                uuid_value = str(uuid.uuid4())
            
            print(f"UUID v{version}: {uuid_value}")
            pyperclip.copy(uuid_value)
            return uuid_value
        except Exception as e:
            error_msg = f"Error generating UUID: {e}"
            print(error_msg)
            return error_msg
    
    def convert_timestamp(self, timestamp: str, format_type: str = 'unix') -> str:
        """
        Convert between different timestamp formats
        
        Args:
            timestamp: Timestamp to convert
            format_type: Target format (unix, iso, readable)
            
        Returns:
            Converted timestamp
        """
        print(f"""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                        Timestamp Converter
        """)
        
        try:
            # Try to parse as unix timestamp first
            if timestamp.isdigit():
                unix_time = int(timestamp)
                dt = datetime.datetime.fromtimestamp(unix_time)
            else:
                # Try to parse as ISO format
                dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                unix_time = int(dt.timestamp())
            
            if format_type.lower() == 'unix':
                result = str(unix_time)
            elif format_type.lower() == 'iso':
                result = dt.isoformat()
            elif format_type.lower() == 'readable':
                result = dt.strftime('%Y-%m-%d %H:%M:%S')
            else:
                result = str(unix_time)
            
            print(f"Converted timestamp: {result}")
            pyperclip.copy(result)
            return result
        except Exception as e:
            error_msg = f"Error converting timestamp: {e}"
            print(error_msg)
            return error_msg
    
    def generate_qr_code(self, text: str) -> str:
        """
        Generate QR code for text/URL
        
        Args:
            text: Text or URL to encode in QR code
            
        Returns:
            QR code URL
        """
        print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            QR Code Generator
        """)
        
        try:
            # URL encode the text
            encoded_text = quote(text)
            qr_url = f"{self.qr_api_url}?size=200x200&data={encoded_text}"
            
            print(f"QR Code URL: {qr_url}")
            print(f"Text: {text}")
            pyperclip.copy(qr_url)
            return qr_url
        except Exception as e:
            error_msg = f"Error generating QR code: {e}"
            print(error_msg)
            return error_msg
    
    def generate_markdown_table(self, headers: List[str], rows: List[List[str]]) -> str:
        """
        Generate markdown table
        
        Args:
            headers: List of column headers
            rows: List of rows (each row is a list of cells)
            
        Returns:
            Markdown table string
        """
        print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            Markdown Table Generator
        """)
        
        try:
            # Create header row
            header_row = "| " + " | ".join(headers) + " |"
            
            # Create separator row
            separator = "| " + " | ".join(["---"] * len(headers)) + " |"
            
            # Create data rows
            data_rows = []
            for row in rows:
                data_row = "| " + " | ".join(str(cell) for cell in row) + " |"
                data_rows.append(data_row)
            
            # Combine all parts
            table = "\n".join([header_row, separator] + data_rows)
            
            print("Markdown Table:")
            print(table)
            pyperclip.copy(table)
            return table
        except Exception as e:
            error_msg = f"Error generating table: {e}"
            print(error_msg)
            return error_msg
    
    def generate_curl_command(self, url: str, method: str = 'GET', headers: Dict[str, str] = None, 
                            data: str = None) -> str:
        """
        Generate curl commands for API testing
        
        Args:
            url: API endpoint URL
            method: HTTP method (GET, POST, PUT, DELETE)
            headers: Dictionary of headers
            data: Request body data
            
        Returns:
            Generated curl command
        """
        print("""
        
         ######  ##     ##    ###    ########  ######  ##     ## ########
        ##    ## ##     ##   ## ##      ##    ##    ## ###   ### ##     ##
        ##       ##     ##  ##   ##     ##    ##       #### #### ##     ##
        ##       ######### ##     ##    ##    ##       ## ### ## ##     ##
        ##       ##     ## #########    ##    ##       ##     ## ##     ##
        ##    ## ##     ## ##     ##    ##    ##    ## ##     ## ##     ##
         ######  ##     ## ##     ##    ##     ######  ##     ## ########
                            cURL Command Generator
        """)
        
        try:
            # Start building curl command
            curl_parts = ['curl']
            
            # Add method
            if method.upper() != 'GET':
                curl_parts.append(f'-X {method.upper()}')
            
            # Add headers
            if headers:
                for key, value in headers.items():
                    curl_parts.append(f'-H "{key}: {value}"')
            
            # Add data
            if data:
                curl_parts.append(f'-d \'{data}\'')
            
            # Add URL
            curl_parts.append(f'"{url}"')
            
            curl_command = ' '.join(curl_parts)
            
            print(f"cURL Command: {curl_command}")
            pyperclip.copy(curl_command)
            return curl_command
        except Exception as e:
            error_msg = f"Error generating curl command: {e}"
            print(error_msg)
            return error_msg


# Create instance
developer_tools = DeveloperTools()