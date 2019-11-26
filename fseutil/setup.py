#!/usr/bin/env python

import os
from codecs import open  # To use a consistent encoding

import setuptools

import fseutil

with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md")) as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="fseutil",
    version=fseutil.__version__,
    description="Fire Safety Engineering Utilities",
    author="Ian Fu",
    author_email="fuyans@gmail.com",
    url="https://github.com/fsepy/fseutil",
    download_url="https://github.com/fsepy/sfeprapy/archive/master.zip",
    keywords=["fire safety", "structural fire engineering"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["fseutil", "fseutil.lib"],
    install_requires=requirements,
    include_package_data=True,
    entry_points={"console_scripts": ["fseutil=fseutil.cli:main"]},
)
