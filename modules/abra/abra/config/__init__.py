import os

from pathlib import Path
from dotenv import load_dotenv

import logging

# Logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

logger = logging.getLogger()

# Load environment variables
load_dotenv()

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

db_file = "invoices.duckdb"
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
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)