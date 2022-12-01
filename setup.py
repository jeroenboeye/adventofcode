"""Builds the aoc package from the aoc folder.

To do so run the command below in the root folder:
pip install -e .
"""
from setuptools import find_packages, setup

setup(
    name="aoc",
    version="1.0",
    packages=find_packages(),
    author="Jeroen Boeye",
    author_email="j.boeye@faktion.com",
    description="Advent of code helper functions.",
)
