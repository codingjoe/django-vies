from warnings import warn
from django.db.models import CharField

from vies import fields


class VATINField(CharField):

    description = "A VIES VAT field."

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(VATINField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.VATINField}
        defaults.update(kwargs)
        return super(VATINField, self).formfield(**defaults)


class VIESField(VATINField):
    """Deprecated in favor of VATINField"""
    def __init__(self, *args, **kwargs):
        warn(DeprecationWarning, '%(class)s has been deprecated in favor of VATINField')
        super(VIESField, self).__init__(*args, **kwargs)