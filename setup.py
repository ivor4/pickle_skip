# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 20:46:02 2023

@author: Jaime Bonache < http://www.github.com/ivor4/pickle_skip > < jaime.bonache.iv4@gmail.com >
"""
import os

from setuptools import setup, find_packages

with open(os.path.join("pickle_skip", "version.txt")) as file_handler:
    __version__ = file_handler.read().strip()

setup(
    name='pickle_skip',
    version=__version__,
    author='Jaime Bonache',
    author_email='jaime.bonache.iv4@gmail.com',
    description='A short workaround to observe full content of attributes with Variable Explorer from Spyder avoinding Pickle erorrs for some types. If you use this library, please give Like at github :)',
    package_data={"pickle_skip": ["version.txt"]},
    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)

