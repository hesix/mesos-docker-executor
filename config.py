__author__ = "qiang.he@chinacache.com"

import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger("log")
