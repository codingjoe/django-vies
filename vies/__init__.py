"""Validate and store VAT Information Exchange System (VIES) data in Django."""

import logging

from . import _version  # noqa

logger = logging.getLogger("vies")

__version__ = _version.__version__
VERSION = _version.VERSION_TUPLE

VIES_WSDL_URL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"  # NoQA
VATIN_MAX_LENGTH = 14
