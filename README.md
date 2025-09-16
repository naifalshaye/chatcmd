# ChatCMD #

[![PyPI version](https://img.shields.io/pypi/v/chatcmd.svg?style=flat-square)](https://pypi.org/project/chatcmd)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/chatcmd.svg?style=flat-square)](https://pypi.org/project/chatcmd)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://en.wikipedia.org/wiki/MIT_License)

#### **ChatCMD** is an open source AI-driven CLI-based command lookup using multiple AI models to lookup relevant CLI commands based on user input and other generating and lookup features. ####

#### Boost Your Productivity, ***Say Goodbye*** to Manual Searches ####

### What's New in 2.0
- Multi-provider workflow with unified model management (list models, model info, current model, performance stats)
- Provider-specific API key storage via secure keyring; legacy OpenAI flags kept for backward compatibility
- Optional length argument for `--random-password` (default 18)
- Enhanced, colored help and unified header output
- Stability and error handling improvements

## Features ##

### Core Features
- CLI-based command lookup using multiple AI models (OpenAI, Anthropic, Google, Cohere, Ollama)
- Generate SQL query using AI
- Generate a random user-agent
- Generate a random password
- Get your public IP address
- Get a color Hex code by describing the color
- Lookup HTTP Code
- Lookup any port number
- Auto copy command to clipboard
- Disable copy feature
- Store Data in Sqlite Database
- Add or update API keys for multiple providers
- Validate API keys
- Display API Keys
- Display last command
- Display last {number} of commands
- Delete last Command
- Delete last {number} of commands
- Display the total number of commands
- Clear all history records
- Display the database file size
- Clear and validate user inputs
- Clear and validate lookup results to ensure only valid CLI commands are returned
- Enhanced error handling with human-readable messages
- Display library information

#### Core Features Implementation Types

| Feature | Implementation | AI/API Usage | Description |
|---------|---------------|--------------|-------------|
| **CLI Command Lookup** | 🟢 AI-Powered | ✅ AI Models | Uses OpenAI, Anthropic, Google, Cohere, Ollama |
| **SQL Query Generation** | 🟢 AI-Powered | ✅ AI Models | AI generates SQL based on natural language |
| **Random User-Agent** | 🔴 Static Code | ❌ No AI | Uses predefined user-agent strings |
| **Random Password** | 🔴 Static Code | ❌ No AI | Uses Python's random library |
| **Public IP Address** | 🟡 External API | ⚠️ External Service | Uses external IP service (not AI) |
| **Color Hex Code** | 🔴 Static Code | ❌ No AI | Uses predefined color database |
| **HTTP Code Lookup** | 🔴 Static Code | ❌ No AI | Uses predefined HTTP status codes |
| **Port Lookup** | 🔴 Static Code | ❌ No AI | Uses predefined port database |
| **Database Operations** | 🔴 Static Code | ❌ No AI | Uses SQLite for local storage |
| **API Key Management** | 🔴 Static Code | ❌ No AI | Local storage and validation |
| **Command History** | 🔴 Static Code | ❌ No AI | Local database operations |
| **Clipboard Operations** | 🔴 Static Code | ❌ No AI | Uses pyperclip library |
| **Input Validation** | 🔴 Static Code | ❌ No AI | Regex and string validation |

**Summary:**
- **🟢 AI-Powered (2 features)**: CLI lookup and SQL generation
- **🔴 Static Code (10 features)**: Most core features work offline
- **🟡 External API (1 feature)**: IP address lookup only

### Developer Tools
- **Regex Pattern Generator** - Create regex patterns for common use cases
- **Base64 Encoder/Decoder** - Encode or decode base64 strings
- **UUID Generator** - Generate UUIDs in different formats
- **Timestamp Converter** - Convert between different timestamp formats
- **QR Code Generator** - Generate QR codes for text/URLs

#### Developer Tools Implementation Types

| Feature | Implementation | AI/API Usage | Benefits |
|---------|---------------|--------------|----------|
| **Regex Pattern Generator** | 🔴 Static Code | ❌ No AI | Instant response, predefined patterns |
| **Base64 Encoder/Decoder** | 🔴 Static Code | ❌ No AI | Fast, built-in Python library |
| **UUID Generator** | 🔴 Static Code | ❌ No AI | Fast, uses Python's uuid library |
| **Timestamp Converter** | 🔴 Static Code | ❌ No AI | Reliable, uses datetime library |
| **QR Code Generator** | 🟡 External API | ⚠️ External Service | Uses api.qrserver.com (not AI) |

**Key Benefits:**
- **86% Static Code**: Most tools work offline without API calls
- **No AI Costs**: Developer tools don't consume AI API credits
- **Fast Response**: Instant results without network latency
- **Reliable**: No dependency on external AI services
- **Offline Capable**: Works without internet (except QR codes)

### Multi-Model AI Support
- **OpenAI Models**: GPT-3.5 Turbo, GPT-4, GPT-4 Turbo
- **Anthropic Claude Models**: Claude 3 Haiku, Sonnet, Opus
- **Google Models**: Gemini Pro
- **Cohere Models**: Command, Command Light
- **Local Models (Ollama)**: Llama 2, Code Llama, Mistral, Llama 3.2 3B

## Requirements ##
    Python >= 3.8.9
    AI provider account and valid API key (OpenAI, Anthropic, Google, Cohere, or Ollama for local models)
    
    Get API keys:
    - OpenAI: https://platform.openai.com/signup
    - Anthropic: https://console.anthropic.com/
    - Google: https://makersuite.google.com/app/apikey
    - Cohere: https://dashboard.cohere.ai/
    - Ollama: https://ollama.ai/ (for local models)

## Installation ##
    pip3 install chatcmd
    
If pip not installed:

    python3 -m pip install chatcmd

Installation output should display:

    Collecting chatcmd
    Using cached chatcmd-2.0.1-py3-none-any.whl (6.8 kB)
    Installing collected packages: chatcmd
    Successfully installed chatcmd-2.0.1

### Upgrade ###
    pip3 install --upgrade chatcmd

If pip not installed:

    python3 -m pip install --upgrade chatcmd

### Uninstall ###
    pip3 uninstall chatcmd

If pip not installed:

    python3 -m pip uninstall chatcmd

## Quick Start ##

### 1. Set Up API Keys
```bash
# Set OpenAI API key
chatcmd --set-model-key openai

# Set Anthropic API key
chatcmd --set-model-key anthropic

# Set Google API key
chatcmd --set-model-key google

# Set Cohere API key
chatcmd --set-model-key cohere
```

### 2. List Available Models
```bash
chatcmd --list-models
```

### 3. Basic Usage
```bash
# Use default model (GPT-3.5 Turbo)
chatcmd --cmd

# Use specific model
chatcmd --model gpt-4 --cmd

# Generate a random password with custom length (default is 18)
chatcmd --random-password 24

```

## Usage ##

```
Usage:

chatcmd [options]

Core Features:
  -c, --cmd                         looking up a CLI command.
  -q, --sql                         generate SQL query.

Tools:
  --random-useragent                generate a random user-agent
  --get-ip                          get your public IP address.
  --random-password [<length>]      generate a random password (default: 18).
  --color-code                      get a color Hex code.
  --lookup-http-code                lookup HTTP Code by code number.
  --port-lookup                     lookup any port number.
  --regex-pattern                   generate regex pattern for description.
  --base64-encode                   encode text to base64.
  --base64-decode                   decode base64 text.
  --generate-uuid <version>         generate UUID (1, 3, 4, 5).
  --timestamp-convert <format>      convert timestamp (unix, iso, readable).
  --qr-code                         generate QR code for text/URL.

Library Options:
  -k, --set-key                     set or update API key (legacy OpenAI only).
  -o, --get-key                     display API key (legacy OpenAI only).
  -m, --model <model>               select AI model (gpt-3.5-turbo, gpt-4, claude-3-haiku, etc.)
  --list-models                     list all available AI models
  --model-info <model>              show information about a specific model
  --set-model-key <provider>        set API key for specific provider
  --get-model-key <provider>        get API key for specific provider
  --current-model                   show current model and provider
  --performance-stats               show model performance statistics
  -g, --get-cmd                     display the last command.
  -G, --get-last=<value>            display the last [number] of commands.
  -d, --delete-cmd                  delete the last command.
  -D, --delete-last-cmd=<value>     delete the last [number] of commands.
  -t, --cmd-total                   display the total number of commands.
  -r, --clear-history               clear all history records.
  -s, --db-size                     display the database size.
  -n, --no-copy                     disable copy feature.
  -h, --help                        display this screen.
  -v, --version                     display ChatCMD version.
  -x, --library-info                display library information.

```

## Usage Examples ##

### Basic CLI Command Lookup
```bash
# Use default model
chatcmd --cmd "find all files larger than 100MB"

# Use specific model
chatcmd --model gpt-4 --cmd "create a backup of my database"
```

### Developer Tools
```bash
# Generate regex pattern
chatcmd --regex-pattern "email validation"


# Generate UUID
chatcmd --generate-uuid 4

# Convert timestamp
chatcmd --timestamp-convert unix

# Generate QR code
chatcmd --qr-code
```

### Multi-Model Usage
```bash
# List available models
chatcmd --list-models

# Use Claude 3 Sonnet
chatcmd --model claude-3-sonnet --cmd

# Use local Llama 2 (requires Ollama)
chatcmd --model llama2 --cmd

# Check current model
chatcmd --current-model

# View performance statistics
chatcmd --performance-stats
```

### Provider Key Management
```bash
# Set API key for a specific provider (recommended)
chatcmd --set-model-key openai
chatcmd --set-model-key anthropic
chatcmd --set-model-key google
chatcmd --set-model-key cohere

# Get masked API key for a provider
chatcmd --get-model-key openai
```

### Local Models Setup (Ollama)
```bash
# Install Ollama
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull codellama
ollama pull mistral
ollama pull llama3.2:3b

# Use local models
chatcmd --model llama2 --cmd
chatcmd --model codellama --cmd
chatcmd --model llama3.2:3b --cmd
```

## Model Comparison ##

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| gpt-3.5-turbo | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | General use, fast responses |
| gpt-4 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | Complex commands, best quality |
| claude-3-haiku | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | Fast, good quality |
| claude-3-sonnet | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | Balanced performance |
| claude-3-opus | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | Best quality, complex tasks |
| gemini-pro | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | Google ecosystem |
| command | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Cost-effective |
| llama2 (local) | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Privacy, no API costs |
| codellama (local) | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Coding tasks, privacy |
| llama3.2:3b (local) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Small, fast local model |

## Error Codes ##
Include an exception message for each error if occurs.

| Code |             Description             |
|------|:-----------------------------------:|
| 1001 |          General exception          |
| 1002 |    Failed to connect to database    |
| 1003 | Failed to get API key from database |
| 1004 |      Failed to output API key       |
| 1005 | Failed to save API key to database  |
| 1006 |       Invalid ChatGPT API key       |
| 1007 |      Failed requesting API key      |
| 1008 |        Failed to add command        |
| 1009 |    API key is invalid or missing    |
| 1010 |      OpenAI API error occurred      |
| 1011 |      Lookup exception occurred      |
| 1012 |        Failed to add command        |
| 1013 |     Failed to get last command      |
| 1014 |    Failed to get list of command    |
| 1015 |    Failed deleting last command     |
| 1016 |     Failed to get last command      |
| 1017 |       Failed clearing history       |
| 1018 |       Failed to copy command        |

### Linux copy command issue
In order to perform a Graphics-related job in a Unix environment,
the DISPLAY variable needs to be set initially.
An error can occur when connecting to Linux via SSH, particularly if there is no copy/paste mechanism like Xclip installed.
To resolve this, you can try installing Xclip using the following command: "sudo apt-get install xclip".
Additionally, you need to export the DISPLAY variable by running: "export DISPLAY=:0.0".

To avoid the error message, you can use the "-no-copy" option when looking up a command, as it disables the copy feature.
## Support ##
[Issues](https://github.com/naifalshaye/chatcmd/issues)


Developed and maintained by:\
Naif Alshaye\
[https://naif.io](https://naif.io)\
naif@naif.io



## License
The MIT License (MIT). Please see License File [MIT License](https://choosealicense.com/licenses/mit/) for more information.