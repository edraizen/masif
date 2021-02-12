import os,sys
from setuptools import setup, find_packages

from distutils.core import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

import subprocess
from os import path

#install_dir = os.path.abspath(os.path.dirname(__file__))
#third_party_dir = os.path.join(install_dir, "third_party")

#os.environ["PYMESH_PATH"] = os.path.join(third_party_dir, "PyMesh")

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rb") as f:
        reqs = f.read().decode("utf-8")
    return reqs

packages = find_packages(exclude=("third_party", "data", "comparison"))
print(packages)

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
