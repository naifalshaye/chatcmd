from setuptools import setup

with open('README.md') as f:
    readme = f.read()

setup(
    name="chatcmd",
    version="2.0.1",
    description="Open-source AI CLI for command lookup, SQL generation, and developer tools with multi-model support (OpenAI, Anthropic, Google, Cohere, Ollama).",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Naif Alshaye",
    author_email="naif@naif.io",
    url="https://github.com/naifalshaye/chatcmd",
    install_requires=[
        "docopt>=0.6.2,<0.7.0",
        "openai>=1.0.0,<2.0.0",
        "anthropic>=0.7.0,<1.0.0",
        "google-generativeai>=0.3.0,<1.0.0",
        "cohere>=4.0.0,<5.0.0",
        "pyperclip>=1.8.2,<2.0.0",
        "requests>=2.31.0,<3.0.0",
        "fake_useragent>=1.3.0,<2.0.0",
        "cryptography>=41.0.0,<43.0.0",
        "keyring>=23.0.0,<25.0.0"
    ],
)
