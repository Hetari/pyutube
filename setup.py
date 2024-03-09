from setuptools import setup, find_packages


# Read the README file to use as the long description
with open("README.md", "r") as f:
    description = f.read()

# Setup configuration
setup(
    # Name of the package
    name="pyutube",

    # Version of the package
    version="1.0.0",

    # Required dependencies
    install_requires=[
        "pytube",
        "inquirer",
        "yaspin",
        "typer",
        "requests",
        "rich",
        "inquirer",
        "termcolor"
    ],

    # Classifiers to categorize the package
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],

    # Entry points for console scripts
    entry_points={
        "console_scripts": [
            "pyutube=pyutube:cli.app",  # Command to run the application
        ],
    },

    # Python version requirement
    python_requires=">=3.6",

    # Long description of the package
    long_description=description,

    # Description content type
    long_description_content_type="text/markdown",

    # Project URLs
    project_urls={
        "Homepage": "https://github.com/Hetari/pyutube",
    }
)
