#!/usr/bin/env python
from setuptools import setup, Command
import sys, os


class PyTest(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        import subprocess

        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)


# When creating the sdist, make sure the django.mo file also exists:
if 'sdist' in sys.argv or 'develop' in sys.argv:
    try:
        os.chdir('vies')
        from django.core import management
        management.call_command('compilemessages')
    finally:
        os.chdir('..')

setup(
    name='django-vies',
    version='2.1.3',
    description='European VIES VAT field for Django',
    author='codingjoe',
    url='https://github.com/codingjoe/django-vies',
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
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    packages=['vies'],
    include_package_data=True,
    install_requires=['suds-jurko>=0.6', 'retrying>=1.1.0'],
    cmdclass={'test': PyTest},
)
