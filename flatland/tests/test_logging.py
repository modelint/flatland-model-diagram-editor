"""This is just here to see if I logging works for submodules"""

import logging
import logging.config
from pathlib import Path

# log_conf_path = Path(__file__).parent.parent / 'log.conf'
# logging.config.fileConfig(fname=log_conf_path, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def doMessage():
    logger.debug('This is a debug message again')