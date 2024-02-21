"""Setup script for sietch"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sietch",
    version="0.2.0",
    author="GandalfsDad",
    description="Lightweight environment & cli tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GandalfsDad/sietch",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click",
    ],
    packages=find_packages(),
    entry_points={"console_scripts": ["sietch=sietch.cli.main:cli"]},
)
