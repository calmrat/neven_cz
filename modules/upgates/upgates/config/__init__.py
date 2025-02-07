# -*- coding: utf-8 -*-

"""
This module initializes configuration settings for the Abra application.

Usage:
    This module is automatically imported and executed to set up environment variables,
    logging, and directory paths for the application.

File:
    abra/config/__init__.py
"""

import os
import logging

import logfire

from pathlib import Path

from dotenv import load_dotenv

# Define helper functions
def expand_home(path):
    ''' Expand the user's home directory in a given path. '''
    if not path:
        path = Path.home()
    return Path(os.path.expanduser(path))

def init_dirs(paths) -> int:
    ''' Create directories if they do not exist. '''
    for path in paths:
        path = Path(path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    return 1 # success


# Load environment variables
load_dotenv()

# Python Logging
logging_enabled = os.getenv("LOGGING_ENABLED", "").lower() in ("1", "true") or False
logging_level = os.getenv("LOGGING_LEVEL", "").lower() or 'info'
debug = logging_level # alias
logging_level = logging.DEBUG if logging_level == 'debug' else logging.INFO

# Logfire Logging
logfire_enabled = os.getenv("LOGFIRE_ENABLED", "").lower() in ("1", "true") or True
logfire_consoloe_min_log_level = os.getenv("LOGFIRE_CONSOLE_MIN_LOG_LEVEL").lower() or 'info'
logfire_project = os.getenv("LOGFIRE_PROJECT", "neven-agents")

# CLI Settings
paralell_batch_size = int(os.getenv("PARALELL_BATCH_SIZE", 1))

# Upgates
upgates_api_url = os.getenv("UPGATES_API_URL", "")
upgates_login = os.getenv("UPGATES_LOGIN", "")
upgates_api_key = os.getenv("UPGATES_API_KEY", "")
upgates_sync_interveral_minutes = os.getenv("UPGATES_SYNC_INTERVAL_MINUTES", 10)
upgates_api_retry_limit = os.getenv("UPGATES_API_RETRY_LIMIT", 1)
upgates_verify_ssl = os.getenv("UPGATES_VERIFY_SSL", "").lower() in ("1", "true") or True

# Open AI
openai_enabled = os.getenv("OPENAI_ENABLED", "").lower() in ("1", "true") or True
openai_api_key = os.getenv("OPENAI_API_KEY", "")
openai_default_model = os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")
openai_default_retries = os.getenv("OPENAI_DEFAULT_RETRIES", 1)

# Define application filestystem paths
neven_path = Path(os.getenv("NEVEN_PATH", "~/.neven/"))

data_path = neven_path / "data"

input_path = data_path / "input"
output_path = data_path / "output"
logs_path = data_path / "logs"
db_path = data_path / "db"
cache_path = data_path / "cache"

db_file = __name__.split(".")[0] + ".db"
default_db_path = db_path / db_file

sys_dirs = [neven_path, data_path, input_path, output_path, logs_path, db_path, cache_path]

# Ensure default data path and subdirectories exist
init_dirs(sys_dirs)

# defaults
logger = None
debug_msg = "🟡 Debug mode is enabled."
info_msg = "🟠 Info mode is enabled."

if logging_enabled:    
    # Setup Logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    logger = logging.getLogger(__name__)

    if debug:    
        logger.setLevel(logging.DEBUG)
        logger.debug(f"LOGGING: {debug_msg}")
    else:
        logger.info(f"LOGGING: {debug_msg}")

if logfire_enabled:
    if debug:
        os.environ["LOGFIRE_CONSOLE_MIN_LOG_LEVEL"] = "debug"
    else:
        value = os.environ["LOGFIRE_CONSOLE_MIN_LOG_LEVEL"]
        os.environ["LOGFIRE_CONSOLE_MIN_LOG_LEVEL"] = "info" if not value else value

    logfire.configure()
    
    if debug:
        logfire.debug(f"LOGFIRE: {info_msg}")
    else:
        logfire.info(f"LOGFIRE: {info_msg}")




# Log paths
logging.debug(f"Default data path: {data_path}")
logging.debug(f"Input path: {input_path}")
logging.debug(f"Output path: {output_path}")
logging.debug(f"Logs path: {logs_path}")
logging.debug(f"Database path: {db_path}")
logging.debug(f"Default database path: {default_db_path}")

# EOF