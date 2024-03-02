from setuptools import setup, find_packages


setup(
    name="Py-uTube",
    version="1.0",
    author="Ebraheem Alhetari",
    author_email="hetari4all@gmail.com",
    description="YouTube Downloader CLI",
    packages=find_packages(),
    install_requires=["pytube", "inquirer",
                      "yaspin", "requests", "rich", "inquirer", "termcolor"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={
        "console_scripts": [
            "uTube=uTube:cli.app",
            "utube=uTube:cli.app",
        ],
    },
    long_description=open("README.md").read(),
    python_requires=">=3.6",
    readme="README.md",
)
