import logging
import re

from suds import WebFault
from suds.client import Client


# logging.basicConfig(level=logging.ERROR)
# logging.getLogger('suds.client').setLevel(logging.DEBUG)

VIES_WSDL_URL = 'http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl'

VIES_COUNTRY_CHOICES = (
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


def dk_format(v):
    return '%s %s %s %s' % (v[:4], v[4:6], v[6:8], v[8:10])


def gb_format(v):
    if len(v) == 11:
        return '%s %s %s' % (v[:5], v[5:9], v[9:11])
    if len(v) == 14:
        return '%s %s' % (gb_format(v[:11]), v[11:14])
    return v


def fr_format(v):
    return '%s %s' % (v[:4], v[4:])


VIES_OPTIONS = {
    'AT': (u"Austria", re.compile(r'^ATU\d{8}$')),
    'BE': (u"Belgium", re.compile(r'^BE0?\d{9}$')),
    'BG': (u"Bulgaria", re.compile(r'^BG\d{9,10}$')),
    'CY': (u"Cyprus", re.compile(r'^CY\d{8}[A-Z]$')),
    'CZ': (u"Czech Republic", re.compile(r'^CZ\d{8,10}$')),
    'DE': (u"Germany", re.compile(r'^DE\d{9}$')),
    'DK': (u"Denmark", re.compile(r'^DK\d{8}$'), dk_format),
    'EE': (u"Estonia", re.compile(r'^EE\d{9}$')),
    'EL': (u"Greece", re.compile(r'^EL\d{9}$')),
    'ES': (u"Spain", re.compile(r'^ES[A-Z0-9]\d{7}[A-Z0-9]$')),
    'FI': (u"Finland", re.compile(r'^FI\d{8}$')),
    'FR': (u"France", re.compile(r'^FR[A-HJ-NP-Z0-9][A-HJ-NP-Z0-9]\d{9}$'), fr_format),
    'GB': (u"United Kingdom", re.compile(r'^(GB(GD|HA)\d{3}|GB\d{9}|GB\d{12})$'), gb_format),
    'HU': (u"Hungary", re.compile(r'^HU\d{8}$')),
    'IE': (u"Ireland", re.compile(r'^IE\d[A-Z0-9\+\*]\d{5}[A-Z]$')),
    'IT': (u"Italy", re.compile(r'^IT\d{11}$')),
    'LT': (u"Lithuania", re.compile(r'^LT(\d{9}|\d{12})$')),
    'LU': (u"Luxembourg", re.compile(r'^LU\d{8}$')),
    'LV': (u"Latvia", re.compile(r'^LV\d{11}$')),
    'MT': (u"Malta", re.compile(r'^MT\d{8}$')),
    'NL': (u"The Netherlands", re.compile(r'^NL\d{9}B\d{2}$')),
    'PL': (u"Poland", re.compile(r'^PL\d{10}$')),
    'PT': (u"Portugal", re.compile(r'^PT\d{9}$')),
    'RO': (u"Romania", re.compile(r'^RO\d{2,10}$')),
    'SE': (u"Sweden", re.compile(r'^SE\d{10}01$')),
    'SI': (u"Slovenia", re.compile(r'^SI\d{8}$')),
    'SK': (u"Slovakia", re.compile(r'^SK\d{10}$')),
}

MEMBER_COUNTRY_CODES = VIES_OPTIONS.keys()


class VATIN(object):
    """
    Object wrapper for the european VAT Identification Number
    """

    _country_code = None

    @property
    def country_code(self):
        return self._country_code[:2].upper()

    _number = None

    @property
    def number(self):
        return self._number.upper()

    def __init__(self, country_code, number):
        self._country_code = country_code
        self._number = number

        try:
            if self._validate():
                self.client = Client(VIES_WSDL_URL)
        except ValueError, e:
            raise e

    def is_valid(self):
        return self._verify() if self._validate() else False

    def _validate(self):
        if not re.match(r'^[a-zA-Z]', self.country_code):
            raise ValueError('%s is not a valid ISO_3166-1 country code.' % (self.country_code))
        elif not self.country_code in MEMBER_COUNTRY_CODES:
            raise ValueError('%s is not a VIES member country.' % (self.country_code))

        country = dict(map(None, ('country', 'validator', 'formatter'), VIES_OPTIONS[self.country_code]))
        return country['validator'].match('%s%s' % (self.country_code, self.number))

    def _verify(self):
        try:
            result = self.client.service.checkVat(self.country_code, self.number)
            return result.valid
        except WebFault:
            raise ValueError('%s is not a valid ISO_3166-1 country code.' % (self.country_code))