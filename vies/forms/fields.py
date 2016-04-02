# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms

from vies.types import VATIN, VIES_COUNTRY_CHOICES
from vies.validators import VATINValidator

from .. import VATIN_MAX_LENGTH
from .widgets import VATINHiddenWidget, VATINWidget


class VATINField(forms.MultiValueField):

    hidden_widget = VATINHiddenWidget
    widget = VATINWidget

    def __init__(self, choices=VIES_COUNTRY_CHOICES, *args, **kwargs):
        max_length = kwargs.pop('max_length', VATIN_MAX_LENGTH)

        kwargs['widget'] = self.widget(choices=choices)
        kwargs.setdefault('validators', [VATINValidator()])

        fields = (
            forms.ChoiceField(required=False, choices=choices),
            forms.CharField(required=False, max_length=max_length)
        )

        super(VATINField, self).__init__(fields=fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return VATIN(*data_list)
