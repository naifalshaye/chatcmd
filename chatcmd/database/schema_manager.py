"""
Database schema management for ChatCMD
Handles database creation, migrations, and schema updates
"""

import sqlite3
import os
from typing import Dict, List, Optional, Any
from chatcmd.helpers.platform_utils import platform_utils


class SchemaManager:
    """Manages database schema and migrations"""
    
    def __init__(self, db_path: str = None):
        # Use secure cross-platform path if not provided
        if db_path is None:
            db_path = platform_utils.get_db_path()
        
        # Migrate from legacy location if needed
        legacy_paths = ['db.sqlite', 'chatcmd/db.sqlite']
        for legacy_path in legacy_paths:
            if os.path.exists(legacy_path) and not os.path.exists(db_path):
                platform_utils.migrate_legacy_db(legacy_path, db_path)
                break
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # Set secure file permissions
        platform_utils.set_secure_file_permissions(db_path)
        
        self._initialize_schema()
        # Added: schema versioning and write maintenance
        self._initialize_schema_versioning()
        self._write_count = 0
    
    def _initialize_schema(self):
        """Initialize database schema with all required tables"""
        self._create_ai_providers_table()
        self._create_model_configs_table()
        self._create_usage_stats_table()
        self._create_history_table()
        self._create_config_table()
        self._migrate_existing_data()
    
    def _initialize_schema_versioning(self):
        """Create schema versioning table and set initial version."""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS schema_version (
                    id INTEGER PRIMARY KEY CHECK (id = 1),
                    version INTEGER NOT NULL
                )
            ''')
            self.conn.commit()
            self.cursor.execute('SELECT version FROM schema_version WHERE id = 1')
            row = self.cursor.fetchone()
            if not row:
                self.cursor.execute('INSERT INTO schema_version (id, version) VALUES (1, 1)')
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Migration warning: {e}")
    
    def _create_ai_providers_table(self):
        """Create AI providers table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_providers (
                id INTEGER PRIMARY KEY,
                provider_name TEXT UNIQUE NOT NULL,
                api_key TEXT,
                base_url TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def _create_model_configs_table(self):
        """Create model configurations table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS model_configs (
                id INTEGER PRIMARY KEY,
                provider_id INTEGER,
                model_name TEXT NOT NULL,
                display_name TEXT,
                max_tokens INTEGER DEFAULT 100,
                temperature REAL DEFAULT 0.7,
                is_default BOOLEAN DEFAULT 0,
                cost_per_token REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (provider_id) REFERENCES ai_providers(id)
            )
        ''')
        self.conn.commit()
    
    def _create_usage_stats_table(self):
        """Create usage statistics table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_stats (
                id INTEGER PRIMARY KEY,
                provider_id INTEGER,
                model_name TEXT,
                tokens_used INTEGER,
                cost REAL,
                response_time REAL,
                success BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (provider_id) REFERENCES ai_providers(id)
            )
        ''')
        self.conn.commit()
    
    def _create_history_table(self):
        """Create command history table (existing table)"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY,
                prompt TEXT,
                command TEXT,
                model_name TEXT,
                provider_name TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def _create_config_table(self):
        """Create general configuration table (existing table)"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS config (
                id INTEGER PRIMARY KEY,
                api_key TEXT,
                current_model TEXT DEFAULT 'gpt-3.5-turbo',
                current_provider TEXT DEFAULT 'openai'
            )
        ''')
        self.conn.commit()
    
    def _migrate_existing_data(self):
        """Migrate existing data to new schema"""
        try:
            # Check if old config table exists and has data
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='config'")
            if self.cursor.fetchone():
                # Check if config table has the old structure
                self.cursor.execute("PRAGMA table_info(config)")
                columns = [column[1] for column in self.cursor.fetchall()]
                
                if 'api_key' in columns and 'current_model' not in columns:
                    # Migrate old API key to new structure
                    self.cursor.execute("SELECT api_key FROM config WHERE id = 1")
                    old_api_key = self.cursor.fetchone()
                    
                    if old_api_key and old_api_key[0]:
                        # Add OpenAI provider
                        self.add_provider('openai', old_api_key[0])
                        
                        # Update config table
                        self.cursor.execute('''
                            ALTER TABLE config ADD COLUMN current_model TEXT DEFAULT 'gpt-3.5-turbo'
                        ''')
                        self.cursor.execute('''
                            ALTER TABLE config ADD COLUMN current_provider TEXT DEFAULT 'openai'
                        ''')
                        self.conn.commit()
                        
        except sqlite3.Error as e:
            print(f"Migration warning: {e}")
    
    def add_provider(self, provider_name: str, api_key: str, base_url: str = None) -> int:
        """
        Add a new AI provider
        
        Args:
            provider_name: Name of the provider (openai, anthropic, etc.)
            api_key: API key for the provider
            base_url: Base URL for the provider (optional)
            
        Returns:
            Provider ID
        """
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO ai_providers (provider_name, api_key, base_url)
                VALUES (?, ?, ?)
            ''', (provider_name, api_key, base_url))
            self.conn.commit()
            self._post_write_maintenance()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error adding provider: {e}")
            return None
    
    def get_provider(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """
        Get provider information
        
        Args:
            provider_name: Name of the provider
            
        Returns:
            Provider information dictionary or None
        """
        try:
            self.cursor.execute('''
                SELECT id, provider_name, api_key, base_url, is_active
                FROM ai_providers WHERE provider_name = ?
            ''', (provider_name,))
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'id': result[0],
                    'provider_name': result[1],
                    'api_key': result[2],
                    'base_url': result[3],
                    'is_active': bool(result[4])
                }
            return None
        except sqlite3.Error as e:
            print(f"Error getting provider: {e}")
            return None
    
    def get_all_providers(self) -> List[Dict[str, Any]]:
        """
        Get all providers
        
        Returns:
            List of provider information dictionaries
        """
        try:
            self.cursor.execute('''
                SELECT id, provider_name, api_key, base_url, is_active
                FROM ai_providers ORDER BY provider_name
            ''')
            results = self.cursor.fetchall()
            
            return [{
                'id': row[0],
                'provider_name': row[1],
                'api_key': row[2],
                'base_url': row[3],
                'is_active': bool(row[4])
            } for row in results]
        except sqlite3.Error as e:
            print(f"Error getting providers: {e}")
            return []
    
    def update_provider_api_key(self, provider_name: str, api_key: str) -> bool:
        """
        Update provider API key
        
        Args:
            provider_name: Name of the provider
            api_key: New API key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cursor.execute('''
                UPDATE ai_providers 
                SET api_key = ?, updated_at = CURRENT_TIMESTAMP
                WHERE provider_name = ?
            ''', (api_key, provider_name))
            self.conn.commit()
            self._post_write_maintenance()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating provider API key: {e}")
            return False
    
    def set_current_model(self, model_name: str, provider_name: str) -> bool:
        """
        Set the current model and provider
        
        Args:
            model_name: Name of the model
            provider_name: Name of the provider
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO config (id, current_model, current_provider)
                VALUES (1, ?, ?)
            ''', (model_name, provider_name))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error setting current model: {e}")
            return False
    
    def get_current_model(self) -> Dict[str, str]:
        """
        Get the current model and provider
        
        Returns:
            Dictionary with current_model and current_provider
        """
        try:
            self.cursor.execute('''
                SELECT current_model, current_provider FROM config WHERE id = 1
            ''')
            result = self.cursor.fetchone()
            
            if result:
                return {
                    'current_model': result[0] or 'gpt-3.5-turbo',
                    'current_provider': result[1] or 'openai'
                }
            else:
                # Insert default values
                self.cursor.execute('''
                    INSERT INTO config (id, current_model, current_provider)
                    VALUES (1, 'gpt-3.5-turbo', 'openai')
                ''')
                self.conn.commit()
                return {
                    'current_model': 'gpt-3.5-turbo',
                    'current_provider': 'openai'
                }
        except sqlite3.Error as e:
            print(f"Error getting current model: {e}")
            return {
                'current_model': 'gpt-3.5-turbo',
                'current_provider': 'openai'
            }
    
    def add_usage_stat(self, provider_id: int, model_name: str, tokens_used: int, 
                      cost: float = None, response_time: float = None, success: bool = True):
        """
        Add usage statistics
        
        Args:
            provider_id: ID of the provider
            model_name: Name of the model used
            tokens_used: Number of tokens used
            cost: Cost of the request
            response_time: Response time in seconds
            success: Whether the request was successful
        """
        try:
            self.cursor.execute('''
                INSERT INTO usage_stats (provider_id, model_name, tokens_used, cost, response_time, success)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (provider_id, model_name, tokens_used, cost, response_time, success))
            self.conn.commit()
            self._post_write_maintenance()
        except sqlite3.Error as e:
            print(f"Error adding usage stat: {e}")
    
    def get_usage_stats(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get usage statistics for the last N days
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of usage statistics
        """
        try:
            self.cursor.execute('''
                SELECT p.provider_name, us.model_name, us.tokens_used, us.cost, 
                       us.response_time, us.success, us.created_at
                FROM usage_stats us
                JOIN ai_providers p ON us.provider_id = p.id
                WHERE us.created_at >= datetime('now', '-{} days')
                ORDER BY us.created_at DESC
            '''.format(days))
            
            results = self.cursor.fetchall()
            return [{
                'provider_name': row[0],
                'model_name': row[1],
                'tokens_used': row[2],
                'cost': row[3],
                'response_time': row[4],
                'success': bool(row[5]),
                'created_at': row[6]
            } for row in results]
        except sqlite3.Error as e:
            print(f"Error getting usage stats: {e}")
            return []
    
    def _post_write_maintenance(self):
        """Run periodic VACUUM/ANALYZE after N writes to keep SQLite healthy."""
        try:
            self._write_count += 1
            threshold = 50
            if self._write_count >= threshold:
                self.cursor.execute('ANALYZE;')
                self.cursor.execute('VACUUM;')
                self.conn.commit()
                self._write_count = 0
        except sqlite3.Error:
            pass
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()