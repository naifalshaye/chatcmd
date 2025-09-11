"""
Secure API key storage with cross-platform keyring support
Falls back to encrypted local storage if keyring is unavailable
"""

import os
import base64
import json
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from chatcmd.helpers.platform_utils import platform_utils

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False


class SecureStorage:
    """Secure storage for API keys with cross-platform support"""
    
    SERVICE_NAME = "chatcmd"
    
    def __init__(self):
        self.keyring_available = KEYRING_AVAILABLE
        self.encryption_key = self._get_or_create_encryption_key()
    
    def _get_or_create_encryption_key(self) -> Optional[bytes]:
        """Get or create encryption key for local storage fallback"""
        try:
            key_file = os.path.join(platform_utils.get_user_data_dir(), '.encryption_key')
            
            if os.path.exists(key_file):
                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                # Generate new key
                key = Fernet.generate_key()
                os.makedirs(os.path.dirname(key_file), exist_ok=True)
                with open(key_file, 'wb') as f:
                    f.write(key)
                # Set secure permissions
                platform_utils.set_secure_file_permissions(key_file)
                return key
        except Exception:
            return None
    
    def store_api_key(self, provider: str, api_key: str) -> bool:
        """
        Store API key securely
        
        Args:
            provider: Provider name (openai, anthropic, etc.)
            api_key: API key to store
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.keyring_available:
                # Use keyring for secure storage
                keyring.set_password(self.SERVICE_NAME, provider, api_key)
                return True
            else:
                # Fallback to encrypted local storage
                return self._store_encrypted_key(provider, api_key)
        except Exception as e:
            print(f"Warning: Could not store API key securely: {e}")
            return False
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Retrieve API key securely
        
        Args:
            provider: Provider name
            
        Returns:
            API key or None if not found
        """
        try:
            if self.keyring_available:
                return keyring.get_password(self.SERVICE_NAME, provider)
            else:
                return self._get_encrypted_key(provider)
        except Exception:
            return None
    
    def delete_api_key(self, provider: str) -> bool:
        """
        Delete API key
        
        Args:
            provider: Provider name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.keyring_available:
                keyring.delete_password(self.SERVICE_NAME, provider)
                return True
            else:
                return self._delete_encrypted_key(provider)
        except Exception:
            return False
    
    def _store_encrypted_key(self, provider: str, api_key: str) -> bool:
        """Store API key in encrypted local file"""
        try:
            if not self.encryption_key:
                return False
            
            fernet = Fernet(self.encryption_key)
            encrypted_key = fernet.encrypt(api_key.encode())
            
            keys_file = os.path.join(platform_utils.get_user_data_dir(), 'api_keys.enc')
            keys_data = {}
            
            # Load existing keys
            if os.path.exists(keys_file):
                with open(keys_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                keys_data = json.loads(decrypted_data.decode())
            
            # Add new key
            keys_data[provider] = base64.b64encode(encrypted_key).decode()
            
            # Save encrypted keys
            encrypted_data = fernet.encrypt(json.dumps(keys_data).encode())
            with open(keys_file, 'wb') as f:
                f.write(encrypted_data)
            
            platform_utils.set_secure_file_permissions(keys_file)
            return True
        except Exception:
            return False
    
    def _get_encrypted_key(self, provider: str) -> Optional[str]:
        """Retrieve API key from encrypted local file"""
        try:
            if not self.encryption_key:
                return None
            
            keys_file = os.path.join(platform_utils.get_user_data_dir(), 'api_keys.enc')
            if not os.path.exists(keys_file):
                return None
            
            fernet = Fernet(self.encryption_key)
            
            with open(keys_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)
            keys_data = json.loads(decrypted_data.decode())
            
            if provider in keys_data:
                encrypted_key = base64.b64decode(keys_data[provider])
                return fernet.decrypt(encrypted_key).decode()
            
            return None
        except Exception:
            return None
    
    def _delete_encrypted_key(self, provider: str) -> bool:
        """Delete API key from encrypted local file"""
        try:
            if not self.encryption_key:
                return False
            
            keys_file = os.path.join(platform_utils.get_user_data_dir(), 'api_keys.enc')
            if not os.path.exists(keys_file):
                return True
            
            fernet = Fernet(self.encryption_key)
            
            with open(keys_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = fernet.decrypt(encrypted_data)
            keys_data = json.loads(decrypted_data.decode())
            
            if provider in keys_data:
                del keys_data[provider]
                
                if keys_data:
                    # Save remaining keys
                    encrypted_data = fernet.encrypt(json.dumps(keys_data).encode())
                    with open(keys_file, 'wb') as f:
                        f.write(encrypted_data)
                else:
                    # No keys left, delete file
                    os.remove(keys_file)
            
            return True
        except Exception:
            return False
    
    def is_available(self) -> bool:
        """Check if secure storage is available"""
        return self.keyring_available or self.encryption_key is not None


# Create instance for easy import
secure_storage = SecureStorage()
