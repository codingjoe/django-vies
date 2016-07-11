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


class TestValidatorsWithoutVATINObject(object):
    """Validate raw values without VATIN object from model field."""
    def test_valid(self):
        valid_vatin = ''.join([VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER])
        validator = VATINValidator()
        validator(valid_vatin)

        validator = VATINValidator(verify=False, validate=True)
        validator(valid_vatin)

        validator = VATINValidator(verify=True, validate=True)
        validator(valid_vatin)

    def test_invalid(self):
        invalid_number_vatin = ''.join([VALID_VIES_COUNTRY_CODE, '12345678'])
        invalid_country_vatin = ''.join(['XX', VALID_VIES_NUMBER])

        validator = VATINValidator()
        with pytest.raises(ValidationError):
            validator(invalid_country_vatin)

        validator = VATINValidator(verify=False, validate=True)
        with pytest.raises(ValidationError):
            validator(invalid_number_vatin)

        validator = VATINValidator(verify=True, validate=True)
        with pytest.raises(ValidationError):
            validator(invalid_country_vatin)

        with pytest.raises(ValidationError):
            validator(invalid_number_vatin)
