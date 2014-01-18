from warnings import warn
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from vies import VATIN, VIES_COUNTRY_CHOICES
from vies.widgets import VATINWidget, VATINHiddenWidget


class VATINField(forms.MultiValueField):
    """VIES VAT field. That verifies on the fly."""
    hidden_widget = VATINHiddenWidget

    def __init__(self, choices=VIES_COUNTRY_CHOICES, *args, **kwargs):
        # Set 'required' to False on the individual fields, because the
        # required validation will be handled by MultiValueField, not by those
        # individual fields.
        fields = (
            forms.ChoiceField(required=True, choices=choices),
            forms.CharField(required=True),
        )
        for f in fields:
            f.required = False
        widget = VATINWidget(choices=choices)

        #  Pop 'max_length' if send by ModelForm helper.
        kwargs.pop('max_length', None)
        super(VATINField, self).__init__(widget=widget, fields=fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return "".join(data_list)
        return None

    def clean(self, value):
        try:
            vatin = VATIN(*value)
            if vatin.is_valid():
                return super(VATINField, self).clean(value)
            else:
                raise ValidationError(_('%(value)s is not a valid European VAT.'), code='invalid',
                                      params={'value': self.compress(value)})
        except ValueError:
            raise ValidationError(_('%(value)s is not a valid European VAT.'), code='invalid',
                                  params={'value': self.compress(value)})


class VIESField(VATINField):
    """Deprecated in favor of VATINField"""
    def __init__(self, *args, **kwargs):
        warn(DeprecationWarning, '%(class)s has been deprecated in favor of VATINField')
        super(VIESField, self).__init__(*args, **kwargs)