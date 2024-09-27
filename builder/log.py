import logging
from logging import config

logging.config.fileConfig("logging.conf")
LOG = logging.getLogger("default")
