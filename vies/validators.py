from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _


@deconstructible
class VATINValidator(object):
    """Validator for European VIES VAT Identification Number."""

    message = _('Not a valid European VAT number.')
    code = 'invalid'

    def __init__(self, verify=True, validate=False):
        if not (verify or validate):
            raise ValueError('"verify" and "validate" can not both be false.')
        self.verify = verify
        self.validate = validate

    def __call__(self, value):
        if self.verify:
            value.verify()
        if self.validate:
            value.validate()
