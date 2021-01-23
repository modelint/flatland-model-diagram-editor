"""
build_db_test.py – Ensure that we can build the database
"""
import logging
import logging.config
from pathlib import Path

from flatland.database.flatlanddb import FlatlandDB

def get_logger():
    """Initiate the logger"""
    log_conf_path = Path(__file__).parent.parent / 'log.conf'  # Logging configuration is in this file
    logging.config.fileConfig(fname=log_conf_path, disable_existing_loggers=False)
    return logging.getLogger(__name__)  # Create a logger for this module

logger = get_logger()
db = FlatlandDB(rebuild=True)