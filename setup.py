#!/usr/bin/env python
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

long_description = "TIFFStack reader for ScanImage 5 (and 4)."


setup(
    name='tiffreader',
    version='0.1.0.dev1',
    description="A TIFF stack reader for scan image 4 and 5 tiff stacks.",
    long_description=long_description,
    author='Fabian Sinz',
    author_email='sinz@bcm.edu',
    license=" BSD",
    url='https://github.com/atlab/TIFFReader',
    keywords='Scientific Imaging',
    packages=['tiffreader'],
    install_requires=['numpy','tifffile'],
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved ::  BSD',
        'Topic :: Reader :: Front-Ends',
    ],
)
