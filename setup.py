#!/usr/bin/env python
# vim: et ts=4 sw=4


from setuptools import setup, find_packages


setup(
    name="djappsettings",
    version="0.3.0",
    license="BSD",

    author="Adam Mckaig",
    author_email="adam.mckaig@gmail.com",

    description="Per-app default settings for Django",
    url="http://github.com/adammck/djappsettings",
    packages=find_packages(exclude=['app_with_import_error']),
    test_suite='tests',
    classifiers=[
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Framework :: Django',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
    ],
)
