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
        max_length = kwargs.pop('max_length', 14)
        fields = (
            forms.ChoiceField(required=False, choices=choices),
            forms.CharField(required=False, max_length=max_length)
        )
        kwargs['widget'] = VATINWidget(choices=choices)
        super(VATINField, self).__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return "".join(data_list)
        return ''

    def clean(self, value):
        if not value or not isinstance(value, (list, tuple)):
            if not value or not [v for v in value if v not in self.empty_values]:
                if self.required:
                    raise ValidationError(self.error_messages['required'], code='required')
                else:
                    return self.compress([])
        else:
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