# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db.models import CharField
from django.utils.translation import ugettext_lazy as _

from . import fields


class VATINField(CharField):

    description = _("A VIES VAT field.")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(VATINField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'form_class': fields.VATINField,
            'required': not (self.blank or self.null)
        }
        defaults.update(kwargs)
        return super(VATINField, self).formfield(**defaults)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [r"^vies\.models"])
except ImportError:
    pass
