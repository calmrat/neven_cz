import os

from pathlib import Path
from dotenv import load_dotenv

import logging

# Load environment variables
load_dotenv()

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

    # # Default configuration if no config file exists.
    # config = {
    #     "database": {
    #         "cache_path": ".data/cache",
    #         "data_path": ".data"
    #     },
    #     "upgates": {
    #         "api_url": "https://api.upgates.cz",
    #         "login": "your_login",
    #         "api_key": "your_api_key"
    #     },
    #     "api": {
    #         "verify_ssl": True,
    #         "retry_attempts": 3,
    #         "parallel_batches": 1
    #     },
    #     "logging": {
    #         "log_level": "info"
    #     }
    # }