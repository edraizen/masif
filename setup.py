import os,sys
from setuptools import setup, find_packages

from distutils.core import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info

import subprocess
from os import path

install_dir = os.path.abspath(os.path.dirname(__file__))
third_party_dir = os.path.join(install_dir, "third_party")

os.environ["PYMESH_PATH"] = os.path.join(third_party_dir, "PyMesh")

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname), "rb") as f:
        reqs = f.read().decode("utf-8")
    return reqs

# def update_submodules(mode):
#     assert mode in ["install", "develop", "egg_info"]
#     if path.exists('.git'):
#         subprocess.check_call(['git', 'submodule', 'update', '--init', '--recursive'])
#         third_party = next(os.walk(third_party_dir))[1]
#         for dependency in third_party:
#             dependency_dir = os.path.join(third_party_dir, dependency)
#             setup_script = os.path.join(dependency_dir, "setup.py")
#             if os.path.isfile(setup_script):
#                 try:
#                     subprocess.check_call(["pwd"], cwd=os.path.join(dependency_dir, "third_party"))
#                     subprocess.check_call([sys.executable, "build.py", "all"], cwd=os.path.join(dependency_dir, "third_party"))
#                 except subprocess.CalledProcessError:
#                     print(f"no {dependency} build")
#                     pass
#                 subprocess.check_call([sys.executable, "setup.py", "install"], cwd=dependency_dir)
#
# class SubmoduleInstallCommand(install):
#     def run(self):
#         update_submodules("install")
#         install.run(self)
#
# class SubmoduleDevelopCommand(develop):
#     def run(self):
#         update_submodules("develop")
#         develop.run(self)
#
# class SubmoduleEggInfoCommand(egg_info):
#     def run(self):
#         update_submodules("egg_info")
#         egg_info.run(self)

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
    # cmdclass={
    #     'install': SubmoduleInstallCommand,
    #     'develop': SubmoduleDevelopCommand,
    #     'egg_info': SubmoduleEggInfoCommand,
    # },
)
