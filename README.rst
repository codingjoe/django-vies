.. image:: https://travis-ci.org/codingjoe/django-vies.png?branch=master
    :target: https://travis-ci.org/codingjoe/django-vies
    :alt: TravisCI

.. image:: https://coveralls.io/repos/codingjoe/django-vies/badge.png?branch=master
    :target: https://coveralls.io/r/codingjoe/django-vies

.. image:: https://pypip.in/v/django-vies/badge.png
    :target: https://pypi.python.org/pypi/django-vies/
    :alt: Latest Version
    
.. image:: https://pypip.in/status/django-vies/badge.svg
    :target: https://pypi.python.org/pypi/django-vies/
    :alt: Development Status

.. image:: https://pypip.in/py_versions/django-vies/badge.svg
    :target: https://pypi.python.org/pypi/django-vies/
    :alt: Supported Python versions
    
.. image:: https://pypip.in/d/django-vies/badge.png
    :target: https://pypi.python.org/pypi//django-vies/
    :alt: Downloads

.. image:: https://pypip.in/license/django-vies/badge.png
    :target: https://pypi.python.org/pypi/django-vies/
    :alt: License


===========
Django-VIES
===========
Django-VIES is a django extension that allows storing VAT Information Exchange System (VIES) data in django models and validation.
Provided are a VATIN object, a ModelField and a FormField.

Installation
------------
Current Stable
::

    pip install django-vies

Latest Development
::

    pip install -e git://github.com/codingjoe/django-vies.git#egg=django-vies

Usage
-----

``VATINField`` for models
::

    from vies.models import VATINField


    class Company(models.Model):
        name = models.CharField(max_length=100)
        vat = VATINField(blank=True, null=True)

``VATIN`` wrapper class, allows access to result.
::

    >>> from vies import VATIN
    >>> vat = VATIN('NL', '124851903B01')
    >>> vat.is_valid()
    True
    >>> vat.result
    (reply){
       countryCode = "NL"
       vatNumber = "124851903B01"
       requestDate = 2014-03-25
       valid = True
       name = "JIETER"
       address = "(...)"
     }



License
-------
The MIT License (MIT)

Copyright (c) 2014 Johannes Hoppe

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
