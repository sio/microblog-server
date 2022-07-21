import logging
import os

log = logging.getLogger(__package__)
logging.basicConfig(
    level=logging.DEBUG if 'DEBUG' in os.environ else logging.INFO,
    format='%(levelname)-8s %(message)s',
)
