#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://centreonapi.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='centreonapi',
    version='0.2.0',
    description='Centreon Api for use Webservice in Centreon Web 2.8.0 or later',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Guillaume Watteeux',
    author_email='g@15x.fr',
    url='https://github.com/guillaumewatteeux/centreon-sdk-python',
    packages=find_packages(),
    package_dir={'centreonapi': 'centreonapi'},
    include_package_data=True,
    install_requires=[
        'requests',
        'bs4',
    ],
    license='Apache-2.0',
    zip_safe=False,
    keywords='centreonapi',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

