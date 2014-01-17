# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='django-vies',
    version='0.1.0',
    description='European VIES VAT field for Django',
    author='codingjoe',
    url='https://github.com/codingjoe/django-vies',
    author_email='info@johanneshoppe.com',
    license='License :: OSI Approved :: MIT License',
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
    requires=['django (>=1.3.1)', 'requests (>=1.0.0)'],
)
