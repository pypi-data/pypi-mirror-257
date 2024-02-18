#!/usr/bin/env python3
# mypy: ignore-errors
"""Plotting and analysis tools for the ARTIS 3D supernova radiative transfer code."""
import importlib.util
from pathlib import Path

from setuptools import find_namespace_packages
from setuptools import setup
from setuptools_scm import get_version

spec = importlib.util.spec_from_file_location("commands", "./artistools/commands.py")
commands = importlib.util.module_from_spec(spec)
spec.loader.exec_module(commands)

setup(
    name="artistools",
    version=get_version(local_scheme="no-local-version"),
    author="ARTIS Collaboration",
    author_email="luke.shingles@gmail.com",
    packages=find_namespace_packages(where="."),
    package_dir={"": "."},
    package_data={"artistools": ["**/*.txt", "**/*.csv", "**/*.md", "matplotlibrc"]},
    url="https://www.github.com/artis-mcrt/artistools/",
    long_description=(Path(__file__).absolute().parent / "README.md").open().read(),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": commands.get_console_scripts(),
    },
)
