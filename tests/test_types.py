import logging

import pytest
from django.core.exceptions import ValidationError
from mock import patch
from suds import WebFault

from tests import VALID_VIES_COUNTRY_CODE, VALID_VIES_IE, VALID_VIES_NUMBER
from vies.types import VATIN


class TestVATIN(object):
    def test_creation(self):
        VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)

    def test_str(self):
        assert "AB1234567890" == str(VATIN('AB', '1234567890'))

    def test_repr(self):
        assert "<VATIN AB1234567890>" == repr(VATIN('AB', '1234567890'))

    def test_verify(self):
        with pytest.raises(ValidationError) as e:
            VATIN('xx', VALID_VIES_NUMBER).verify()
        assert "XX is not a european member state." in e.value

        with pytest.raises(ValidationError) as e:
            VATIN('16', VALID_VIES_NUMBER).verify()
        assert "16 is not a valid ISO_3166-1 country code." in e.value

    def test_country_code_setter(self):
        v = VATIN(VALID_VIES_COUNTRY_CODE.lower(), VALID_VIES_NUMBER)
        assert v.country_code == VALID_VIES_COUNTRY_CODE

    def test_is_valid(self):
        v = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        assert v.is_valid()

        v = VATIN('XX', VALID_VIES_NUMBER)
        assert not v.is_valid()

    def test_result(self):
        v = VATIN('NL', '124851903B01')
        assert v.is_valid()
        assert v.data['countryCode'] == 'NL'
        assert v.data['vatNumber'] == '124851903B01'
        assert v.data['name'] == 'JIETER'

    def test_ie_regex_verification(self):
        for vn in VALID_VIES_IE:
            v = VATIN('IE', vn)
            v.verify()
        v = VATIN('IE', '1234567890')
        with pytest.raises(ValidationError) as e:
            v.verify()
        assert "IE1234567890 does not match the country's VAT ID specifications." in e.value

    def test_is_not_valid(self):
        """Invalid number."""
        vatin = VATIN('GB', '000000000')
        assert not vatin.is_valid()

    @patch('vies.types.Client')
    def test_raises_when_suds_web_fault(self, mock_client):
        """Raise an error if suds raises a WebFault."""
        mock_check_vat = mock_client.return_value.service.checkVat
        mock_check_vat.side_effect = WebFault(500, 'error')

        v = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)

        logging.getLogger('vies').setLevel(logging.CRITICAL)

        with pytest.raises(WebFault):
            v.validate()

        logging.getLogger('vies').setLevel(logging.NOTSET)

        mock_check_vat.assert_called_with(
            VALID_VIES_COUNTRY_CODE,
            VALID_VIES_NUMBER)


@pytest.mark.parametrize("number,expected_number", [
    ("DK99999999", "DK99 99 99 99"),  # DK
    ("FRXX999999999", "FRXX 999999999"),  # FR
    ("GB999 9999 73", "GB999 9999 73"),  # GB
    ("GB999999999 733", "GB999 9999 99 733"),  # GB
    ("GBGD001", "GBGD001"),  # GB
    ("GBHA599", "GBHA599"),  # GB
])
def test_formater(number, expected_number):
    v = VATIN(number[:2], number[2:])
    assert str(v) == expected_number
