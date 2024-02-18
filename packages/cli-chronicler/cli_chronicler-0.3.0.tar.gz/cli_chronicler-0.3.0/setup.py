from setuptools import setup, find_packages

setup(
    name="cli_chronicler",
    version="0.3.0",
    packages=find_packages(),
    entry_points={"console_scripts": ["punch = cli_chronicler:main"]}
)
