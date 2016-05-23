#!/usr/bin/env python
import os
import sys

from setuptools import setup

try:
    import django
except ImportError:
    django = None


if django and ('sdist' in sys.argv or 'develop' in sys.argv):
    try:
        os.chdir('vies')
        from django.core import management
        management.call_command('compilemessages')
    finally:
        os.chdir('..')


PACKAGE = "vies"
URL = "https://github.com/codingjoe/django-vies"
DESCRIPTION = __import__(PACKAGE).__doc__
VERSION = __import__(PACKAGE).__version__


setup(
    name='django-vies',
    version=VERSION,
    description=DESCRIPTION,
    author='codingjoe',
    url=URL,
    download_url=URL,
    author_email='info@johanneshoppe.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=[PACKAGE],
    include_package_data=True,
    install_requires=[
        'suds-jurko>=0.6',
        'retrying>=1.1.0',
    ],
)
