# -*- coding: utf-8 -*-
from setuptools import setup, Command


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


setup(
    name='django-vies',
    version='0.2.1',
    description='European VIES VAT field for Django',
    author='codingjoe',
    url='https://github.com/codingjoe/django-vies',
    author_email='info@johanneshoppe.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Topic :: Office/Business :: Financial :: Accounting',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    packages=['vies'],
    include_package_data=True,
    requires=['django (>=1.3.1)', 'suds (>=0.4)'],
    cmdclass={'test': PyTest},
)
