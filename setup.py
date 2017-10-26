#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="singer-best-practices-linter",
    version="0.1.0",
    description="Linter for Singer Taps",
    author="Buck Ryan",
    url="https://github.com/b-ryan/singer-best-practices-linter",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["linter"],
    entry_points="""
    [console_scripts]
    singer-best-practices-linter=singer_best_practices_linter:main
    """,
)
