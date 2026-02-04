# Django-VIES

Validate and store VAT Information Exchange System (VIES) data in Django.

## Installation

```shell
python3 -m pip install django-vies
```

## Usage

`VATINField` for models

```python
from django.db import models
from vies.models import VATINField


class Company(models.Model):
    name = models.CharField(max_length=100)
    vat = VATINField(blank=True, null=True)
```

`VATIN` wrapper class, allows access to result.

```python
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
```

You can also use the classmethod `VATIN.from_str` to create `VATIN` from
`str`.

```python
>>> from vies.types import VATIN
>>> vat = VATIN.from_str('LU26375245')
>>> vat.is_valid()
True
```

The VIES API endpoint can be very unreliable and seems to have an IP
based access limit. Therefore the `VATINField` does NOT perform API
based validation by default. It needs to be explicitly turned on or
performed in a separate task.

e.g.

```python
from vies.models import VATINField
from vies.validators import VATINValidator


class Company(models.Model):
    name = models.CharField(max_length=100)
    vat = VATINField(validators=[VATINValidator(verify=True, validate=True)])
```

`validate=True` will tell the validator to validate against the VIES
API. `verify` is enabled on by default and will only verify that the
VATIN matches the country's specifications.

It is recommended to perform VIES API validation inside an asynchronous
task.

e.g. using celery

```python
from celery import shared_task
from vies.models import VATINField
from vies.types import VATIN
from django.core.exceptions import ValidationError


class Company(models.Model):
    name = models.CharField(max_length=100)
    vat = VATINField()
    vat_is_valid = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)
        self.__vat = self.vat

    def save(self, *args, **kwargs):
        if self.__vat != self.vat:
            validate_vat_field.delay(self.pk)
        super(Company, self).save(*args, **kwargs)
        self.__vat = self.vat

    def refresh_from_db(self, *args, **kwargs):
        super(Company, self).refresh_from_db(*args, **kwargs)
        self.__vat = self.vat


@shared_task
def validate_vat_field(company_id):
    company = Company.objects.get(pk=company_id)
    vat = VATIN.from_str(company.vat)
    try:
        vat.validate()
    except ValidationError:
        company.vat_is_valid = False
    else:
        company.vat_is_valid = True
    finally:
        company.save(update_fields=["vat_is_valid"])
```

You can also use
`celery.current_app.send_task('validate_vat_field', kwargs={"company_id": self.pk})`
to call asynchronous task to avoid **circular import errors**.

## Translations

Feel free to contribute translations, it's simple!

```shell
cd vies
django-admin makemessages -l $YOUR_COUNTRY_CODE
```

Just edit the generated PO file. Pull-Requests are welcome!
