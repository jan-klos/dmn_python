import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "dmn_python",
    version = "0.1.3",
    author = "Jan Klos",
    author_email = "janklos@protonmail.com",
    description = ("Python library enabling importing and exporting a DMN model (as an XML file) and visualizating it."),
    license = "GNU GENERAL PUBLIC LICENSE",
    keywords = ["dmn", "xml"],
    classifiers=[
        # License should match "license" above.
        "License :: OSI Approved :: GNU General Public License (GPL)",
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 4 - Beta",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    url = "https://github.com/jan-klos/dmn-python",
    packages = ['dmn_python'],
    install_requires = [
        'lxml',
        'graphviz',
        'IPython',
        'tabulate'
    ],
    python_requires = '>=3',
    long_description = read('README.txt'),
)
