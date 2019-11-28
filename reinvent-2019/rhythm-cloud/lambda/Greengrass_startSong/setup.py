#!/usr/bin/env python

"""
distutils/setuptools install script.
"""
import os
import re

from setuptools import setup, find_packages


ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r'''__version__ = ['"]([0-9.]+)['"]''')


requires = [
]


def get_version():
    init = open(os.path.join(ROOT,'greengrasssdk','__init__.py')).read()
    return VERSION_RE.search(init).group(1)


setup(
    name='greengrasssdk',
    version=get_version(),
    description='The AWS IoT Greengrass SDK for Python',
    long_description=open('README.rst').read(),
    author='Amazon Web Services',
    url='',
    scripts=[],
    packages=find_packages(),
    package_data={
        'greengrasssdk': [
        ]
    },
    include_package_data=True,
    install_requires=requires,
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
    ],
)
