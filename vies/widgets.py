from django import forms
from django.forms.widgets import HiddenInput
import re

EMPTY_VALUES = (None, '')

VAT_CHOICES = (
    ('', '----------'),
    ('AT', 'AT-Austria'),
    ('BE', 'BE-Belgium'),
    ('BG', 'BG-Bulgaria'),
    ('CY', 'CY-Cyprus'),
    ('CZ', 'CZ-Czech Republic'),
    ('DE', 'DE-Germany'),
    ('DK', 'DK-Denmark'),
    ('EE', 'EE-Estonia'),
    ('EL', 'EL-Greece'),
    ('ES', 'ES-Spain'),
    ('FI', 'FI-Finland'),
    ('FR', 'FR-France '),
    ('GB', 'GB-United Kingdom'),
    ('HU', 'HU-Hungary'),
    ('IE', 'IE-Ireland'),
    ('IT', 'IT-Italy'),
    ('LT', 'LT-Lithuania'),
    ('LU', 'LU-Luxembourg'),
    ('LV', 'LV-Latvia'),
    ('MT', 'MT-Malta'),
    ('NL', 'NL-The Netherlands'),
    ('PL', 'PL-Poland'),
    ('PT', 'PT-Portugal'),
    ('RO', 'RO-Romania'),
    ('SE', 'SE-Sweden'),
    ('SI', 'SI-Slovenia'),
    ('SK', 'SK-Slovakia'),
)


class VatWidget(forms.MultiWidget):
    """docstring for VatWidget"""

    def __init__(self, choices=VAT_CHOICES, attrs=None):
        widgets = (
            forms.Select(choices=choices),
            forms.TextInput()
        )
        super(VatWidget, self).__init__(widgets, attrs)

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
                    empty, country, code = re.split('([a-zA-Z]+)', code)
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
                    empty, country, code = re.split('([a-zA-Z]+)', code)
                except:
                    pass
            return [country, code]
        return [None, None]


class VatHiddenWidget(VatWidget):
    """
    A Widget that splits vat input into two <input type="hidden"> inputs.
    """

    def __init__(self, attrs=None):
        widgets = (HiddenInput(attrs=attrs), HiddenInput(attrs=attrs))
        super(VatWidget, self).__init__(widgets, attrs)


