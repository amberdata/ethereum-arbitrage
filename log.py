import logging
from logging.config import fileConfig
fileConfig('logging_config.ini')
logger = logging.getLogger()
