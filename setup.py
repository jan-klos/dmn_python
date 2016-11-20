    import os
    from setuptools import setup

    def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

    setup(
        name = "dmn_python",
        version = "0.1.0",
        author = "Jan Klos",
        author_email = "janklos@protonmail.com",
        description = ("Python library enabling importing and exporting a DMN model (as an XML file) and visualizating it."),
        license = "GNU GENERAL PUBLIC LICENSE",
        keywords = ["dmn", "xml"],
        url = "https://github.com/jan-klos/dmn-python",
        download_url="https://github.com/jan-klos/dmn-python/tarball/0.1.0",
        packages=['dmn_python'],
        install_requires=[
            'lxml',
            'graphviz',
            'IPython',
            'tabulate'
        ],
        long_description=read('README.txt'),
    )