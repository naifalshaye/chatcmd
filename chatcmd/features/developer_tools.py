"""
Developer tools and utilities for ChatCMD
Additional features useful for software engineers and developers
"""

import base64
import uuid
import re
import datetime
import requests
import pyperclip
from typing import Dict, List, Optional, Any
from urllib.parse import quote


class DeveloperTools:
    """Collection of developer-focused tools and utilities"""
    
    def __init__(self):
        self.qr_api_url = "https://api.qrserver.com/v1/create-qr-code/"
    
    
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
    
    


# Create instance
developer_tools = DeveloperTools()