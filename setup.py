#!/usr/bin/env python
# vim: et ts=4 sw=4


from setuptools import setup, find_packages


setup(
    name="djappsettings",
    version="0.2.1",
    license="BSD",

    author="Adam Mckaig",
    author_email="adam.mckaig@gmail.com",

    description="Per-app default settings for Django",
    url="http://github.com/adammck/djappsettings",
    packages=find_packages(),
    test_suite='tests',
)
