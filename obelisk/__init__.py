import logging
from logging import basicConfig

from .transform import *


logger = basicConfig(
    format='%(levelname)s:%(asctime)s:%(name)s:%(message)s',
    level=logging.INFO
)
