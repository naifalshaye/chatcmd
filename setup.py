from setuptools import setup,find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="chatcmd",
    version="1.1.8",
    description="ChatCMD is an AI-driven CLI-based command lookup using ChatGPT to lookup relevant CLI commands based on user input.",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Naif Alshaye",
    author_email="naif@naif.io",
    url="https://github.com/naifalshaye/chatcmd",
    install_requires=[
        "docopt",
        "openai",
        "pyperclip"
    ],
)