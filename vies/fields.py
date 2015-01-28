# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import)

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from . import VATIN, VIES_COUNTRY_CHOICES
from .widgets import VATINWidget, VATINHiddenWidget


class VATINField(forms.MultiValueField):
    """VIES VAT field. That verifies on the fly."""
    hidden_widget = VATINHiddenWidget

    default_error_messages = {
        'invalid_vat': _('This is not a valid European VAT number.')
    }

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
            value = ''.join(data_list)
            try:
                vatin = VATIN(*data_list)
            except ValueError as e:
                raise ValidationError(str(e), code='error', params={'value': value})
            if vatin.is_valid():
                self._vies_result = vatin.result
            else:
                raise ValidationError(
                    self.error_messages['invalid_vat'], 
                    code='invalid_vat',
                    params={'value': value})
        else:
            value = ''
        return value

    def vatinData(self):
        return self._vies_result if hasattr(self, '_vies_result') else None
