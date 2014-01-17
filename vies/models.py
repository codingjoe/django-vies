from django.db.models import CharField

from vies import fields


class VIESField(CharField):

    description = "A VIES VAT field."

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(VIESField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': fields.VIESField}
        defaults.update(kwargs)
        return super(VIESField, self).formfield(**defaults)