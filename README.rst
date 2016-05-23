.. image:: https://img.shields.io/badge/Django-CC-ee66dd.svg
    :target: https://github.com/codingjoe/django-cc

.. image:: https://img.shields.io/pypi/v/django-vies.svg
    :target: https://pypi.python.org/pypi/django-vies/

.. image:: https://travis-ci.org/codingjoe/django-vies.svg?branch=master
    :target: https://travis-ci.org/codingjoe/django-vies
    :alt: Iontinuous Integration

.. image:: https://landscape.io/github/codingjoe/django-vies/master/landscape.svg?style=flat
    :target: https://landscape.io/github/codingjoe/django-vies/master
    :alt: Code Health

.. image:: https://coveralls.io/repos/codingjoe/django-vies/badge.svg?branch=master
    :target: https://coveralls.io/r/codingjoe/django-vies
    :alt: Test Coverage

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

.. code:: shell

    pip install django-vies

Latest Development

.. code:: shell

    pip install -e git://github.com/codingjoe/django-vies.git#egg=django-vies

Usage
-----

``VATINField`` for models

.. code:: python

    from vies.models import VATINField


    class Company(models.Model):
        name = models.CharField(max_length=100)
        vat = VATINField(blank=True, null=True)

``VATIN`` wrapper class, allows access to result.

.. code:: python

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


The VIES API endpoint can be very unreliable and seems to have an IP based access limit.
Therefore the ``VATINField` does NOT perform API based validation by default. It needs
to be explicitly turned on or performed in a separate task.

e.g.

.. code:: python

    from vies.models import VATINField
    from vies.validators import VATINValidator


    class Company(models.Model):
        name = models.CharField(max_length=100)
        vat = VATINField(validators=VATINValidator(verify=True, validate=True))

``validate=True`` will tell the validator to validate against the VIES API.
``verify`` is enabled on by default and will only verify that the VATIN matches the countries specifications.

It is recommended to perform VIES API validation inside an asynchronous task.

e.g. using celery

.. code:: python

    from celery import shared_task
    from vies.models import VATINField
    from vies.validators import VATINValidator


    class Company(models.Model):
        name = models.CharField(max_length=100)
        vat = VATINField()
        vat_is_valid = models.BooleanField(default=False)

        def __init__(self, *args, **kwargs):
            self.__vat = self.vat
            super(Company, self).__init__(*args, **kwargs)

        def save(self, *args, **kwargs):
            if self.__vat != self.vat:
                validate_vat_field.delay(self)
            super(Company, self).save(*args, **kwargs)
            self.__vat = self.vat

        def refresh_from_db(self)
            super(Company, self).refresh_from_db()
            self.__vat = self.vat

    @shared_task
    def validate_vat_field(company):
        try:
            company.vat.validate()
        except ValidationError:
            self.vat_is_valid = False
        else:
            self.vat_is_valid = False
        finally:
            self.save()


Translations
------------

Feel free to contribute translations, it's simple!

.. code:: shell

    cd vies
    django-admin makemessages -l $YOUR_COUNTRY_CODE

Just edit the generated PO file. Pull-Requests are welcome!


License
-------
The MIT License (MIT)

Copyright (c) 2014-2016 Johannes Hoppe

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
