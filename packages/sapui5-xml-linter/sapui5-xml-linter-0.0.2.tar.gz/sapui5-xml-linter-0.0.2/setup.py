#!/usr/bin/env python3
""" Setup script for this package"""

from distutils.core import setup
import os

## The text of the README file
README_TEXT = ""
if os.path.exists("README.md"):
    with open("README.md") as fh:
        README_TEXT = fh.read()

setup(
    name = "sapui5-xml-linter",
    version = "0.0.2",
    description = "Checks SAPUI5 XML views for unnecessary attributes and empty tags",
    author = "Daniel Kullmann",
    author_email = "python@danielkullmann.de",
    url = "https://gitlab.com/danielkullmann/sapui5-xml-linter",
    packages = [],
    scripts = ["sapui5-xml-linter"],
    requires = ["lxml", "config_path"],
    license = "MIT",
    long_description=README_TEXT,
    long_description_content_type="text/markdown",
)
