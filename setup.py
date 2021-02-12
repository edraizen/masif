import os,sys
from setuptools import setup, find_packages

import subprocess
from os import path

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rb") as f:
        reqs = f.read().decode("utf-8")
    return reqs

packages = find_packages(exclude=("third_party", "data", "comparison"))

setup(
    name = "masif",
    version = "0.0.1",
    author = "Pablo Gainza",
    author_email = "edraizen@gmail.com",
    packages=packages,
    long_description=read('README.md'),
    install_requires=read("requirements.txt").splitlines(),
    include_package_data=True,
    entry_points = {
        "console_scripts": [
            "masif = masif:main",
        ]
    }
)
