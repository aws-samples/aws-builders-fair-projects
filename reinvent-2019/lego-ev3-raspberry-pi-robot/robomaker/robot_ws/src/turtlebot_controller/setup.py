# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
from setuptools import setup, find_packages

# Package meta-data.

NAME = 'turtlebot_controller'
REQUIRES_PYTHON = '>=3.5.0'

setup(
    name=NAME,
    version='0.0.1',
    packages=find_packages(),
    python_requires=REQUIRES_PYTHON,

    install_requires=[
        'annoy==1.8.3',
        'boto3==1.9.23',
        'futures==3.1.1',
        'gym==0.10.5',
        'matplotlib==2.0.2',
        'netifaces==0.10.7',
        'numpy==1.13.3',
        'pandas==0.20.2',
        'Pillow==8.3.2',
        'PyYAML==5.4',
        'scipy==0.19.0',
        'scikit-image==0.13.0',
        'tensorflow==2.5.3',
        'rospkg==1.1.7',
        'awsiotpythonsdk==1.4.7'
    ]
)
