"""
This module contains the setup configuration for the pyutube package.
"""


from setuptools import find_packages, setup
from pyutube.utils import __version__


# Read the README file to use as the long description
with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

# Setup configuration
setup(
    name="pyutube",

    version=__version__,

    author="Ebraheem Alhetari",

    author_email="hetari4all@gmail.com",

    description="Awesome CLI to download YouTube videos (as video or audio)/shorts/playlists from the terminal",

    long_description=description,

    long_description_content_type="text/markdown",

    keywords=[
        "youtube",
        "download",
        "cli",
        "pyutube",
        "pytubefix",
        "pytube",
        "youtube-dl",
    ],

    license="MIT",

    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],


    include_package_data=True,
    package_data={"pyutube": ["finish.mp3"]},

    python_requires=">=3.6",

    install_requires=[
        "pytubefix",
        "inquirer",
        "yaspin",
        "typer",
        "requests",
        "rich",
        "inquirer",
        "termcolor",
        "moviepy",
        "playsound"
    ],


    entry_points={
        "console_scripts": [
            "pyutube=pyutube:cli.app",
        ],
    },


    project_urls={
        "Author": "https://github.com/Hetari",
        "Homepage": "https://github.com/Hetari/pyutube",
        "Bug Tracker": "https://github.com/Hetari/pyutube/issues",
        "Source Code": "https://github.com/Hetari/pyutube",
        "Documentation": "https://github.com/Hetari/pyutube",
    },

    platforms=["Linux", "Windows", "MacOS"],
    packages=find_packages()
)
