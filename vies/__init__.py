"""Validate and store VAT Information Exchange System (VIES) data in Django."""

import logging

from . import _version

logger = logging.getLogger("vies")

__version__ = _version.__version__
VERSION = _version.__version_tuple__

VIES_WSDL_URL = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
VATIN_MAX_LENGTH = 14
