"""
Setup script for ldplayer package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="ldplayer",
    version="1.0.0",
    packages=find_packages(),
    description="This is a package for LDPlayer emulator control software. (unofficial)",
    author="sinmentis",
    maintainer="sinmentis",
    url="https://github.com/sinmentis/ldplayer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[]
)
