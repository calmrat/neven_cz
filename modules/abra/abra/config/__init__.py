import os

from pathlib import Path
from dotenv import load_dotenv

import logging

# Load environment variables
load_dotenv()

# Define paths
default_data_path = Path(os.getenv("DATA_PATH", "../.data"))
input_path = default_data_path / "input"
output_path = default_data_path / "output"
logs_path = default_data_path / "logs"
db_path = default_data_path / "db"
db_file = "invoices.duckdb"
sample_db_path = db_path / db_file


# Log paths
logging.debug(f"Default data path: {default_data_path}")
logging.debug(f"Input path: {input_path}")
logging.debug(f"Output path: {output_path}")
logging.debug(f"Logs path: {logs_path}")
logging.debug(f"Database path: {db_path}")

# Ensure default data path and subdirectories exist
for path in [default_data_path, input_path, output_path, logs_path, db_path]:
    path = Path(path)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
