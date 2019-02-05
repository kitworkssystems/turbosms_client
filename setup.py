#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='turbosms_client',
    version='1.0.1',
    description='TurboSMS Python SDK',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['zeep', ],
)
