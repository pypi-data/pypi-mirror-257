#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

from setuptools import setup, find_packages


with open("README.md", mode="rt", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", mode="rt", encoding="utf-8") as f:
    requirements = [req.strip() for req in f.read().splitlines() if not req.strip().startswith('#')]

all_requirements = list(set(requirements))

setup(
    name="dict2dataframe",
    version="0.0.1",
    author="João Antunes",
    description="Python package for converting JSON data into tabular format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joao8tunes/dict2dataframe",
    packages=find_packages(),
    install_requires=all_requirements,
    python_requires=">=3.7",
)
