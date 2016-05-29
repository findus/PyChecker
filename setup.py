import os
from setuptools import find_packages,setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "PyChecker",
    version = "0.0.1",
    author = "Philipp Hentschel",
    author_email = "",
    description = ("Basic tool to check Twitch Streams"),
    license = "",
    url = "https://github.com/Fozruk/PyChecker",
    packages=find_packages(exclude=['tests', 'tests.*']),
    long_description=read('README.md'),
        install_requires=[
        'wxPython',
        'setuptools',
        'notify2',
    ],
)
