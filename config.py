__author__ = "qiang.he@chinacache.com"

import logging
import logging.config

logging.config.fileConfig("/mesos-docker-executor/logging.conf")
logger = logging.getLogger("log")
