# -*- coding: utf-8 -*-

"""
This module initializes configuration settings for the Abra application.

Usage:
    This module is automatically imported and executed to set up environment variables,
    logging, and directory paths for the application.

File:
    abra/config/__init__.py
"""

import logging
import os

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


# Begin Main Execution Path

# Load environment variables
load_dotenv()

# Logfire
logfire_level = os.getenv("LOGFIRE_LEVEL", "info").lower()
logfire_project = os.getenv("LOGFIRE_PROJECT", "neven-agents")

# Set log level from environment or config file, default to "info"
#log_level: str = os.getenv("LOGFIRE_CONSOLE_MIN_LOG_LEVEL", config.get("logging", {}).get("log_level", "info"))
logfire.configure()

# Define application configuration settings
paralell_batch_size = os.getenv("PARALELL_BATCH_SIZE", 1)

# Upgates
upgates_api_url = os.getenv("UPGATES_API_URL", "")
upgates_login = os.getenv("UPGATES_LOGIN", "")
upgates_api_key = os.getenv("UPGATES_API_KEY", "")
upgates_sync_interveral_minutes = os.getenv("UPGATES_SYNC_INTERVAL_MINUTES", 10)
upgates_api_retry_limit = os.getenv("UPGATES_API_RETRY_LIMIT", 1)
upgates_verify_ssl = os.getenv("UPGATES_VERIFY_SSL", True)

# Open AI
openai_enabled = os.getenv("OPENAI_ENABLED", True)
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

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

if str(os.getenv("DEBUG")).lower() in ("1", "true"):
    logger.setLevel(logging.DEBUG)
    logger.debug("🟡 Debug mode is enabled.")
else:
    logger.setLevel(logging.INFO)
    logger.info("🟠 Info mode is enabled.")

# Log paths
logging.debug(f"Default data path: {data_path}")
logging.debug(f"Input path: {input_path}")
logging.debug(f"Output path: {output_path}")
logging.debug(f"Logs path: {logs_path}")
logging.debug(f"Database path: {db_path}")
logging.debug(f"Default database path: {default_db_path}")

# EOF