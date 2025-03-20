# -*- coding: utf-8 -*-

"""
This module initializes configuration settings for the Abra application.

Usage:
    This module is automatically imported and executed to set up environment variables,
    logging, and directory paths for the application.

File:
    /Users/cward/Repos/neven_cz/modules/abra/abra/config/__init__.py
"""

import logging
import os

from pathlib import Path
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Setup Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

if str(os.getenv("DEBUG")).lower() in ("1", "true"):
    logger.setLevel(logging.DEBUG)
    logger.debug("🟡 Debug mode is enabled.")
else:
    logger.setLevel(logging.INFO)
    logger.info("🟠 Info mode is enabled.")

def expand_home(path):
    if not path:
        path = Path.home()
    return Path(os.path.expanduser(path))

# Define paths
neven_path = Path(os.getenv("NEVEN_PATH", "~/.neven"))

data_path = neven_path / "data"

input_path = data_path / "input"
output_path = data_path / "output"
logs_path = data_path / "logs"
db_path = data_path / "db"

db_file = "abra_invoices.duckdb"
default_db_path = db_path / db_file


# Log paths
logging.debug(f"Default data path: {data_path}")
logging.debug(f"Input path: {input_path}")
logging.debug(f"Output path: {output_path}")
logging.debug(f"Logs path: {logs_path}")
logging.debug(f"Database path: {db_path}")
logging.debug(f"Default database path: {default_db_path}")

# Ensure default data path and subdirectories exist
for path in [neven_path, data_path, input_path, output_path, logs_path, db_path]:
    path = Path(path).expanduser()
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)