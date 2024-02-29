from setuptools import setup, find_packages

setup(
    name='uTube',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'uTube=uTube.__main__:cli',
            'utube=uTube.__main__:cli',
        ],
    },
)
