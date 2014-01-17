from django import forms
from django.core.exceptions import ValidationError
import requests
from django.utils.translation import ugettext_lazy as _

from vies.widgets import VatWidget, VAT_CHOICES, VatHiddenWidget


class VIESField(forms.MultiValueField):
    """VIES VAT field. That verifies on the fly."""
    hidden_widget = VatHiddenWidget

    def __init__(self, choices=VAT_CHOICES, *args, **kwargs):
        # Set 'required' to False on the individual fields, because the
        # required validation will be handled by MultiValueField, not by those
        # individual fields.
        fields = (
            forms.ChoiceField(required=True, choices=choices),
            forms.CharField(required=True),
        )
        for f in fields:
            f.required = False
        widget = VatWidget(choices=choices)

        #  Pop 'max_length' if send by ModelForm helper.
        kwargs.pop('max_length', None)
        super(VIESField, self).__init__(widget=widget, fields=fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return "".join(data_list)
        return None

    def clean(self, value):
        r = requests.get('http://isvat.appspot.com/%s/%s/' % (value[0], value[1]))
        if r.text == 'true':
            return super(VIESField, self).clean(value)
        else:
            raise ValidationError(_('%(value)s is not a valid European VAT.'), code='invalid',
                                  params={'value': self.compress(value)})