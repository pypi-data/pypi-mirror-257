from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as fh:
    long_description = fh.read()

VERSION = '0.0.10'
DESCRIPTION = 'A Node Editor Library using PyQt5 Specialized in TMD'
LONG_DESCRIPTION = 'A package that allows building simple nodes, sockets, and edges.'

# Setting up
setup(
    name="tmd_editor",
    version=VERSION,
    author="DigiBrain4",
    description=DESCRIPTION,
    long_description=long_description,
    packages=find_packages(),
    install_requires=['PyQt5', 'QtPy'],
    keywords=['python', 'node', 'tmd_nodeeditor', 'editor', 'edges', 'sockets'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
