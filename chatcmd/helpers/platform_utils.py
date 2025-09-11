"""
Cross-platform utilities for secure file and directory management
Ensures compatibility across Linux, macOS, and Windows
"""

import os
import platform
from pathlib import Path
from typing import Optional


class PlatformUtils:
    """Cross-platform utilities for secure file operations"""
    
    @staticmethod
    def get_user_data_dir() -> str:
        """
        Get cross-platform user data directory for storing application data
        
        Returns:
            Path to user data directory
        """
        system = platform.system()
        
        if system == "Windows":
            # Windows: %APPDATA%\chatcmd
            base_dir = os.environ.get('APPDATA', os.path.expanduser('~\\AppData\\Roaming'))
        elif system == "Darwin":
            # macOS: ~/Library/Application Support/chatcmd
            base_dir = os.path.expanduser('~/Library/Application Support')
        else:
            # Linux and others: ~/.local/share/chatcmd
            base_dir = os.path.expanduser('~/.local/share')
        
        data_dir = os.path.join(base_dir, 'chatcmd')
        return data_dir
    
    @staticmethod
    def ensure_secure_directory(path: str) -> bool:
        """
        Create directory with secure permissions (0o700)
        
        Args:
            path: Directory path to create
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs(path, mode=0o700, exist_ok=True)
            return True
        except (OSError, PermissionError) as e:
            print(f"Warning: Could not create secure directory {path}: {e}")
            return False
    
    @staticmethod
    def get_secure_db_path() -> str:
        """
        Get secure database path in user data directory
        
        Returns:
            Path to database file
        """
        data_dir = PlatformUtils.get_user_data_dir()
        PlatformUtils.ensure_secure_directory(data_dir)
        return os.path.join(data_dir, 'chatcmd.db')
    
    @staticmethod
    def set_secure_file_permissions(file_path: str) -> bool:
        """
        Set secure file permissions (0o600) - owner read/write only
        
        Args:
            file_path: Path to file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.chmod(file_path, 0o600)
            return True
        except (OSError, PermissionError) as e:
            print(f"Warning: Could not set secure permissions for {file_path}: {e}")
            return False
    
    @staticmethod
    def migrate_legacy_db(old_path: str, new_path: str) -> bool:
        """
        Migrate database from old location to new secure location
        
        Args:
            old_path: Old database path
            new_path: New database path
            
        Returns:
            True if migration successful, False otherwise
        """
        try:
            if os.path.exists(old_path) and not os.path.exists(new_path):
                import shutil
                shutil.copy2(old_path, new_path)
                PlatformUtils.set_secure_file_permissions(new_path)
                print(f"Database migrated from {old_path} to {new_path}")
                return True
            return True  # Already migrated or no old DB
        except Exception as e:
            print(f"Warning: Could not migrate database: {e}")
            return False
    
    @staticmethod
    def is_portable_mode() -> bool:
        """
        Check if running in portable mode (DB in current directory)
        
        Returns:
            True if portable mode detected
        """
        # Check if db.sqlite exists in current directory
        return os.path.exists('db.sqlite') or os.path.exists('chatcmd/db.sqlite')
    
    @staticmethod
    def get_db_path() -> str:
        """
        Get database path with fallback logic
        
        Returns:
            Path to database file
        """
        # If in portable mode, use local db
        if PlatformUtils.is_portable_mode():
            if os.path.exists('db.sqlite'):
                return 'db.sqlite'
            elif os.path.exists('chatcmd/db.sqlite'):
                return 'chatcmd/db.sqlite'
        
        # Use secure user data directory
        return PlatformUtils.get_secure_db_path()


# Create instance for easy import
platform_utils = PlatformUtils()
