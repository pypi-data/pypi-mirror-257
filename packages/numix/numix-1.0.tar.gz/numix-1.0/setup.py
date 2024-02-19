from setuptools import find_packages, setup
import re

with open("README.md", "r") as f:
    long_description = f.read()
    

def get_version():
    with open("mylib/__init__.py") as f:
        content = f.read()
        match = re.search(r"__version__ = \"(.*?)\"", content)
        if match:
            return match.group(1)
        else:
            raise RuntimeError("Could not find version in __init__.py")


setup(
    name="numix",
    version="1.0",
    description="random number generator with a twist",
    author="Abel Zecharias",
    package_dir={"": "numix"},
    packages=find_packages(where="numix"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abelzk/numix.git",
    author_email="abelzeki24@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
)

