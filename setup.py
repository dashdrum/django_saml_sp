

#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014, OneLogin, Inc.
# All rights reserved.

from setuptools import setup

setup(
    name='django_saml_sp',
    version='1.0',
    description='Basic SAML2 login for Django',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
    ],
    author='Matthew Rich',
    url='https://github.com/dashdrum/django_saml_sp',
    packages=['django_saml_sp'],
    install_requires=[
        'python3_saml'
    ],
    keywords='saml saml2 django python3',
)
