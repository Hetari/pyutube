from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="pyutube",
    version="0.1",
    install_requires=["pytube", "inquirer", "yaspin",
                      "requests", "rich", "inquirer", "termcolor"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
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
)
