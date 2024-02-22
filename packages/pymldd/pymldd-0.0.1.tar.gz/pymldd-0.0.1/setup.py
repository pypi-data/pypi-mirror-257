# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - Intelligentica (Morocco)
Email: a.benmhamed@intelligentica.net
Website: https://intelligentica.net
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pymldd",
    version="0.0.1",
    author="Abdelouahed Ben Mhamed",
    author_email="a.benmhamed@intelligentica.net",
    description="A Python library for solving combinatorial optimization using Multivalued  Decision Diagrams and Machine Learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AIM-BENMHAMED/pymldd",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        # Add any dependencies your library may have
    ],
    entry_points={
        "console_scripts": [
            # If your library includes any command-line scripts, add them here
        ],
    },
)
