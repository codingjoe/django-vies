# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import)

import logging

__version__ = "3.0.0"

logger = logging.getLogger('vies')

logging.basicConfig(level=logging.ERROR)
logging.getLogger('suds.client').setLevel(logging.INFO)

VIES_WSDL_URL = str('http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl')  # NoQA
VATIN_MAX_LENGTH = 14
