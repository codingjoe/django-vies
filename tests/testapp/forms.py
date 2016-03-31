from django.forms import Form, ModelForm

from tests.testapp.models import EmptyVIESModel, VIESModel
from vies import fields


class VIESModelForm(ModelForm):
    class Meta:
        model = VIESModel
        exclude = []


class EmptyVIESModelForm(ModelForm):
    class Meta:
        model = EmptyVIESModel
        exclude = []


class VIESForm(Form):
    vat = fields.VATINField()


class EmptyVIESForm(Form):
    vat = fields.VATINField(required=False)


custom_error_16 = {
    'invalid_vat': '%(value)s is not a valid European VAT.'
}


class VIESFormCustomError16(Form):
    vat = fields.VATINField(error_messages=custom_error_16)

custom_error = {
    'invalid_vat': 'This VAT number is not valid'
}


class VIESFormCustomError(Form):
    vat = fields.VATINField(error_messages=custom_error)
