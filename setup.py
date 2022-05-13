"""Install packages as defined in this file into the Python environment."""
from setuptools import setup, find_packages

# The version of this tool is based on the following steps:
# https://packaging.python.org/guides/single-sourcing-package-version/
VERSION = {}

with open("./livekit/__init__.py") as fp:
    # pylint: disable=W0122
    exec(fp.read(), VERSION)

setup(
    name="livekit",
    author="Barton Ip",
    author_email="_livekit@barty.af",
    url="https://github.com/bartonip/livekit-server-sdk-py",
    description="A Python implementation of the LiveKit Server SDK",
    version=VERSION.get("__version__", "0.0.0"),
    packages=find_packages(where=".", exclude=["tests"]),
    install_requires=[
        "setuptools>=45.0",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.0",
        "Topic :: Utilities",
    ],
)