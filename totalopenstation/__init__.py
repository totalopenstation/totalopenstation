# -*- coding: utf-8 -*-

__version__  = '0.5.dev'

import logging
from pprint import pformat

def geo_to_debug(data):
    logger = logging.getLogger("tops")
    for f in data:
        formatted = pformat(f.__geo_interface__)
        for line in formatted.splitlines():
            logger.debug(line.rstrip())
