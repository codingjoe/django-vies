from warnings import warn
from django import forms
from django.forms.widgets import HiddenInput
import re

from vies import VIES_COUNTRY_CHOICES

EMPTY_VALUES = (None, '')


class VATINWidget(forms.MultiWidget):
    """docstring for VATINWidget"""

    def __init__(self, choices=VIES_COUNTRY_CHOICES, attrs=None):
        widgets = (
            forms.Select(choices=choices),
            forms.TextInput()
        )
        super(VATINWidget, self).__init__(widgets, attrs)

    def value_from_datadict(self, data, files, name):
        value = [widget.value_from_datadict(data, files, name + '_%s' % i) for i, widget in enumerate(self.widgets)]
        try:
            country, code = value
            #the spaces and the dots are removed
            code = code.replace(".", "").replace(" ", "")
        except:
            return data.get(name, None)
        if code not in EMPTY_VALUES:
            if country in EMPTY_VALUES:
                try:
                    # ex. code="FR09443710785", country="".
                    empty, country, code = re.split('([a-zA-Z])', code)
                except:
                    return ['', code]
            else:
                #ex. code ="FR09443710785", country="FR".
                re_code = re.compile(r'^%s(\d+)$' % country)
                if re_code.match(code):
                    code = code.replace(country, "", 1)
            try:
                country = country.upper()
            except:
                pass
            return [country, code]

    def format_output(self, rendered_widgets):
        return "%s&nbsp;%s" % (rendered_widgets[0], rendered_widgets[1])

    def decompress(self, value):
        if value:
            try:
                country, code = value
            except:
                country = None
                code = value
            if country in EMPTY_VALUES:
                try:
                    empty, country, code = re.split('([a-zA-Z])', code)
                except:
                    pass
            return [country, code]
        return [None, None]


class VATINHiddenWidget(VATINWidget):
    """
    A Widget that splits vat input into two <input type="hidden"> inputs.
    """

    def __init__(self, attrs=None):
        widgets = (HiddenInput(attrs=attrs), HiddenInput(attrs=attrs))
        super(VATINWidget, self).__init__(widgets, attrs)


class VatWidget(VATINWidget):
    """Deprecated in favor of VATINWidget"""
    def __init__(self, choices=VIES_COUNTRY_CHOICES, attrs=None):
        warn(DeprecationWarning, '%(class)s has been deprecated in favor of VATINWidget')
        super(VatWidget, self).__init__(choices=choices, attrs=attrs)


class VatHiddenWidget(VATINHiddenWidget):
    """Deprecated in favor of VATINHiddenWidget"""
    def __init__(self, attrs=None):
        warn(DeprecationWarning, '%(class)s has been deprecated in favor of VATINHiddenWidget')
        super(VatHiddenWidget, self).__init__(attrs=attrs)