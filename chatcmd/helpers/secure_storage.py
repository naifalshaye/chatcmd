"""
Secure API key storage with cross-platform keyring support
Falls back to encrypted local storage if keyring is unavailable
"""

import os
import stat
import base64
import json
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from chatcmd.helpers.platform_utils import platform_utils

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False

# Keyring service name for storing encryption key
ENCRYPTION_KEY_SERVICE = "chatcmd_encryption"
ENCRYPTION_KEY_USERNAME = "encryption_key"


class SecureStorage:
    """Secure storage for API keys with cross-platform support"""

    SERVICE_NAME = "chatcmd"

    def __init__(self):
        self.keyring_available = KEYRING_AVAILABLE and self._test_keyring()
        self.encryption_key = self._get_or_create_encryption_key()

    def _test_keyring(self) -> bool:
        """Test if keyring is actually functional"""
        try:
            # Try a simple keyring operation to verify it works
            keyring.get_password(self.SERVICE_NAME, "__test_keyring__")
            return True
        except Exception:
            return False

    def _get_or_create_encryption_key(self) -> Optional[bytes]:
        """
        Get or create encryption key.
        Priority: 1) Keyring, 2) Encrypted file with permission checks
        """
        try:
            # Try to get key from keyring first (most secure)
            if self.keyring_available:
                stored_key = keyring.get_password(ENCRYPTION_KEY_SERVICE, ENCRYPTION_KEY_USERNAME)
                if stored_key:
                    return stored_key.encode()

                # Generate new key and store in keyring
                key = Fernet.generate_key()
                keyring.set_password(ENCRYPTION_KEY_SERVICE, ENCRYPTION_KEY_USERNAME, key.decode())
                return key

            # Fallback to file-based key with security checks
            key_file = os.path.join(platform_utils.get_user_data_dir(), '.encryption_key')

            if os.path.exists(key_file):
                # Verify file permissions before reading
                if not self._verify_file_permissions(key_file):
                    print("Warning: Encryption key file has insecure permissions. Refusing to read.")
                    return None

                with open(key_file, 'rb') as f:
                    return f.read()
            else:
                # Generate new key with atomic write
                key = Fernet.generate_key()
                self._atomic_write_file(key_file, key)
                return key
        except Exception:
            return None

    def _verify_file_permissions(self, file_path: str) -> bool:
        """Verify file has secure permissions (owner-only read/write)"""
        try:
            if os.name == 'nt':  # Windows
                return True  # Windows uses ACLs, skip check

            file_stat = os.stat(file_path)
            mode = file_stat.st_mode

            # Check if group or others have any permissions
            if mode & (stat.S_IRWXG | stat.S_IRWXO):
                return False

            # Verify owner matches current user
            if file_stat.st_uid != os.getuid():
                return False

            return True
        except Exception:
            return False

    def _atomic_write_file(self, file_path: str, content: bytes) -> bool:
        """Write file atomically using temp file + rename"""
        try:
            dir_path = os.path.dirname(file_path)
            os.makedirs(dir_path, mode=0o700, exist_ok=True)

            # Write to temp file first
            fd, temp_path = tempfile.mkstemp(dir=dir_path)
            try:
                os.write(fd, content)
                os.close(fd)

                # Set secure permissions on temp file
                os.chmod(temp_path, 0o600)

                # Atomic rename
                os.replace(temp_path, file_path)
                return True
            except Exception:
                # Clean up temp file on failure
                try:
                    os.close(fd)
                except Exception:
                    pass
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                raise
        except Exception:
            return False
    
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
        """Store API key in encrypted local file with atomic write"""
        try:
            if not self.encryption_key:
                return False

            fernet = Fernet(self.encryption_key)
            encrypted_key = fernet.encrypt(api_key.encode())

            keys_file = os.path.join(platform_utils.get_user_data_dir(), 'api_keys.enc')
            keys_data = {}

            # Load existing keys with permission check
            if os.path.exists(keys_file):
                if not self._verify_file_permissions(keys_file):
                    print("Warning: API keys file has insecure permissions.")
                    return False

                with open(keys_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = fernet.decrypt(encrypted_data)
                keys_data = json.loads(decrypted_data.decode())

            # Add new key
            keys_data[provider] = base64.b64encode(encrypted_key).decode()

            # Save encrypted keys atomically
            encrypted_data = fernet.encrypt(json.dumps(keys_data).encode())
            return self._atomic_write_file(keys_file, encrypted_data)
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

            # Verify file permissions before reading
            if not self._verify_file_permissions(keys_file):
                print("Warning: API keys file has insecure permissions. Refusing to read.")
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

            # Verify file permissions before modifying
            if not self._verify_file_permissions(keys_file):
                print("Warning: API keys file has insecure permissions.")
                return False

            fernet = Fernet(self.encryption_key)

            with open(keys_file, 'rb') as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)
            keys_data = json.loads(decrypted_data.decode())

            if provider in keys_data:
                del keys_data[provider]

                if keys_data:
                    # Save remaining keys atomically
                    encrypted_data = fernet.encrypt(json.dumps(keys_data).encode())
                    return self._atomic_write_file(keys_file, encrypted_data)
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
