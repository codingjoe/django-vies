.. image:: https://img.shields.io/pypi/v/django-vies.svg
    :target: https://pypi.python.org/pypi/django-vies/

.. image:: https://travis-ci.org/codingjoe/django-vies.png?branch=master
    :target: https://travis-ci.org/codingjoe/django-vies
    :alt: Iontinuous Integration

.. image:: https://landscape.io/github/codingjoe/django-vies/master/landscape.svg?style=flat
    :target: https://landscape.io/github/codingjoe/django-vies/master
    :alt: Code Health

.. image:: https://coveralls.io/repos/codingjoe/django-vies/badge.png?branch=master
    :target: https://coveralls.io/r/codingjoe/django-vies
    :alt: Test Coverage

.. image:: https://scrutinizer-ci.com/g/codingjoe/django-vies/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/codingjoe/django-vies/?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :alt: MIT License

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/codingjoe/django-vies
   :target: https://gitter.im/codingjoe/django-vies?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


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


Translations
------------

Feel free to contribute translations, it's simple!

```
cd vies
django-admin makemessages -l $YOUR_COUNTRY_CODE
```

Just edit the generated PO file. Pull-Requests are welcome!


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
