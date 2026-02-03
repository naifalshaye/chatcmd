"""
Constants for ChatCMD
Centralized configuration values to avoid magic numbers
"""

# Password generation
DEFAULT_PASSWORD_LENGTH = 18
MIN_PASSWORD_LENGTH = 1
MAX_PASSWORD_LENGTH = 1000

# AI model defaults
DEFAULT_MAX_TOKENS = 100
DEFAULT_SQL_MAX_TOKENS = 200
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MODEL = 'gpt-3.5-turbo'
DEFAULT_PROVIDER = 'openai'

# HTTP request timeouts (seconds)
HTTP_REQUEST_TIMEOUT = 3
OLLAMA_REQUEST_TIMEOUT = 30

# Input validation
MIN_PROMPT_WORDS = 3

# Statistics and history
DEFAULT_STATS_LOOKBACK_DAYS = 7
MAX_STATS_LOOKBACK_DAYS = 365

# Database maintenance
DB_VACUUM_THRESHOLD = 50

# API key masking
API_KEY_MASK_PREFIX_LENGTH = 8
API_KEY_MASK_SUFFIX_LENGTH = 4
API_KEY_MIN_LENGTH_FOR_MASK = 12

# Supported AI providers
SUPPORTED_PROVIDERS = ['openai', 'anthropic', 'google', 'cohere', 'ollama']

# Error codes
ERROR_CODES = {
    'NO_COMMANDS': 1012,
    'INVALID_NUMBER': 1013,
    'DELETE_FAILED': 1014,
    'DELETE_ERROR': 1015,
    'DELETE_RANGE_ERROR': 1016,
    'CLEAR_HISTORY_ERROR': 1017,
}
