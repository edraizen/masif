import os,sys
from setuptools import setup, find_packages

import subprocess
from os import path

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rb") as f:
        reqs = f.read().decode("utf-8")
    return reqs

def install_deps():
    """Reads requirements.txt and preprocess it
    to be feed into setuptools.

    This is the only possible way (we found)
    how requirements.txt can be reused in setup.py
    using dependencies from private github repositories.

    Links must be appendend by `-{StringWithAtLeastOneNumber}`
    or something like that, so e.g. `-9231` works as well as
    `1.1.0`. This is ignored by the setuptools, but has to be there.

    Warnings:
        to make pip respect the links, you have to use
        `--process-dependency-links` switch. So e.g.:
        `pip install --process-dependency-links {git-url}`

    Returns:
         list of packages and dependency links.
    """
    with open('requirements.txt', 'r') as f:
        default = f.readlines()
    new_pkgs = []
    links = []
    for resource in default:
        if 'git' in resource:
            pkg = resource.split('#')[-1]
            links.append(resource.strip() + '-9876543210')
            new_pkgs.append(pkg.replace('egg=', '').rstrip())
        else:
            new_pkgs.append(resource.strip())
    return new_pkgs, links

pkgs, new_links = install_deps()

packages = find_packages(exclude=("third_party", "data", "comparison"))

setup(
    name = "masif",
    version = "0.0.1",
    author = "Pablo Gainza",
    author_email = "edraizen@gmail.com",
    packages=packages,
    long_description=read('README.md'),
    install_requires=pkgs,
    dependency_links=new_links,
    include_package_data=True,
    entry_points = {
        "console_scripts": [
            "masif = masif:main",
        ]
    }
)
