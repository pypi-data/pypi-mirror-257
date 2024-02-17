#!/usr/bin/env python
# coding=utf-8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nl-ego-cities',
    version='0.1.16',
    author="L.Z",
    author_email="zhangle@gmail.com",
    description="Data for Netherland Cities Coordinates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cheerzhang/NLGeoCities",
    project_urls={
        "Bug Tracker": "https://github.com/cheerzhang/NLGeoCities/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages("."),
    install_requires=[
        'pandas>=0.25.1',
        'numpy>=1.21.5',
        'cdifflib>=1.2.6'
    ],
    python_requires=">=3.11",
)