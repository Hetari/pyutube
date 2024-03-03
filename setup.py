from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="pyutube",
    version="1.0.0",
    install_requires=["pytube", "inquirer", "yaspin", "typer",
                      "requests", "rich", "inquirer", "termcolor"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "pyutube=pyutube:cli.app",
            "utube=pyutube:cli.app",
        ],
    },
    python_requires=">=3.6",
    long_description=description,
    long_description_content_type="text/markdown",
    project_urls={
        "Homepage": "https://github.com/Hetari/pyutube",
    }
)
