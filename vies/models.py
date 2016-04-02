# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from . import VATIN_MAX_LENGTH, forms


class VATINField(CharField):
    """
    Database field for European VIES VAT Identification Number.

    This field stores and validates VATINs.

    Example::

        class MyModel(models.Model):
            vat = VATINField(_('EU VAT ID'))

    """

    description = _("A VIES VAT field.")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', VATIN_MAX_LENGTH)
        super(VATINField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.setdefault('form_class', forms.VATINField)
        return super(VATINField, self).formfield(**kwargs)
