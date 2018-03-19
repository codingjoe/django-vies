# -*- coding: utf-8 -*-
from __future__ import (unicode_literals, absolute_import)

import logging

__version__ = "3.5.0"

logger = logging.getLogger('vies')

VIES_WSDL_URL = str('http://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl')  # NoQA
VATIN_MAX_LENGTH = 14
