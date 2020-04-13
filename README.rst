===========
Django-VIES
===========

Validate and store VAT Information Exchange System (VIES) data in Django.

Installation
------------

.. code:: shell

    python3 -m pip install django-vies

Usage
-----

``VATINField`` for models

.. code:: python

    from django.db import models
    from vies.models import VATINField

    class Company(models.Model):
        name = models.CharField(max_length=100)
        vat = VATINField(blank=True, null=True)

``VATIN`` wrapper class, allows access to result.

.. code:: python

    >>> from vies.types import VATIN
    >>> vat = VATIN('LU', '26375245')
    >>> vat.is_valid()
    True
    >>> vat.data
    {
        'countryCode': 'LU',
        'vatNumber': '26375245',
        'requestDate': datetime.date(2020, 4, 13),
        'valid': True,
        'name': 'AMAZON EUROPE CORE S.A R.L.',
        'address': '38, AVENUE JOHN F. KENNEDY\nL-1855  LUXEMBOURG'
    }


You can also use the classmethod ``VATIN.from_str`` to create ``VATIN``
from ``str``.

.. code:: python

    >>> from vies.types import VATIN
    >>> vat = VATIN.from_str('LU26375245')
    >>> vat.is_valid()
    True

The VIES API endpoint can be very unreliable and seems to have an IP based access limit.
Therefore the ``VATINField`` does NOT perform API based validation by default. It needs
to be explicitly turned on or performed in a separate task.

e.g.

.. code:: python

    from vies.models import VATINField
    from vies.validators import VATINValidator


    class Company(models.Model):
        name = models.CharField(max_length=100)
        vat = VATINField(validators=[VATINValidator(verify=True, validate=True)])

``validate=True`` will tell the validator to validate against the VIES API.
``verify`` is enabled on by default and will only verify that the VATIN matches the country's specifications.

It is recommended to perform VIES API validation inside an asynchronous task.

e.g. using celery

.. code:: python

    from celery import shared_task
    from vies.models import VATINField


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

        def refresh_from_db(self, *args, **kwargs)
            super(Company, self).refresh_from_db(*args, **kwargs)
            self.__vat = self.vat

    @shared_task
    def validate_vat_field(company):
        try:
            company.vat.validate()
        except ValidationError:
            company.vat_is_valid = False
        else:
            company.vat_is_valid = True
        finally:
            company.save(update_fields=['vat_is_valid'])


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
