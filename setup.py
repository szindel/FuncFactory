from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="funcfactory",
    author="Steven Zindel <steven.zindel@gmail.com>",
    description="Python package The FuncFactory! Easily adaptable production grade code on the fly.",
    long_description=long_description,
    version="0.1.0",
    packages=find_packages(include=["funcfactory", "funcfactory.*"]),
)
