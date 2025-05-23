import re

from django.core.exceptions import ValidationError
from django.utils.functional import cached_property
from django.utils.translation import gettext
from zeep import Client

from vies import VIES_WSDL_URL, logger


def dk_format(v):
    return f"{v[:4]} {v[4:6]} {v[6:8]} {v[8:10]}"


def fr_format(v):
    return f"{v[:4]} {v[4:]}"


VIES_OPTIONS = {
    "AT": ("Austria", re.compile(r"^ATU\d{8}$")),
    "BE": ("Belgium", re.compile(r"^BE(0|1)\d{9}$")),
    "BG": ("Bulgaria", re.compile(r"^BG\d{9,10}$")),
    "HR": ("Croatia", re.compile(r"^HR\d{11}$")),
    "CHE": ("Switzerland", re.compile(r"^CHE\d{9}$")),
    "CY": ("Cyprus", re.compile(r"^CY\d{8}[A-Z]$")),
    "CZ": ("Czech Republic", re.compile(r"^CZ\d{8,10}$")),
    "DE": ("Germany", re.compile(r"^DE\d{9}$")),
    "DK": ("Denmark", re.compile(r"^DK\d{8}$"), dk_format),
    "EE": ("Estonia", re.compile(r"^EE\d{9}$")),
    "EL": ("Greece", re.compile(r"^EL\d{9}$")),
    "ES": ("Spain", re.compile(r"^ES[A-Z0-9]\d{7}[A-Z0-9]$")),
    "FI": ("Finland", re.compile(r"^FI\d{8}$")),
    "FR": ("France", re.compile(r"^FR[A-HJ-NP-Z0-9][A-HJ-NP-Z0-9]\d{9}$"), fr_format),
    "HU": ("Hungary", re.compile(r"^HU\d{8}$")),
    "IE": ("Ireland", re.compile(r"^IE\d[A-Z0-9\+\*]\d{5}[A-Z]{1,2}$")),
    "IT": ("Italy", re.compile(r"^IT\d{11}$")),
    "LT": ("Lithuania", re.compile(r"^LT(\d{9}|\d{12})$")),
    "LU": ("Luxembourg", re.compile(r"^LU\d{8}$")),
    "LV": ("Latvia", re.compile(r"^LV\d{11}$")),
    "MT": ("Malta", re.compile(r"^MT\d{8}$")),
    "NL": ("The Netherlands", re.compile(r"^NL\d{9}B\d{2}$")),
    "PL": ("Poland", re.compile(r"^PL\d{10}$")),
    "PT": ("Portugal", re.compile(r"^PT\d{9}$")),
    "RO": ("Romania", re.compile(r"^RO\d{2,10}$")),
    "SE": ("Sweden", re.compile(r"^SE\d{10}01$")),
    "SI": ("Slovenia", re.compile(r"^SI\d{8}$")),
    "SK": ("Slovakia", re.compile(r"^SK\d{10}$")),
    "XI": ("Northern Ireland", re.compile(r"^XI\d{9}$")),
}

VIES_COUNTRY_CHOICES = sorted(
    (("", "--"),) + tuple((key, key) for key, value in VIES_OPTIONS.items())
)

MEMBER_COUNTRY_CODES = VIES_OPTIONS.keys()


class VATIN:
    """Object wrapper for the european VAT Identification Number."""

    def __init__(self, country_code, number):
        self.country_code = country_code
        self.number = number

    def __str__(self):
        unformated_number = f"{self.country_code}{self.number}"

        country = VIES_OPTIONS.get(self.country_code, {})
        if len(country) == 3:
            return country[2](unformated_number)
        return unformated_number

    def __repr__(self):
        return f"<VATIN {self.__str__()}>"

    def get_country_code(self):
        return self._country_code

    def set_country_code(self, value):
        self._country_code = value.upper()

    country_code = property(get_country_code, set_country_code)

    def get_number(self):
        return self._number

    def set_number(self, value):
        self._number = value.upper().replace(" ", "")

    number = property(get_number, set_number)

    @cached_property
    def data(self):
        """VIES API response data."""
        client = Client(VIES_WSDL_URL)
        try:
            return client.service.checkVat(self.country_code, self.number)
        except Exception as e:
            logger.exception(e)
            raise

    def is_valid(self):
        try:
            self.verify()
            self.validate()
        except ValidationError:
            return False
        else:
            return True

    def verify_country_code(self):
        if not re.match(r"^[a-zA-Z]", self.country_code):
            msg = gettext("%s is not a valid ISO_3166-1 country code.")
            raise ValidationError(msg % self.country_code)
        if self.country_code not in MEMBER_COUNTRY_CODES:
            msg = gettext("%s is not a european member state.")
            raise ValidationError(msg % self.country_code)

    def verify_regex(self):
        country = dict(
            map(
                lambda x, y: (x, y),
                ("country", "validator", "formatter"),
                VIES_OPTIONS[self.country_code],
            )
        )
        if not country["validator"].match(f"{self.country_code}{self.number}"):
            msg = gettext("%s does not match the country's VAT ID specifications.")
            raise ValidationError(msg % self)

    def verify(self):
        self.verify_country_code()
        self.verify_regex()

    def validate(self):
        if not self.data.valid:
            msg = gettext("%s is not a valid VATIN.")
            raise ValidationError(msg % self)

    @classmethod
    def from_str(cls, value):
        """Return a VATIN object by given string."""
        return cls(value[:2].strip(), value[2:].strip())
