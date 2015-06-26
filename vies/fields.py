# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from suds import WebFault

from . import VATIN, VIES_COUNTRY_CHOICES
from .widgets import VATINHiddenWidget, VATINWidget


class VATINField(forms.MultiValueField):

    """VIES VAT field. That verifies on the fly."""

    hidden_widget = VATINHiddenWidget

    default_error_messages = {
        'invalid_vat': _('Not a valid European VAT number.'),
        'server_error': _('VIES check VAT service currently unavailable.'),
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
                is_valid = vatin.is_valid()
            except WebFault:
                raise ValidationError(
                    self.default_error_messages['server_error'],
                    code='server_error',
                    params={'value': value})
            except ValueError as e:
                raise ValidationError(e.message, code='invalid_country_code')
            if is_valid:
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
