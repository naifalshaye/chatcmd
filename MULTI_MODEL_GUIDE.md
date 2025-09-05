# ChatCMD Multi-Model Support Guide

ChatCMD now supports multiple AI models for CLI command lookup! This guide shows you how to use the new multi-model features.

## Supported AI Models

### OpenAI Models
- **gpt-3.5-turbo** - Fast and efficient (default)
- **gpt-4** - Most capable model
- **gpt-4-turbo** - Latest GPT-4 with improved performance

### Anthropic Claude Models
- **claude-3-haiku** - Fast and efficient Claude model
- **claude-3-sonnet** - Balanced Claude model for most tasks
- **claude-3-opus** - Most capable Claude model

### Google Models
- **gemini-pro** - Google's advanced language model

### Cohere Models
- **command** - Cohere's instruction-following model
- **command-light** - Faster Cohere model for simple tasks

### Local Models (Ollama)
- **llama2** - Local Llama 2 model via Ollama
- **codellama** - Local Code Llama model for coding tasks
- **mistral** - Local Mistral model via Ollama

## Quick Start

### 1. List Available Models
```bash
chatcmd --list-models
```

### 2. Set Up API Keys
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

### 3. Select a Model
```bash
# Use GPT-4
chatcmd --model gpt-4 --lookup-cmd

# Use Claude 3 Sonnet
chatcmd --model claude-3-sonnet --lookup-cmd

# Use Gemini Pro
chatcmd --model gemini-pro --lookup-cmd
```

### 4. Check Current Model
```bash
chatcmd --current-model
```

## New CLI Options

### Model Management
- `--list-models` - List all available AI models
- `--model <model>` - Select specific AI model
- `--model-info <model>` - Show information about a model
- `--current-model` - Show current model and provider

### API Key Management
- `--set-model-key <provider>` - Set API key for specific provider
- `--get-model-key <provider>` - Get API key for specific provider

### Performance & Statistics
- `--performance-stats` - Show model performance statistics

## Usage Examples

### Basic Command Lookup
```bash
# Use default model (GPT-3.5 Turbo)
chatcmd --lookup-cmd

# Use specific model
chatcmd --model gpt-4 --lookup-cmd

# Disable clipboard copying
chatcmd --model claude-3-haiku --no-copy
```

### Model Information
```bash
# List all models
chatcmd --list-models

# Get info about a specific model
chatcmd --model-info gpt-4

# Check current model
chatcmd --current-model
```

### API Key Management
```bash
# Set API key for OpenAI
chatcmd --set-model-key openai

# Set API key for Anthropic
chatcmd --set-model-key anthropic

# Check if API key is set
chatcmd --get-model-key openai
```

### Performance Monitoring
```bash
# View performance statistics
chatcmd --performance-stats
```

## Setting Up Local Models (Ollama)

### 1. Install Ollama
```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai/download
```

### 2. Pull Models
```bash
# Pull Llama 2
ollama pull llama2

# Pull Code Llama
ollama pull codellama

# Pull Mistral
ollama pull mistral
```

### 3. Use Local Models
```bash
# Use local Llama 2
chatcmd --model llama2 --lookup-cmd

# Use local Code Llama
chatcmd --model codellama --lookup-cmd
```

## Model Comparison

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

## Tips for Best Results

### 1. Choose the Right Model
- **For speed**: Use `gpt-3.5-turbo` or `claude-3-haiku`
- **For quality**: Use `gpt-4` or `claude-3-opus`
- **For privacy**: Use local models like `llama2` or `codellama`
- **For cost**: Use `command` or local models

### 2. Model-Specific Prompts
Different models may respond better to different prompt styles:
- **OpenAI**: Works well with direct, clear prompts
- **Claude**: Responds well to conversational prompts
- **Google**: Good with technical, structured prompts
- **Cohere**: Effective with instruction-based prompts

### 3. Performance Monitoring
Use `--performance-stats` to track:
- Response times
- Success rates
- Model usage patterns

## Troubleshooting

### Common Issues

1. **"No API key found"**
   - Use `--set-model-key <provider>` to configure your API key

2. **"Model not supported"**
   - Check available models with `--list-models`
   - Ensure you're using the correct model name

3. **"Invalid API key"**
   - Verify your API key is correct
   - Check if the API key has the right permissions

4. **Local model not working**
   - Ensure Ollama is running: `ollama serve`
   - Check if the model is pulled: `ollama list`

### Getting Help

- Check model info: `chatcmd --model-info <model>`
- View current configuration: `chatcmd --current-model`
- Check performance: `chatcmd --performance-stats`

## Migration from Single Model

The new multi-model system is fully backward compatible:

1. **Existing API keys** are automatically migrated
2. **Default behavior** remains the same (GPT-3.5 Turbo)
3. **All existing commands** work without changes
4. **New features** are opt-in

## Advanced Configuration

### Custom Model Parameters
You can customize model parameters in the configuration:

```python
# In model_config.py
'gpt-4': ModelInfo(
    name='gpt-4',
    max_tokens=150,  # Increase for longer commands
    temperature=0.5,  # Lower for more consistent results
    # ...
)
```

### Provider-Specific Settings
Some providers support additional configuration:

```bash
# Ollama with custom base URL
chatcmd --model llama2 --lookup-cmd
# (Ollama runs on http://localhost:11434 by default)
```

## Contributing

Want to add support for more AI models? Check out the provider implementation in `chatcmd/providers/` and follow the `BaseAIProvider` interface.

---

**Happy command hunting with multiple AI models! 🚀**