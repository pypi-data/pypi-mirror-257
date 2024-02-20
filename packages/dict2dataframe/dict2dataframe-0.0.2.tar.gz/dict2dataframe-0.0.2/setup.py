#!/usr/bin/env python
# encoding: utf-8

# João Antunes <joao8tunes@gmail.com>
# https://github.com/joao8tunes

from setuptools import setup, find_packages

setup(
    name="dict2dataframe",
    version="0.0.2",
    author="João Antunes",
    description="Python package for converting JSON data into tabular format.",
    long_description_content_type="text/markdown",
    url="https://github.com/joao8tunes/dict2dataframe",
    packages=find_packages(),
    install_requires=[
        "coloredlogs",
        "openpyxl",
        "pandas",
        "pyarrow",
        "python-benedict",
        "xlrd"
    ],
    python_requires=">=3.7",
)
