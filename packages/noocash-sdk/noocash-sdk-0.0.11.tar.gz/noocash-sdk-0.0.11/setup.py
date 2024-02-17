import json
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("package.json", "r") as pkg:
    version = json.loads(pkg.read())["version"]
setup(
    name="noocash-sdk",
    version=version,
    author="Mitch Chanza",
    author_email="hello@mitch.guru",
    description="Python SDK for mobile money API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thepresidentafrica/money-sdks",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)
