from setuptools import setup, find_packages

setup(
    name='youtube_downloader',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'youtube-downloader=youtube_downloader.cli:main',
        ],
    },
)
