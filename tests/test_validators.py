import pytest
from django.core.exceptions import ValidationError

from tests import VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER
from vies.types import VATIN
from vies.validators import VATINValidator


class TestValidators(object):
    """Validate values with VATIN object and string values."""

    @pytest.mark.parametrize(
        "vatin",
        [
            VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER),
            "".join([VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER]),
        ],
    )
    def test_valid(self, vatin):
        validator = VATINValidator()
        validator(vatin)

        validator = VATINValidator(verify=False, validate=True)
        validator(vatin)

        validator = VATINValidator(verify=True, validate=True)
        validator(vatin)

    @pytest.mark.parametrize(
        "invalid_number_vatin",
        [
            VATIN(VALID_VIES_COUNTRY_CODE, "12345678"),
            "".join([VALID_VIES_COUNTRY_CODE, "12345678"]),
        ],
    )
    @pytest.mark.parametrize(
        "invalid_country_vatin",
        [VATIN("XX", VALID_VIES_NUMBER), "".join(["XX", VALID_VIES_NUMBER])],
    )
    def test_invalid(self, invalid_number_vatin, invalid_country_vatin):
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

    def test_no_check_exception(self):
        with pytest.raises(ValueError):
            VATINValidator(verify=False, validate=False)
