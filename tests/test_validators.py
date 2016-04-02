import pytest
from django.core.exceptions import ValidationError

from tests import VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER
from vies.types import VATIN
from vies.validators import VATINValidator


class TestValidators(object):
    def test_valid(self):
        validator = VATINValidator()
        vatin = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        validator(vatin)

        validator = VATINValidator(verify=False, validate=True)
        vatin = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        validator(vatin)

        validator = VATINValidator(verify=True, validate=True)
        vatin = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        validator(vatin)

    def test_no_check_exception(self):
        with pytest.raises(ValueError):
            VATINValidator(verify=False, validate=False)

    def test_invalid(self):
        validator = VATINValidator()
        vatin = VATIN('XX', VALID_VIES_NUMBER)
        with pytest.raises(ValidationError):
            validator(vatin)

        validator = VATINValidator(verify=False, validate=True)
        vatin = VATIN(VALID_VIES_COUNTRY_CODE, '12345678')
        with pytest.raises(ValidationError):
            validator(vatin)

        validator = VATINValidator(verify=True, validate=True)
        vatin = VATIN('XX', VALID_VIES_NUMBER)
        with pytest.raises(ValidationError):
            validator(vatin)

        vatin = VATIN(VALID_VIES_COUNTRY_CODE, '12345678')
        with pytest.raises(ValidationError):
            validator(vatin)
