References:
https://ai.pydantic.dev/api/
https://logfire.pydantic.dev/docs/
https://docs.pydantic.dev/latest/

system_prompt.md
# System Prompt for Upgatescz API v0.4.0

## Overview

This system facilitates syncing of product data, customers, orders, and other related data from Upgates API to a local DuckDB database. It supports real-time updates via webhooks, periodic syncs, and translation of product descriptions.

## Core Features

- **Data Sync**: Sync products, customers, and orders data from Upgates.
- **Real-Time Updates**: React to events like product updates using webhooks.
- **Automated Sync**: Sync data periodically using a scheduler.
- **Translations**: Automatically translate product descriptions based on language settings.
- **DuckDB**: Use DuckDB for high-performance local data storage.

## Data Structures

### Upgates API Data

- **Product Data**
    - `product_id`: Integer
    - `code`: String
    - `ean`: String
    - `manufacturer`: String
    - `stock`: Integer
    - `weight`: Integer
    - `availability`: String
    - `unit`: String
    - `descriptions`: List of dictionaries with fields like `language`, `title`, `short_description`, `long_description`, `url`, `seo_title`, etc.

- **Prices**
    - `product_id`: Integer
    - `currency`: String
    - `price_with_vat`: Float

- **Images**
    - `product_id`: Integer
    - `url`: String
    - `position`: Integer

- **Categories**
    - `product_id`: Integer
    - `category_id`: Integer
    - `category_name`: String

- **Metas**
    - `product_id`: Integer
    - `meta_key`: String
    - `meta_value`: String

- **Vats**
    - `product_id`: Integer
    - `country_code`: String
    - `vat_percentage`: Float

### Upgates CSV Data

- **Products CSV**
    - Columns: `product_id`, `code`, `ean`, `manufacturer`, `stock`, `weight`, `availability`, `unit`

- **Prices CSV**
    - Columns: `product_id`, `currency`, `price_with_vat`

- **Images CSV**
    - Columns: `product_id`, `url`, `position`

- **Categories CSV**
    - Columns: `product_id`, `category_id`, `category_name`

### DuckDB Tables

- **products**: Contains product details.
- **prices**: Contains pricing information.
- **images**: Stores image URLs for products.
- **categories**: Contains product categories.
- **metas**: Stores meta information about products.
- **vats**: Stores VAT details.

## Logging

The system uses Logfire for logging. The log levels used are:

- **INFO**: Regular logs about system operations.
- **DEBUG**: Detailed logs for debugging.
- **WARNING**: Warnings for potential issues.
- **ERROR**: Errors that need to be addressed.
- **SUCCESS**: Logs for successful operations.

## File Locations

- **Cache Path**: `.data/cache`
- **Data Path**: `.data`
- **Configuration File**: `.config/config.toml`
- **Log Files**: Stored in `.data/logs/`

## CLI Commands

- `start_webhook`: Start the Flask-based webhook server for real-time updates.
- `start_scheduler`: Start the periodic syncing scheduler.
- `sync_all`: Sync all data (products, customers, orders).
- `sync_products`: Sync product data.
- `sync_customers`: Sync customer data.
- `sync_orders`: Sync order data.
- `search_product`: Search for a product by product code.
- `translate_product`: Translate product descriptions.
- `show-products`: Show all products.
- `clear_cache`: Clear the DuckDB cache.

## Configuration Example (`config.toml`)

```toml
[database]
cache_path = ".data/cache"
data_path = ".data"

[api]
api_url = "https://api.upgates.cz"
login = "your_username"
api_key = "your_api_key"
verify_ssl = true
parallel_batches = 5
retry_attempts = 3

[logging]
log_level = "info"

-----------
upgatescz_api v0.1.0

Project Structure
upgatescz_api/
│
├── .config/
│   ├── config.toml.sample  # Sample config file
│
├── .data/
│   ├── cache/  # DuckDB cache directory
│   ├── logs/   # Log files (if any)
│
├── upgates/
│   ├── cli.py  # Command-line interface for syncing and managing products, customers, orders
│   ├── webhook_server.py  # Webhook server for real-time updates
│   ├── scheduler.py  # Scheduler for periodic synchronization
│   ├── upgates_client.py  # Main client for interacting with Upgates API
│   ├── db/
│   │   ├── upgates_duckdb_api.py  # DuckDB management and data operations
│   └── config.py  # Configuration management and defaults
│
├── docker-compose.yml
├── Dockerfile
├── install.sh  # Installation script
├── .gitignore
├── requirements.txt
├── README.md
└── tests/
    ├── test_upgates.py  # Pytest test coverage
    └── system_prompt.md  # Document for system setup

-----

`requirements.txt`
```plaintext
flask
aiohttp
duckdb
logfire
pandas
schedule
pytest
pytest-asyncio
tqdm

----
.env
CONFIG_PATH=".config/upgates/config.toml"

----

.config/upgates/config.toml.sample
[upgates]
api_url = "https://api.upgates.cz"
login = "your-login"
api_key = "your-api-key"

[database]
cache_path = ".data/cache"
data_path = ".data"

[logging]
log_level = "info"


----
README.md

# Upgatescz API v0.4.0

## Project Overview
The Upgatescz API is a Python-based tool for synchronizing product data, customers, orders, and other related data from the Upgates.cz platform. It supports real-time updates via webhooks, batch synchronization of data, translation of product descriptions, and storing all data in a DuckDB cache for efficient querying.

## Features
- **Data Sync**: Sync products, customers, orders, and parameters from Upgates.cz API.
- **Webhooks**: Real-time updates triggered by product, customer, or order changes.
- **Batch Syncing**: Fetch large datasets in batches and store them in DuckDB.
- **AI Translations**: Supports translation of product descriptions using the Pydantic AI model.
- **Docker Support**: Easily deploy the system using Docker.

## Installation
### Requirements
- Python 3.12+
- Docker (optional)
- Redis (optional)

### Setup via GitHub
```bash
# Clone the repository
git clone https://github.com/yourusername/upgatescz_api.git
cd upgatescz_api

# Install dependencies
bash install.sh

# Start the application
python upgates/cli.py


------

Dokerfile
# Use a Python base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Expose Flask's default port
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=upgates/cli.py
ENV FLASK_ENV=production

# Run the Flask server by default
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
-----
 docker-compose.yml
version: '3'

services:
  upgates-api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
      - LOGFIRE_CONSOLE_MIN_LOG_LEVEL=debug
    depends_on:
      - redis
    command: python upgates/cli.py

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
    driver: local
-----

install.sh (move to setup/install.sh; add setup/install.py)

#!/bin/bash

# Update and install system dependencies
echo "🌐 Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y curl python3-pip python3-venv

# Clone the repository
echo "🔄 Cloning repository..."
git clone https://github.com/yourusername/upgatescz_api.git
cd upgatescz_api

# Create and activate a Python virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Set up the environment configuration
echo "⚙️ Setting up configuration..."
cp .config/config.toml.sample .config/config.toml

# Start the application
echo "🚀 Starting the application..."
python upgates/cli.py

----

In the docker/ directory, you could have a docker-compose.yml to manage services such as the webhook and your app itself.

version: '3'

services:
  upgatescz-api:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_ENV=development
    command: python src/cli.py
  redis:
    image: redis:latest
    ports:
      - "6379:6379"

----
py.test
import pytest
from upgates.upgates_client import UpgatesClient

@pytest.fixture
def client():
    """Fixture to initialize UpgatesClient."""
    return UpgatesClient()

def test_sync_products(client):
    """Test the sync of products."""
    result = asyncio.run(client.sync_products(page_count=1))
    assert len(result) > 0, "Should fetch at least one product."

def test_sync_orders(client):
    """Test the sync of orders."""
    result = asyncio.run(client.sync_orders(page_count=1))
    assert len(result) > 0, "Should fetch at least one order."

def test_get_product_details(client):
    """Test retrieving product details."""
    product_details = asyncio.run(client.db_api.get_product_details("10009"))
    assert not product_details.empty, "Product details should be returned."

def test_sync_all(client):
    """Test syncing all data."""
    result = asyncio.run(client.sync_all())
    assert result is not None, "Sync should complete successfully."

# Add additional tests for webhook handling, scheduled sync, etc.

----

schedules.py

import schedule
import time

def scheduled_sync():
    """Runs full API sync on a schedule."""
    print("🔄 Running scheduled sync...")
    # Replace with appropriate sync function (product, customer, orders)
    # Here we sync all data
    from upgates.upgates_client import UpgatesClient
    client = UpgatesClient()
    asyncio.run(client.sync_all())

schedule.every(30).minutes.do(scheduled_sync)

print("🕒 Scheduled sync initialized.")
while True:
    schedule.run_pending()
    time.sleep(1)


----

webhook_server.py

from flask import Flask, request, jsonify
import asyncio
from upgates.upgates_client import UpgatesClient

# Initialize Flask and UpgatesClient
app = Flask(__name__)
client = UpgatesClient()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook for real-time Upgates updates."""
    data = request.json
    print(f"🔔 Webhook received: {data}")

    # Handle various webhook event types
    match data.get("type"):
        case "product.updated":
            asyncio.run(client.sync_products())
        case "customer.updated":
            asyncio.run(client.sync_customers())
        case "order.updated":
            asyncio.run(client.sync_orders())
        case _:
            print(f"⚠️ Unknown webhook event: {data}")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


----
.gitignore

# ==============================
# 🌍 Universal OS-specific ignores
# ==============================

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/

# Linux
*~
.nfs*

# ==============================
# 🐍 Python-specific ignores
# ==============================

# Ignore Python compiled files
__pycache__/
*.pyc
*.pyo
*.pyd

# Ignore environment files
.env
.venv/
venv/
Pipfile.lock
poetry.lock

# ==============================
# 💻 IDE / Editor ignores
# ==============================

# VS Code
.vscode/
*.code-workspace

# JetBrains (PyCharm, WebStorm, etc.)
.idea/
*.iml
*.ipr
*.iws

# Sublime Text
*.sublime-workspace
*.sublime-project

# Jupyter Notebook checkpoints
.ipynb_checkpoints/

# ==============================
# 🔧 Project-specific ignores
# ==============================

# Ignore config files
/config.toml
/config/

# Ignore local user-defined configuration
.config/
.config/*

# Ignore DuckDB cache and other generated data
.data/
data/
cache/
backups/
logs/

# Ignore log files
*.log

# Ignore backup files
*.bak
*.swp

# ==============================
# 🚀 Deployment / Build ignores
# ==============================

# Byte-compiled / packaged
dist/
build/
*.egg-info/
*.manifest
*.spec

# Docker
docker-compose.override.yml

----




----

cli.py
import sys
import os
import click
import asyncio
import subprocess
import toml
import json
import pandas as pd
import ipdb
import duckdb
#import atexit


# Ensure the package directory is included in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from upgates.upgates_client import UpgatesClient
from upgates.config import config

cache_path = config["database"].get("cache_path", ".data/cache")  # Default to .data/cache if not defined
# Update DuckDB path using the config-provided cache path
db_file = os.path.join(cache_path, "duckdb_cache.db")

client = UpgatesClient()

# Assuming you have an active event loop and async functions to run
#loop = asyncio.get_event_loop()

## Function that runs at exit to ensure pending tasks are completed
#def cleanup_pending_tasks():
#    pending = asyncio.all_tasks(loop)  # Get all pending tasks for the loop
#    if pending:
#        print("Cleaning up pending tasks...")
#        loop.run_until_complete(asyncio.gather(*pending))  # Wait until all tasks are done
#    else:
#        print("No pending tasks.")

# Register the cleanup function to run at exit
#atexit.register(cleanup_pending_tasks)

def _clear_cache(cache_path=".data/cache"):
    """Clear the DuckDB cache file."""
    db_file = os.path.join(cache_path, "duckdb_cache.db")

    if os.path.exists(db_file):
        os.remove(db_file)
        click.echo("DuckDB cache file cleared.")
    else:
        click.echo("Cache file not found, nothing to clear.")

@click.group()
def cli():
    """CLI for managing Upgates API sync, translation, and configuration.""" 
    pass

@click.command()
def start_webhook():
    """Start webhook server for real-time updates.""" 
    subprocess.run(["python", "webhook_server.py"])

@click.command()
def start_scheduler():
    """Start scheduled auto-sync process.""" 
    subprocess.run(["python", "scheduler.py"])


####


@click.command()
@click.option('--clear-cache', is_flag=False, help="Clear the cache before syncing.")
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
def sync_products(clear_cache, page_count):
    """Sync products data."""
    
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    asyncio.run(client.sync_products(page_count=page_count))
    import ipdb; ipdb.set_trace()

@click.command()
@click.option('--clear-cache', is_flag=False, help="Clear the cache before syncing.")
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
def sync_customers(clear_cache, page_count):
    """Sync customers data."""
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    asyncio.run(client.sync_customers(page_count=page_count))

@click.command()
@click.option('--clear-cache', is_flag=False, help="Clear the cache before syncing.")
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
def sync_orders(clear_cache, page_count):
    """Sync orders data."""
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    asyncio.run(client.sync_orders(page_count=page_count))

@click.command()
@click.option('--clear-cache', is_flag=False, help="Clear the cache before syncing.")
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
def sync_all(clear_cache, page_count):
    """Sync all data: products, customers, orders."""
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    asyncio.run(client.sync_all(page_count=page_count))


####



@click.command()
@click.argument("product_id")
@click.argument("lang")
def translate_product(product_id, lang):
    """Translate product descriptions for a given language.""" 
    asyncio.run(client.translate_product(product_id, lang))

@click.command()
def init_config():
    """Initialize configuration by prompting for missing values.""" 
    client.init_config()

@click.command()
@click.argument("product_code")
@click.option("--format", default="json", type=click.Choice(["json", "json", "df", "toml"]), help="Output format: JSON (default), TOML, or DataFrame (df).")
@click.option("--embed", is_flag=True, default=True, help="Launch ipython.embed() shell after searching for product.")
def search_product(product_code, format, embed):
    """Search for a product by product_code.""" 
    product = asyncio.run(client.db_api.get_product_details(product_code))

    if product.empty:
        click.echo(f"❌ Product '{product_code}' not found.")
        return

    if format == "df":
        if embed:
            import ipdb; ipdb.set_trace()            
        else:
            click.echo(product.to_string(index=False))
    elif format == "json":
        click.echo(product.to_json(orient="records", indent=2))
    #else:
    #    click.echo(toml.dumps(product), fg="green")

@click.command(name="show-products")
@click.option("--embed", is_flag=True, default=True, help="Launch ipython.embed() shell after showing products.")
def show_products(embed):
    """Show all products with related data."""
    # Get all product details (with foreign key relationships)
    products = client.db_api.get_product_details()
    
    if embed:
        import ipdb; ipdb.set_trace()
    
    click.echo(products.to_json(orient="records", indent=2))

@click.command(name="show-customers")
def show_customers():
    """Show all customers."""
    conn = duckdb.connect(db_file)
    df = conn.execute("SELECT * FROM customers").fetchdf()
    conn.close()
    print(df.head())

@click.command(name="show-orders")
def show_orders():
    """Show all orders."""
    conn = duckdb.connect(db_file)
    df = conn.execute("SELECT * FROM orders").fetchdf()
    conn.close()
    print(df.head())

@click.command()
def clear_cache():
    """Force-clear the DuckDB cache file."""
    db_file = os.path.join(config["database"].get("cache_path", ".data/cache"), "duckdb_cache.db")

    # Ensure the cache file exists before attempting to remove
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            click.echo("✅ Database cache file cleared successfully.")
        except Exception as e:
            click.echo(f"❌ Failed to clear cache file: {e}")
    else:
        click.echo("⚠️ Cache file does not exist.")

cli.add_command(start_webhook)
cli.add_command(start_scheduler)
cli.add_command(sync_all)
cli.add_command(sync_products)
cli.add_command(sync_customers)
cli.add_command(sync_orders)
cli.add_command(translate_product)
cli.add_command(init_config)
cli.add_command(search_product)
cli.add_command(show_products)
cli.add_command(show_customers)
cli.add_command(show_orders)
cli.add_command(clear_cache)


if __name__ == "__main__":
    cli()






upgatescz_api.py (api/upgates.py)

import os
import duckdb
import logfire

import pandas as pd

from upgates.config import config

logfire.configure()

class UpgatesDuckDBAPI:
    """Class to manage interactions with DuckDB for Upgates data."""

    _initialized = False  # Class-level flag to track initialization

    def __init__(self):
        """Initialize the DuckDB API client."""
        self.cache_path = config["database"].get("cache_path", ".data/cache")
        self.db_file = os.path.join(self.cache_path, "duckdb_cache.db")
        self._ensure_cache_directory_exists()
        existed_already = os.path.exists(self.db_file)
        self.conn = duckdb.connect(self.db_file)

        # Initialize DB only if not already done
        if not (UpgatesDuckDBAPI._initialized and existed_already):
            logfire.debug(f"Initializing DuckDB API @ {self.db_file}")
            self._initialize_db()
            UpgatesDuckDBAPI._initialized = True
        else:
            logfire.debug("DuckDB tables already exist. Skipping initialization.")

        #logfire.debug("UpgatesDuckDBAPI initialized.")

    def _initialize_db(self):
        """Create tables if they don't exist."""
        logfire.debug("Initializing DuckDB tables...")

        # Create sequences for primary key auto-generation
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_description_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_prices_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_image_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_category_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_meta_id START 1;")
        self.conn.execute("CREATE SEQUENCE IF NOT EXISTS seq_vat_id START 1;")

        # Check if the database and tables exist before creating
        if not self._check_table_exists('products'):
            self._create_products_table()

        if not self._check_table_exists('customers'):
            self._create_customers_table()

        if not self._check_table_exists('orders'):
            self._create_orders_table()

        if not self._check_table_exists('descriptions'):
            self._create_descriptions_table()

        if not self._check_table_exists('prices'):
            self._create_prices_table()

        if not self._check_table_exists('images'):
            self._create_images_table()

        if not self._check_table_exists('categories'):
            self._create_categories_table()

        if not self._check_table_exists('metas'):
            self._create_metas_table()

        if not self._check_table_exists('vats'):
            self._create_vats_table()

        logfire.debug("DuckDB tables initialized.")

    def _check_table_exists(self, table_name):
        """Check if the table exists in DuckDB."""
        query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}'"
        result = self.conn.execute(query).fetchone()
        return result[0] > 0

    def _ensure_cache_directory_exists(self):
        """Ensure the cache directory exists."""
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)

    def _create_products_table(self):
        """Create products table if it doesn't exist."""
        logfire.debug("Creating products table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                code TEXT,
                ean TEXT,
                manufacturer TEXT,
                stock INTEGER,
                weight INTEGER,
                availability TEXT,
                availability_type TEXT,
                unit TEXT,
                action_currently_yn BOOLEAN,
                active_yn BOOLEAN,
                archived_yn BOOLEAN,
                can_add_to_basket_yn BOOLEAN,
                adult_yn BOOLEAN,
                set_yn BOOLEAN,
                in_set_yn BOOLEAN,
                exclude_from_search_yn BOOLEAN
            );
        """)
        logfire.debug(f"Product table created: {self.conn.execute('DESCRIBE products').fetchall()}")

    def _create_customers_table(self):
        """Create customers table if it doesn't exist."""
        logfire.debug("Creating customers table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                type TEXT,
                firstname TEXT,
                surname TEXT,
                email TEXT,
                phone TEXT,
                company_name TEXT
            );
        """)

    def _create_orders_table(self):
        """Create orders table if it doesn't exist."""
        logfire.debug("Creating orders table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                order_number TEXT,
                customer_id INTEGER,
                total_price FLOAT,
                total_weight FLOAT,
                status TEXT
            );
        """)

    def _create_descriptions_table(self):
        """Create descriptions table if it doesn't exist."""
        logfire.debug("Creating descriptions table...")
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS descriptions (
                description_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_description_id'),
                product_id INTEGER,
                language TEXT,
                title TEXT,
                short_description TEXT,
                long_description TEXT,
                url TEXT,
                seo_title TEXT,
                seo_description TEXT,
                seo_url TEXT,
                unit TEXT,
                FOREIGN KEY (product_id) REFERENCES products(product_id) 
            );
        """)

    def _create_prices_table(self):
        """Create prices table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS prices (
                price_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_prices_id'),
                product_id INTEGER,
                currency TEXT,
                price_with_vat FLOAT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_images_table(self):
        """Create images table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS images (
                image_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_image_id'),
                product_id INTEGER,
                file_id INTEGER,
                url TEXT,
                main_yn BOOLEAN,
                position INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_categories_table(self):
        """Create categories table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_category_id'),
                product_id INTEGER,
                category_code TEXT,
                category_name TEXT,
                main_yn BOOLEAN,
                position INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_metas_table(self):
        """Create metas table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS metas (
                meta_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_meta_id'),
                product_id INTEGER,
                meta_key TEXT,
                meta_type TEXT,
                meta_value TEXT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def _create_vats_table(self):
        """Create VAT details table if it doesn't exist."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS vats (
                vat_id INTEGER PRIMARY KEY DEFAULT NEXTVAL('seq_vat_id'),
                product_id INTEGER,
                country_code TEXT,
                vat_percentage FLOAT,
                FOREIGN KEY (product_id) REFERENCES products(product_id)
            );
        """)

    def insert_product(self, product_id, code, ean, manufacturer, stock, weight, availability, availability_type, unit,
                    action_currently_yn, active_yn, archived_yn, can_add_to_basket_yn, adult_yn, set_yn, in_set_yn,
                    exclude_from_search_yn):
        """Insert product data into the products table."""
        self.conn.execute("""
            INSERT INTO products (product_id, code, ean, manufacturer, stock, weight, availability, availability_type, unit,
                                action_currently_yn, active_yn, archived_yn, can_add_to_basket_yn, adult_yn, set_yn, in_set_yn, exclude_from_search_yn)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(product_id) DO UPDATE
            SET code = excluded.code, ean = excluded.ean, manufacturer = excluded.manufacturer, 
                stock = excluded.stock, weight = excluded.weight, availability = excluded.availability,
                availability_type = excluded.availability_type, unit = excluded.unit,
                action_currently_yn = excluded.action_currently_yn, active_yn = excluded.active_yn,
                archived_yn = excluded.archived_yn, can_add_to_basket_yn = excluded.can_add_to_basket_yn,
                adult_yn = excluded.adult_yn, set_yn = excluded.set_yn, in_set_yn = excluded.in_set_yn,
                exclude_from_search_yn = excluded.exclude_from_search_yn
        """, (
            product_id, code, ean, manufacturer, stock, weight, availability, availability_type, unit,
            action_currently_yn, active_yn, archived_yn, can_add_to_basket_yn, adult_yn, set_yn, in_set_yn,
            exclude_from_search_yn
        ))
        # Debug output the count of products
        product_count = self.conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        logfire.debug(f"Added Product ID {product_id}\nTotal number of products: {product_count}")
        
    def insert_description(self, product_id, language, title, short_description, long_description, url, seo_title, seo_description, seo_url, unit):
        """Insert product descriptions into the descriptions table."""
        self.conn.execute("""
            INSERT INTO descriptions (product_id, language, title, short_description, long_description, url, seo_title, seo_description, seo_url, unit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (product_id, language, title, short_description, long_description, url, seo_title, seo_description, seo_url, unit))

    def insert_price(self, product_id, currency, price_with_vat):
        """Insert price data into the prices table."""
        self.conn.execute("""
            INSERT INTO prices (product_id, currency, price_with_vat)
            VALUES (?, ?, ?)
        """, (product_id, currency, price_with_vat))

    def insert_image(self, product_id, file_id, url, main_yn, position):
        """Insert image data into the images table."""
        self.conn.execute("""
            INSERT INTO images (product_id, file_id, url, main_yn, position)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, file_id, url, main_yn, position))

    def insert_category(self, product_id, category_id, category_code, category_name, main_yn, position):
        """Insert category data into the categories table, skipping duplicates."""
        try:
            # Check if the category_id already exists
            existing_category = self.conn.execute("""
                SELECT 1 FROM categories WHERE category_id = ?
            """, (category_id,)).fetchone()

            if existing_category:
                logfire.debug(f"⚠️ Category with ID {category_id} already exists. Skipping insert.")
            else:
                # Insert category if it doesn't exist
                self.conn.execute("""
                    INSERT INTO categories (product_id, category_id, category_code, category_name, main_yn, position)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (product_id, category_id, category_code, category_name, main_yn, position))
                logfire.debug(f"✅ Category with ID {category_id} inserted successfully.")
                
                ## Fetch and log all products for verification
                #products = self.conn.execute("SELECT * FROM products").fetchall()
                #logfire.info(f"All products: {products}")

        except Exception as e:
            logfire.error(f"❌ Failed to insert category {category_id}: {e}")

    def insert_meta(self, product_id, meta_key, meta_type, meta_value):
        """Insert metadata into the metas table."""
        self.conn.execute("""
            INSERT INTO metas (product_id, meta_key, meta_type, meta_value)
            VALUES (?, ?, ?, ?)
        """, (product_id, meta_key, meta_type, meta_value))

    def insert_vat(self, product_id, country_code, vat_percentage):
        """Insert VAT details into the vats table."""
        self.conn.execute("""
            INSERT INTO vats (product_id, country_code, vat_percentage)
            VALUES (?, ?, ?)
        """, (product_id, country_code, vat_percentage))

    async def get_product_details(self, code=None):
        """Show all products with aggregated prices, images, categories, metas, vats, and descriptions."""
        query = """
        SELECT 
            p.product_id, 
            ANY_VALUE(p.code) AS code, 
            ANY_VALUE(p.ean) AS ean, 
            ANY_VALUE(p.manufacturer) AS manufacturer, 
            ANY_VALUE(p.stock) AS stock, 
            ANY_VALUE(p.weight) AS weight, 
            ANY_VALUE(p.availability) AS availability, 
            ANY_VALUE(p.availability_type) AS availability_type, 
            ANY_VALUE(p.unit) AS unit,
            
            -- Aggregating prices (all prices in one column as a comma-separated list)
            GROUP_CONCAT(DISTINCT pr.currency) AS currencies,
            GROUP_CONCAT(DISTINCT pr.price_with_vat) AS prices,
            
            -- Aggregating image URLs (all images in one column)
            GROUP_CONCAT(DISTINCT i.url) AS image_urls,
            GROUP_CONCAT(DISTINCT i.position) AS image_positions,

            -- Aggregating category details (all categories in one column)
            GROUP_CONCAT(DISTINCT c.category_id || ',' || c.category_code || ',' || c.category_name || ',' || c.main_yn || ',' || c.position, '|||') AS category_details,

            -- Aggregating metas (all metas in one column)
            GROUP_CONCAT(DISTINCT m.meta_key || '=' || m.meta_value) AS metas,

            -- Aggregating VAT information
            GROUP_CONCAT(DISTINCT v.country_code || ':' || v.vat_percentage) AS vat_details,

            -- Aggregating descriptions (one for each language)
            GROUP_CONCAT(DISTINCT d.language || ',' || d.title || ',' || d.short_description || ',' || d.long_description || ',' || d.url, '|||') AS descriptions
        FROM 
            products p
        LEFT JOIN prices pr ON p.product_id = pr.product_id
        LEFT JOIN images i ON p.product_id = i.product_id
        LEFT JOIN categories c ON p.product_id = c.product_id
        LEFT JOIN metas m ON p.product_id = m.product_id
        LEFT JOIN vats v ON p.product_id = v.product_id
        LEFT JOIN descriptions d ON p.product_id = d.product_id
        """
        if code:
            query += f" WHERE p.code = '{code}'"
        query += f" GROUP BY p.product_id"
        query += f";"
        
        logfire.debug (f"Query: {query}")

        results = self.conn.execute(query).fetchdf()
        
        # Unflatten descriptions into nested objects
        def unflatten_descriptions(row):
            descriptions = row['descriptions'].split('|||') if row['descriptions'] else []
            description_objects = []
            for desc in descriptions:
                if desc:
                    parts = desc.split(',')
                    description_objects.append({
                        'language': parts[0],
                        'title': parts[1],
                        'short_description': parts[2],
                        'long_description': parts[3],
                        'url': parts[4]
                    })
            row['descriptions'] = description_objects
            return row

        # Unflatten vats into nested objects
        def unflatten_vats(row):
            vats = row['vat_details'].split(',')
            vat_objects = []
            for vat in vats:
                if vat:
                    parts = vat.split(':')
                    vat_objects.append({
                        'country_code': parts[0],
                        'vat_percentage': parts[1]
                    })
            row['vat_details'] = vat_objects
            return row

        # Unflatten metas into nested objects
        def unflatten_metas(row):
            metas = row['metas'].split(',')
            meta_objects = []
            for meta in metas:
                if meta:
                    parts = meta.split('=')
                    meta_objects.append({
                        'meta_key': parts[0],
                        'meta_value': parts[1]
                    })
            row['metas'] = meta_objects
            return row

        # Unflatten categories into nested objects
        def unflatten_categories(row):
            print (row)
            categories = row['category_details'].split('|||') if row['category_details'] else []
            category_objects = []
            for category in categories:
                if category:
                    parts = category.split(',')
                    category_objects.append({
                        'category_id': parts[0],
                        'category_code': parts[1],
                        'category_name': parts[2],
                        'main_yn': parts[3],
                        'position': parts[4]
                    })
            row['category_details'] = category_objects
            return row
        
        # Unflatten images into nested objects
        def unflatten_images(row):
            images = row['image_urls'].split(',')
            image_objects = []
            for image in images:
                if image:
                    parts = image.split(':')
                    image_objects.append({
                        'url': parts[0],
                        'position': parts[1]
                    })
            row['image_urls'] = image_objects
            return row
        
        # Unflatten prices into nested objects
        def unflatten_prices(row):
            #prices = row['prices'].split(',')
            return row['prices']
            # price_objects = []
            # print (row)
            # for price in prices:
            #     if price:
            #         parts = price.split(',')
            #         print (parts)
            #         price_objects.append({
            #             'currency': parts[0],
            #             'price_with_vat': parts[1]
            #         })
            # row['prices'] = price_objects
            # return row

        results = results.apply(unflatten_descriptions, axis=1)#.reset_index(drop=True)
        results = results.apply(unflatten_vats, axis=1)#.reset_index(drop=True)
        # results['metas'] = results.apply(unflatten_metas, axis=1).reset_index(drop=True)
        # results['categories'] = results.apply(unflatten_categories, axis=1).reset_index(drop=True)
        # results['imgaes'] = results.apply(unflatten_images, axis=1).reset_index(drop=True)
        # results['prices'] = results.apply(unflatten_prices, axis=1).reset_index(drop=True)

        # Log and return results
        #logfire.debug(f"Fetched {len(merged_results)} products with their associated details.")
        #import ipdb; ipdb.set_trace()
        logfire.debug(f"Fetched {len(results)} products with their associated details.")
        return results

    def get_customer_details(self):
        """Show all customers."""
        query = "SELECT * FROM customers"
        results = self.conn.execute(query).fetchdf()
        return results

    def get_order_details(self):
        """Show all orders."""
        query = "SELECT * FROM orders"
        results = self.conn.execute(query).fetchdf()
        return results

    #def __del__(self):
    #    """Close the database connection when the class instance is destroyed."""
    #    try:
    #        self.conn.close()
    #        logfire.debug("DuckDB connection closed.")
    #    except Exception as e:
    #        logfire.error(f"Failed to close DuckDB connection: {e}")





upgatescz_client.py (clients/)

import os
import aiohttp
import asyncio
import logfire
from tqdm.asyncio import tqdm
from typing import List, Dict
from upgates.config import config
from upgates.db.upgates_duckdb_api import UpgatesDuckDBAPI


# Set retry attempts from config (default: 1)
RETRY_ATTEMPTS = config.get("api", {}).get("retry_attempts", 1)

# Ensure the cache directory exists
cache_path = config["database"].get("cache_path", ".data/cache")
os.makedirs(cache_path, exist_ok=True)

# Update DuckDB path
db_file = os.path.join(cache_path, "duckdb_cache.db")

# Set log level from environment or config file, default to "info"
#log_level: str = os.getenv("LOGFIRE_CONSOLE_MIN_LOG_LEVEL", config.get("logging", {}).get("log_level", "info"))
logfire.configure()

def log_sync_statistics(sync_results: Dict[str, List]) -> None:
    """Log the number of each object type saved during sync."""
    stats: Dict[str, int] = {key: len(value) for key, value in sync_results.items()}
    logfire.info(f"Sync completed: {stats}")

class UpgatesClient:
    """Async API Client for Upgates with proper syncing, logging, and translations."""
    
    API_URL = config["upgates"]["api_url"]
    LOGIN = config["upgates"]["login"]
    API_KEY = config["upgates"]["api_key"]
    VERIFY_SSL = config["api"].get("verify_ssl", True)
    DATA_PATH = config["database"].get("data_path", ".data")
    DB_FILE = db_file
    PARALLEL_BATCHES = config["api"].get("parallel_batches", 1)

    def __init__(self):
        """Ensure DuckDB database is initialized before starting."""
        logfire.debug("🌉 UpgatesClient initialized.")
        self.db_api = UpgatesDuckDBAPI()  # Initializes only once due to lazy table creation

    async def sync_all(self):
        """Sync all data: products, customers, orders."""
        logfire.info("ℹ️ Starting full API sync...")
        await asyncio.gather(self.sync_products(), self.sync_customers(), self.sync_orders())

    async def sync_products(self, page_count=None):
        """Sync products from the Upgates.cz API."""
        logfire.info("Fetching product data...")
        products_response = await self.fetch_data("products", page_count=page_count)

        if products_response:
            products = products_response.get("products", [])
            logfire.info(f"Fetched product data: {products[:1]}...")  # Log the first product as a sample

            if products:
                for product in products:
                    print ("Product: ", product['product_id'], product['code'])
                    #import pdb; pdb.set_trace()
                    product_id = product.get('product_id', 0)
                    code = product.get('code', 'Unknown Code')
                    ean = product.get('ean', '')
                    manufacturer = product.get('manufacturer', '')
                    stock = product.get('stock', 0)
                    weight = product.get('weight', 0)
                    availability = product.get('availability', '')
                    availability_type = product.get('availability_type', '')
                    unit = product.get('unit', 'ks')

                    # Convert _yn fields to 1 (True) or 0 (False)
                    action_currently_yn = 1 if product.get('action_currently_yn', False) else 0
                    active_yn = 1 if product.get('active_yn', False) else 0
                    archived_yn = 1 if product.get('archived_yn', False) else 0
                    can_add_to_basket_yn = 1 if product.get('can_add_to_basket_yn', False) else 0
                    adult_yn = 1 if product.get('adult_yn', False) else 0
                    set_yn = 1 if product.get('set_yn', False) else 0
                    in_set_yn = 1 if product.get('in_set_yn', False) else 0
                    exclude_from_search_yn = 1 if product.get('exclude_from_search_yn', False) else 0

                    # Inserting product data into the database
                    self.db_api.insert_product(
                        product_id, code, ean, manufacturer, stock, weight, availability, availability_type, unit,
                        action_currently_yn, active_yn, archived_yn, can_add_to_basket_yn, adult_yn, set_yn, in_set_yn,
                        exclude_from_search_yn
                    )

                    # Insert descriptions
                    for desc in product.get('descriptions', []):
                        language = desc.get('language', 'unknown')
                        title = desc.get('title', '')
                        short_description = desc.get('short_description', '')
                        long_description = desc.get('long_description', '')
                        url = desc.get('url', '')
                        seo_title = desc.get('seo_title', '')
                        seo_description = desc.get('seo_description', '')
                        seo_url = desc.get('seo_url', '')
                        unit = desc.get('unit', 'ks')
                        self.db_api.insert_description(product_id, language, title, short_description, long_description, url, seo_title, seo_description, seo_url, unit)

                    # Insert prices
                    for price in product.get('prices', []):
                        currency = price.get('currency', 'unknown')
                        price_with_vat = next((pl.get('price_with_vat', 0) for pl in price.get('pricelists', [])), 0.0)
                        self.db_api.insert_price(product_id, currency, price_with_vat)

                    # Insert images
                    for image in product.get('images', []):
                        file_id = image.get('file_id', None)
                        url = image.get('url', '')
                        main_yn = 1 if image.get('main_yn', False) else 0
                        position = image.get('position', 0)
                        self.db_api.insert_image(product_id, file_id, url, main_yn, position)

                    # Insert categories
                    for category in product.get('categories', []):
                        category_id = category.get('category_id', None)
                        category_code = category.get('code', '')
                        category_name = category.get('name', '')
                        main_yn = 1 if category.get('main_yn', False) else 0
                        position = category.get('position', 0)
                        self.db_api.insert_category(product_id, category_id, category_code, category_name, main_yn, position)

                    # Insert metadata
                    for meta in product.get('metas', []):
                        meta_key = meta.get('key', '')
                        meta_type = meta.get('type', '')
                        meta_value = meta.get('value', '')
                        self.db_api.insert_meta(product_id, meta_key, meta_type, meta_value)

                    # Insert VAT details
                    for vat_country, vat_percentage in product.get('vats', {}).items():
                        self.db_api.insert_vat(product_id, vat_country, vat_percentage)

                logfire.info(f"Product sync complete. {len(products)} products fetched and inserted.")
            else:
                logfire.warning("No product data found to sync.")
        else:
            logfire.warning("Failed to fetch product data.")

    async def sync_customers(self, page_count=None):
        """Sync customer data from the API."""
        logfire.info("ℹ️ Fetching customer data...")
        all_customers = []
        page = 1

        while True:
            try:
                customers_response = await self.fetch_data("customers", page, page_count)
                if isinstance(customers_response, dict) and "customers" in customers_response:
                    customers = customers_response["customers"]
                    if customers:
                        all_customers.extend(customers)
                        logfire.info(f"Fetched {len(customers)} items from page {page}")

                        total_pages = customers_response.get("number_of_pages", 0)
                        if page >= total_pages:
                            logfire.debug(f"✅ All pages fetched. Total pages: {total_pages}")
                            break
                        page += 1
                    else:
                        logfire.warning(f"⚠️ No customers found on page {page}.")
                        break
                else:
                    logfire.error(f"❌ Customers data is missing in response for page {page}.")
                    break
            except Exception as e:
                logfire.warning(f"⚠️ Failed to fetch customer data: {e} for page {page}")
                break

        if all_customers:
            self.db_api.insert_customers(all_customers)
            logfire.info(f"✅ Customer sync complete. {len(all_customers)} customers fetched and inserted.")

    async def sync_orders(self, page_count=None):
        """Sync order data from the API."""
        logfire.info("ℹ️ Fetching order data...")
        all_orders = []
        page = 1

        while True:
            try:
                orders_response = await self.fetch_data("orders", page)
                if isinstance(orders_response, dict) and "orders" in orders_response:
                    orders = orders_response["orders"]
                    if orders:
                        all_orders.extend(orders)
                        logfire.info(f"Fetched {len(orders)} items from page {page}")

                        total_pages = orders_response.get("number_of_pages", 0)
                        if page >= total_pages:
                            logfire.debug(f"✅ All pages fetched. Total pages: {total_pages}")
                            break
                        page += 1
                    else:
                        logfire.warning(f"⚠️ No orders found on page {page}.")
                        break
                else:
                    logfire.error(f"❌ Orders data is missing in response for page {page}.")
                    break
            except Exception as e:
                logfire.warning(f"⚠️ Failed to fetch order data: {e} for page {page}")
                break

        if all_orders:
            self.db_api.insert_orders(all_orders)
            logfire.info(f"✅ Order sync complete. {len(all_orders)} orders fetched and inserted.")

    async def fetch_data(self, endpoint, page=1, page_count=None):
        """Fetch data from the API with retries and handle pagination with rate-limiting."""
        all_data = []
        
        async def fetch_page(page_number):
            """Fetch a single page of data."""
            try:
                logfire.debug(f"🔄 Fetching page {page_number} of {endpoint}")
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        f"{self.API_URL}/{endpoint}?page={page_number}",
                        auth=aiohttp.BasicAuth(self.LOGIN, self.API_KEY),
                        ssl=self.VERIFY_SSL
                    ) as response:
                        logfire.debug(f"✅ Received response status: {response.status} for page {page_number}")

                        if response.status == 429:
                            # If rate limit exceeded, extract Retry-After header and wait
                            retry_after = response.headers.get("Retry-After", 60)  # Default to 60 seconds if not provided
                            logfire.warning(f"❌ Rate limit exceeded, retrying after {retry_after} seconds.")
                            await asyncio.sleep(int(retry_after))  # Wait for retry time
                            return await fetch_page(page_number)  # Retry the same page

                        # Parse the response
                        data = await response.json()
                        logfire.debug(f"📊 Response data: {data}")
                        
                        # Handle the response depending on the endpoint
                        match endpoint:
                            case "products":
                                items = data.get('products', [])
                            case "customers":
                                items = data.get('customers', [])
                            case "orders":
                                items = data.get('orders', [])
                            case _:
                                logfire.error(f"❌ Unexpected endpoint {endpoint}. Aborting.")
                                return [], 0

                        return items, data.get('number_of_pages', 1)

            except Exception as e:
                logfire.warning(f"⚠️ Failed to fetch page {page_number} of {endpoint}: {e}")
                return [], 0

        # Fetch pages sequentially or up to the specified `page_count`
        page = 1
        while True:
            items, total_pages = await fetch_page(page)
            all_data.extend(items)

            # If page_count is provided, stop after reaching the specified number of pages
            if page_count and page >= page_count:
                logfire.debug(f"✅ Reached the requested page count of {page_count}. Stopping.")
                break

            # If all pages are fetched, stop
            match page >= total_pages:
                case True:
                    logfire.debug(f"✅ All pages fetched. Total pages: {total_pages}")
                    break
                case False:
                    page += 1  # Go to the next page

        logfire.info(f"✅ All pages fetched. Total items: {len(all_data)}")
        return {endpoint: all_data}





References - Appendix, include in docs

Here's the Upgates.cz API definition (filetype: .apib)
source: https://upgatesapiv2.docs.apiary.io/api-description-document

FORMAT: 1A
HOST: https://shop-name.upgates.com/

# Upgates API
<a href="https://www.upgates.cz/"><img src="https://files.upgates.com/graphics/logos/upgates/svg/upgates-logo.svg" width="150px" alt="Upgates"></a>

Upgates API slouží jako rozhraní pro přístup do e-shopů Upgates. Díky Upgates API můžete pracovat s daty v systému (vkládání, aktualizace, čtení, mazání) v reálném čase a propojit např. váš účetní, ERP, nebo jiný systém s Upgates. Více informací naleznete na [upgates.cz](https://www.upgates.cz/).
<br>
<br>

## Základní informace
* Pokud vytváříte vlastní napojení, zvažte použítí již [hotových doplňků](https://www.upgates.cz/doplnky), nebo si přečtěte tipy pro [vlastní napojení](https://www.upgates.cz/a/napojeni-na-ucetni-erp-a-jine-systemy)
* Pro komuninaci s API budete potřebovat [vytvořit přístup](https://upgates.cz/cz/a/dokumentace-api-hotova-propojeni). To můžete udělat v administraci e-shopu v sekci *Doplňky > API*.
* API je dostupné na URL adrese: `https://NAZEV-ESHOPU.admin.ZNACKA-SERVERU.upgates.com/api/v2` Přesný tvar URL adresy najdete v administraci e-shopu v sekci *Doplňky > API*.
* Každý požadavek, který má v těle [JSON](https://cs.wikipedia.org/wiki/JavaScript_Object_Notation), by měl obsahovat hlavičku `Content-Type: application/json`.
* V případě chyby vrací API JSON s textem zprávy a odpovídající [stavový kód](#introduction/stavove-kody).
* API pracuje v kódování `UTF-8`, tzn. obsah všech požadavků musí být v tomto kódování.
* Většina endpointů vrací chybové hlášky (pole `messages`). Je to pole objektů, kde je informace o tom ve kterém objektu a které property je jaká chyba. Usnadňuje to odhalení chyby při nevalidním formátu JSON požadavku.

## Autentizace
* Je potřeba si v administraci založit přístup do API (**Administrace / Doplňky - API**).
* Každému API uživateli je možné omezit přístupová práva na jednotlivé API endpointy. Konkrétní seznam včetně přístupových práv lze získat pomocí endpointu [Stav API](#reference/stav-api), který je vždy povolen pro všechny uživatele API.
* Každý API přístup je přiřazen do skupiny, skupiny se přiřazují automaticky a slouží pro [Rate limiting](/#introduction/rate-limiting)
* Autentizace probíhá pomocí [HTTP Basic authentication](https://en.wikipedia.org/wiki/Basic_access_authentication). Používají se identifikační údaje **login:klíč API**.
* Po 5-ti špatných pokusech se API zablokuje a vrací chybovou hlášku `403` (viz. [Omezení přihlášení](#introduction/rate-limiting/omezeni-prihlaseni)).

## Stavové kódy
Kód | Název | Popis
---|-------|-------
 `200` | **OK** | úspěšně zpracovaný požadavek, ve většině případů vrací JSON (viz. popis konkrétních endpointů)
 `301` | **Moved Permanently** | e-shop byl přesunut na jiný server. V tomto případě server vrací hlavičku `Location` s novou adresou. Adresu si u sebe musíte změnit na novou.
 `400` | **Bad Request** | špatný požadavek, nevalidní JSON v těle požadavku. Pokud požadavek vyžaduje JSON, musí to být [JSON Object](https://www.w3schools.com/js/js_json_objects.asp)</a>
 `401` | **Unauthorized** | chyba při autentizaci, chybějící hlavička pro autentizaci nebo špatné přihlašovací údaje
 `403` | **Forbidden** | API uživatel není aktivní, nebo byl překročen maximální počet pokusů o přihlášení. Případně uživatel nemá práva na endpoint nebo metodu endpointu
 `404` | **Not Found** | špatná URL adresa požadavku
 `405` | **Method Not Allowed** | nepodporovaná metoda API nebo metoda konkrétního endpointu není implementována
 `413` | **Payload Too Large** | překročena velikost PUT požadavku - počet položek v JSONu (viz. [Rate Limiting](#introduction/rate-limiting))
 `429` | **Too Many Requests** | překročen maximální počet požadavků (viz. [Rate Limiting](#introduction/rate-limiting))
 `500` | **Internal Server Error** | chyba serveru. Pokud nastane, kontaktujte [technickou podporu Upgates](https://upgates.cz/a/technicka-podpora)
 `501` | **Not Implemented** | metoda není implementována

## HTTP metody
* API podporuje 4 základní HTTP metody: `POST`, `GET`, `PUT`, `DELETE`. Bližší popis je u každého endpointu.
* Pro přepsání HTTP metody můžete použít hlavičku `X-HTTP-Method-Override`. Požadavek může být např. `POST`, ale v pokud bude v požadavku tato hlavička s hodnotou `DELETE`, vyhodnotí se jako `DELETE`.

## Datové typy
Datový typ | Popis
---|-------
 `bool` | true / false, 1 / 0
 `string` | standardní řetězec znaků v **UTF-8**
 `int` | celé číslo
 `float` | desetinné číslo, jako oddělovač desetinných míst používejte tečku
 `array` | pole hodnot
 `object` | JSON Object
 `email` | validní emailová adresa
 `date` | datum zapsané jako řeťezec znaků dle [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
 `language` | kód jazyka dle [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
 `currency` | kód měny dle [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217)
 `country` | kód země dle [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

## API - Best practices
### Webhooks
* **Základním pravidlem je využívat Webhooky** všude, kde to jen bude možné a neposílat zbytečné pravidelné požadavky.
* Místo pravidelného stahování všech objednávek, využívejte nejlépe webhooky. V nejzažším případě můžete použít `last_update_time` na aktuální den, kterým si nové produkty stáhnete.

### Products
* **Products GET**
    * **Produkty**
        * Pokud potřebujete využívat data o produktu, například při založení nové objednávky, doporučujeme provádět stažení na základě ID produktu. Kód produktu není povinný údaj a většina klientů jej nemusí mít vyplněný.
        * Produkty není nutné stahovat každý zvlášt. Využívejte stránkování.
    * **Varianty**
        * Varianty je možné posílat v jednom požadavku, není nutné každou variantu posílat zvlášť.
        * Pokud chcete stahovat parametry jednotlivých produktů (variant), není nutné je stahovat samostatně. Lze použít `/products/parameters`, ve kterém je informace o všech produktech a variantách.
* **Products PUT**
    * **Produkty**
        * Pokud potřebujete produkty aktualizovat, aktualizujte pouze takové sekce, které potřebujete. Pokud budete například vkládat pouze překlady, nemusíte k tomu posílat váhu, zda-li má být produkt vložitelný do košíku, atd.

### Orders
* **Orders GET**
    * Pokud potřebujete mít ve svém doplňku tlačítko na stahování aktuálních objednávek, myslete nejdříve na webhooky. Pokud dané tlačítko musí být skutečně uvedeno, doporučujeme jej nastavit tak, aby nebylo možné používat opakovaně během pár sekund. Použití musí být podmíněno minimálně vždy tak, aby se dalo aktivovat až po dokončení předchozího stahování + například nějaký interval.
    * Objednávky není nutné stahovat po jedné. Využívejte stránkování.

### Owner, languages
* Tyto sekce nepotřebují pravidelné stahování. Využívejte cache

## Doplňky - Best practices
Pokud jste partnerská agentura, která vytváří doplňky do Upgates, Best practices pro doplňky najdete v naší sekci [pro vývojáře](https://www.upgates.cz/a/api-dokumentace-doplnku#doplnek_bestpractices)



## Rate Limiting
Aby nedošlo k přílišnému zahlcení API požadavky, ať už neúmyslně špatným návrhem anebo úmyslně, je API omezeno.

### Omezení přihlášení
Je omezený počet pokusů o přihlášení, tzn. že můžete udělat pouze **5 špatných přihlášení za 1 hodinu na jednu IP adresu**. Potom API zablokuje přístup a vrací stav `403`. Používá se *Floating Time Window*.

### Omezení velikosti požadavku
Je omezena velikost `PUT` požadavku, tzn. že v JSONu může být **maximálně 100 položek**. Pokud je tento počet překročen, neprovede se žádná operace (API veškerá data ignoruje) a vrací stav `413`. Další informace najdete v popisech jednotlivých endpointů.

### Zpoplatnění API
6.1.2025 bude API **zpoplatněno** [(viz ceník)](https://www.upgates.cz/cenik).
- Zpoplatnění API a [Omezení počtu požadavků](/#introduction/rate-limiting/omezeni-poctu-pozadavku) **se nevztahuje na [ověřené doplňky](https://www.upgates.cz/a/pro-vyvojare-doplnky)** vytvářené agenturou, jejichž účelem je nabídnout určitou službu všem klientům Upgates. Ověřené doplňky musí splňovat pouze [podmínky dokumentací a BestPractices](https://www.upgates.cz/a/api-dokumentace-doplnku).

### Omezení počtu požadavků
Počtem požadavků je zde míněna každá komunikace v API 

**Příklad:** 
- Pokud je poslán pokyn k založení produktu *POST /api/v2/products* přes API, je to bráno jako jeden požadavek.
- Pokud je poslán pokyn na stažení nových objednávek *GET /api/v2/orders?last_update_time_from* a následně jsou u těchto objednávek třeba změněny stavy *PUT /api/v2/order-statuses* například na "Vyřizuje se". Tak se jedná o 2 požadavky.

Z tohoto důvodu je dobré dbát na správné uplatnění Best Practices - u GET používat stránkování, a reagovat nejlépe na základě webhooků, atd.
Pokud byste si nevěděli rady, jak nejlépe vaše požadavky optimalizovat, neváhejte s námi váš konkrétní případ probrat. Rádi vám vždy poradíme.

Obracet se můžete například na naše [Discord fórum](/#introduction/discord-forum).


Omezení probíhá na zakladě dvou limitů (Základní a Individuální), které se sčítají.

#### Základní limit

Limit podle vybraného tarifu [(viz ceník)](https://www.upgates.cz/cenik).

Tarif | Hodinový limit | Denni limit | Celkem*
---|-------|-------|-------
**Bronze** | 10 | 100 | 340
**Silver** | 15 | 300 | 660
**Gold** | 50 | 600 | 1800
**Platinum** | 100 | 1500 | 3900
**Exclusive** | 100 | 1500 | 3900 (+ možnosti individuálního rozšíření)

*Celkem = hodinový limit * 24 + denní limit

**Stahování počtu požadavků probíhá vždy nejdříve z hodinového limitu a teprve poté z denního limitu. Hodinový limit se resetuje vždy počátkem nové hodiny.

#### Individuální limit

Tento individuální limit si může klient určit sám. Je tvořen samostatnými "balíčky", které jsou tvořeny po 1000 požadavcích. Těchto 1000 požadavků je rozděleno mezi denní a hodinový limit.

**Celkem tedy 600** (25 za hodinu x 24 hodin) **+ 400 den = 1000**

Maximální počet balíčků, který lze dokoupit je 60. To odpovídá 60 000 požadavků za den. Větší limit je možný pouze na tarifu **Exclusive**, pro přechod na něj kontaktujte technickou podporu.

#### Uplatnění limitu

Pro omezení se používají pevné časovné intervaly. Hodinou je myšlen interval vždy od první do poslední vteřiny aktuální hodiny, stejně tak dnem je myšlen interval od první do poslední vteřiny aktuálního dne.
Každou hodinu je k dispozici počet požadavků ve výši hodinového limitu. Požadavky nad tento limit se odečtou z denního limitu. Pokud je vyčerpán denní limit, bude k dispozici každou hodinu pouze hodinový limit.
Po překročení maximálního počtu požadavků vrací API stav `429`.
Aby bylo možné limity poznat automaticky ve vaší aplikaci, vrací API tyto hlavičky:

- `X-Rate-Limit-Hour` - aktuálně nastavený hodinový limit
- `X-Rate-Limit-Day` - aktuálně nastavený denní limit
- `X-Rate-Limit-Hour-Remaining` - zbývající počet požadavků v hodinovém limitu
- `X-Rate-Limit-Day-Remaining` - zbývající počet požadavků v denním limitu
- `X-Rate-Limit-Total-Remaining` - celkévý zbývající počet požadavků
- `Retry-After` - datum a čas kdy je možné udělat další požadavek který už nebude omezen. Časový udaj je v GMT. Hlavička je pouze v odpovědi se stavem `429`.

### Souběžné požadavky
Na API je možno provádět pouze **3 souběžné požadavky**. Pokud je tento počet překročen, API vrací stav `429`. Větší limit je možný pouze na tarifu **Exclusive**, pro přechod na něj kontaktujte technickou podporu.

**POZOR - souběžné požadavky se počítají na skupinu API přístupu nikoliv na jeden API přístup, proto pokud napojujete doplňkovou funkci kterou využívá více klentů, zvažte napojení přes náš [systém doplňků](/#reference/doplnky). Přes doplňky dostane váš API přístup vlastní skupinu a nebudou ho omezovat ostatní přístupy.**

## Stránkování
Většina endpointů podporujících metodu `GET` nevrací kompletní seznam položek, ale pouze jejich první stranu. Pomocí parametru `page` lze určit konkrétní stranu, která se ve výpisu zobrazí. Odpověď pak obsahuje ještě další parametry, pomocí kterých můžete stránkovat.
* `current_page` - aktuální strana.
* `current_page_items` - počet položek na aktuální straně.
* `number_of_pages` - celkový počet stran.
* `number_of_items` - celkový počet položek.

## Jak na API napojení (rady a tipy)
Pro maximální optimalizaci API propojení doporučujeme tyto postupy:

* Většina endpointů má možnost filtrovat položky podle času poslední změny, jazyka a dalších parametrů. Tzn. že si můžete vytáhnout např. produkty od času posledního volání API a tím ušetřit čas i množství požadavků na stahování produktů.
* V `PUT` a `POST` požadavku je možné posílat až 100 položek. Tím se zakladání nebo aktualizace výrazně zrychlí a není nutné volat API pouze s jednou položkou.
* Zvažte, jak často je třeba API volat. Mnohokrát se stává, že voláte API zbytečně často. Většinou se jedná o `GET` požadavek pro objednávky.
* Zvažte jestli u sebe pro data která se tak často nemění (seznamy číselníků jako jsou stavy objednávek atd.) nepoužívat cache.
* Používejte webhooky ([dokumentace](https://www.upgates.cz/a/webhooky)).
* Pro **každé** napojení si vytvořte **zvláštní přístup** (uživatele), kterému omezíte přístup pouze na potřebné služby. V budoucnu je poté jednodušší takové napojení deaktivovat nebo zrušit.
* Další informace najdete v sekci **[pro vývojáře](https://www.upgates.cz/pro-vyvojare)**

## Testování
Pro testování API můžete použít:
* Rozšíření [Postman](https://chrome.google.com/webstore/detail/tabbed-postman-rest-clien/coohjcphdfgbiolnekdpbcijmhambjff) pro Google Chrome.
* Rozšíření [RESTED](https://addons.mozilla.org/en-US/firefox/addon/rested/) pro Mozilla Firefox.
* [Upgates API client](https://files.upgates.com/api/upgates-api-client.zip) - jednoduchý API klient v PHP.

## Přehled změn

 Datum | Endpoint | Změna
---|-------|-------
**22.1.2025** | Všechny seznamy produktů | Nový URL parametr `can_add_to_basket_yn`
**1.1.2025** | [Zákazníci](#reference/zakaznici) (PUT) | Odebrán atribut `email`, nahrazen v login => email
-- | [Objednávka](#reference/produkty/objednavky) | Odebrán endpoint Stav objednávek `/orders/states`, nahrazen `/order-statuses`
**20.12.2024** | [Kategorie](#reference/kategorie/kategorie/seznam-kategorii) | Do seznamu kategorií přidáno pole `target_category_id` (do objektu `item`)
**31.10.2024** | [Faktury](#reference/faktury/faktury/seznam-faktur) | Do seznamu faktur přidáno pole `recycling_fee` (do objektu `item`)
**5.9.2024** | [Štítky](#reference/stiky/stitky/seznam-stitku) | Do seznamu štítků přidáno pole `color`
**20.8.2024** | [Aktualizace v31.2](https://www.upgates.cz/a/aktualizace-systemu-verze-31-2) | Aktualizace obsahovala:
-- | [Seznam faktur](#reference/faktury/faktury) | přidáno do objektu položky na fatuře pole `type`
-- | [Přesměrování](#reference/presmerovani) | Vytvoření, Seznam, Smazání
-- | [Přílohy objednávky](#reference/objednavky/prilohy-objednavky) | Vytvoření, Seznam, Smazání
 **3.5.2024** | [Skupiny doprav](#reference/doprava/skupiny-doprav) | Seznam skupin doprav
 **3.5.2024** | [Produkty](#reference/produkty) | Do vytvoření a aktualizace produktu přidáno pole `shipment_group`
**22.04.2024** | [Aktualizace v31](https://www.upgates.cz/a/aktualizace-systemu-verze-31) | Aktualizace obsahovala:
-- | [Produkty](#reference/produkty/produkty) (POST) | Vytvoření produktů
-- | [Produkty](#reference/produkty/produkty) (PUT) | Byly přidány pole `code_suplier`, `availability_id`, `manufacturer_id`, `manufacturer`, `weight`, `images`, `categories`, `vats`, `parameters` 
-- | [Dostupnosti](#reference/dostupnosti) | Vytvoření, Aktualizace, Seznam, Smazání
-- | [Parametry](#reference/parametry) | Vytvoření, Aktualizace, Seznam, Smazání
-- | [Kategorie](#reference/kategorie) | Vytvoření, Aktualizace, Seznam, Smazání
-- | [Zákaznici](#reference/zakaznici) | Vytvoření, Aktualizace, Smazání
-- | [Skupiny zákazníků](#reference/zakaznici/skupiny-zakazniku) | Vytvoření, Aktualizace, Smazání
-- | [Zákaznici](#reference/zakaznici) (GET) | Přidáno pole `base_turnover`, `turnover`, `turnover_currencry`, `vat_payer_yn`, `salutation`, `declension`, `note`
-- | [Ceníky](#reference/produkty/ceniky) (DELETE) | Smazání ceníků
-- | [Košíky](#reference/produkty/kosiky) (GET) | Přidáno pole `UUID`
-- | [Objednávka](#reference/produkty/objednavky) (GET) | Přidáno pole `UUID`, 2+1 zdarma, `parent_uuid`, `type`
-- | [Objednávka - Stavy objednávek](#reference/stavy-objednavek/stavy-objednavky) (GET) | `/api/v2/orders/states` bylo nahrazeno novým zápisem `api/v2/order-statuses` 
-- | [Výrobci](#reference/vyrobci) (GET) | Seznam výrobců
-- | [Štítky](#reference/stitky) (POST) | Přidána metoda Vytvoření
-- | [Štítky](#reference/stitky) (GET) | Přidáno stránkování
-- | [Soubory](#reference/soubory) | Založení, Seznam, Smazání, Seznam kategorií souboru
-- | [Seznam produktů](#reference/produkty/produkty) (GET) | Byly přidány pole `availability_id`, `file_id`, `set_yn`
-- | [Seznam produktů - Parametry](#reference/produkty/parametry/seznam-produktu-parametry), [Seznam produktů - Štítky](#reference/produkty/stitky/seznam-produktu-stitky), [Seznam produktů - Soubory](#reference/produkty/soubory/seznam-produktu-soubory) | Odstranění `pricelist`
-- | [Seznam produktů - zjednodušený](#reference/produkty/produkty/seznam-produktu-zjednoduseny), [Seznam produktů - Související](#reference/produkty/souvisejici/seznam-produktu-souvisejici) | Odstranění `language` a `pricelist`
 **26.2.2024** | [Seznam produktů](#reference/produkty/seznam-produktu/seznam-produktu) (GET) | přidáno pole `set_yn`, a `in_set_yn` do objektu produktu (`product`)
 **3.1.2024** | [Vytvoření kupónů](#reference/slevove-kupony/slevove-kupony/vytvoreni-kuponu) (POST) |  přidán typ `payment_shipment`
 **5.12.2023** | [Seznam produktů - ceny](#reference/produkty/seznam-produktu/seznam-produktu-ceny) (GET) | přidáno do objektu produktu (`product`) pole `action_currently_yn`, přidáno do objektu produktu (`variant`) pole `action_currently_yn`
 **7.8.2023** | [Seznam kategorií](#reference/kategorie/seznam-kategorii/seznam-kategorii) (GET) | přidán parametr `parent_id` (možnost filtrace objednávek podle ID nadřazené kategorie)
 **21.11.2023** | [Seznam produktů](#reference/produkty/seznam-produktu/seznam-produktu) (GET) | přidáno do parametrů pole `exclude_from_search_yn`, přidáno do objektu produktu (`product`) pole `exclude_from_search_yn`
 **19.10.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidán parametr `phone` (možnost filtrace objednávek podle telefonního čísla)
 **5.10.2023** | [Seznam faktur](#reference/faktury/faktury/seznam-faktur) | přidáno pole `oss_yn` a `oss_country_id`
 **1.9.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu dopravy (`shipment`) pole `packeta_carrier_id`
 **29.8.2023** | [Platby](#reference/platba/platba/seznam-plateb) | nový endpoint na seznam plateb
 **29.8.2023** | [Jazyky](#reference/e-shop/jazyky/jazyky-eshopu) | přidáno pole `default_yn`
 **25.8.2023** | [Seznam doprav](#reference/doprava/doprava/seznam-doprav) | změna pole `affiliates_yn` na `affiliates_types`
 **25.8.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu dopravy (`shipment`) pole `id`, přidáno do objektu platby (`payment`) pole `id`
 **25.8.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu dopravy (`shipment`) pole `type`, přidáno do objektu platby (`payment`) pole `type`
 **22.8.2023** | [Seznam doprav](#reference/doprava/doprava/seznam-doprav) | nový endpoint na seznam doprav
 **17.8.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu produktu (`product`) pole `adult_yn`
 **10.8.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidán parametr `status_ids` (možnost filtrace objednávek podle více stavů)
 **10.8.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu produktu (`product`) pole `image_url`
 **9.8.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu objednávky (`order`) pole `tracking_url`
 **7.8.2023** | [Seznam kategorií](#reference/kategorie/seznam-kategorii/seznam-kategorii) | přidáno do objektu kategorie (`category`) pole `metas`
 **25.7.2023** | [Vytroření poboček dopravy](#reference/doprava/pobocky-dopravy/vytvoreni-pobocky-dopravy) | přidáno pole `affiliate_id` pro vlastní ID pobočky
 **27.6.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno filtrování podle `external_order_number`
 **19.6.2023** | [Seznam produktů](#reference/produkty/seznam-produktu/seznam-produktu) | přidáno do objektu produktu (`product`) pole `supplier`
 **1.6.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu produktu (`product`) pole `supplier`
 **5.5.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidáno do objektu produktu (`product`) pole `recycling_fee`
 **21.4.2023** | [Seznam objednávek](#reference/objednavky/objednavky/seznam-objednavek) | přidány do objektu zákazníka (`customer`) pole `customer_pricelist_id`, `pricelist_name`, `pricelist_percent`
 **12.4.2023** | - | aktualizace systému na verzi 30.0, více na [blogu](https://www.upgates.cz/a/aktualizace-systemu-verze-30)

## Discord fórum
Discord fórum slouží vývojářům, kteří pracují s API a mají dotaz na naše developery. Zároveň prosíme o pochopení, že se nejedná o žádný online chat a může se stát, že nedostanete odpověď ihned.
Děkujeme za pochopení.
[Discord pozvánka na fórum](https://discord.gg/6X7VbMEVjk).


# Group Objednávky
Unikátním identifikátorem objednávek je číslo objednávky (`order_number`).

Pro práci s objednávkami lze využívat **[webhooky](https://www.upgates.cz/a/objednavky)**.

Více o objednávkách v Upgates e-shopech najdete [zde](https://www.upgates.cz/a/objednavka).

## Objednávky [/api/v2/orders]

### Vytvoření objednávky [POST]
Systém během importu objednávek přes API porovnává zákaznické údaje v e-shopu s těmi v objednávce. Když se najde zákazník se shodným emailem, pak je přiřazen k dané objednávce (je vytvořena vazba). Je to z důvodu správného výpočtu statistik.

Stejným způsobem to funguje také u dopravy, platby a produktů (variant). Ty se párují podle kódu.

Při vytvoření objednávky se posílají emaily a SMS (pokud jsou nějaké u [stavu objednávky](https://www.upgates.cz/a/stavy) nastaveny) a pokud jsou nastaveny atributy `send_emails_yn` a `send_sms_yn`.

+ Request

    + Attributes
        + send_emails_yn (bool, optional) - poslání emailu, který je navázáný na stav objednávky. Výchozí hodnota je `true`
        + send_sms_yn (bool, optional) - poslání SMS, která je navázána na stav objednávky. Výchozí hodnota je `true` (SMS služba není standardně aktivní, více najdete v [Nastavení SMS](https://upgates.cz/a/sms))
        + orders (array, required) - pole objektů s objednávkami
            + (object)
                + external_order_number (string, optional) - číslo objednávky z externího systému
                + language_id (language, required) - jazyk objednávky. Tento jazyk musí být vytvořen v administraci eshopu
                + prices_with_vat_yn (bool, optional) - příznak, jestli jsou ceny s DPH. Pokud není zadáno, bere se podle nastavení z administrace
                + status (string, optional) - název stavu objednávky z administrace (výchozí stav u nové objednávky je **Přijatá**). Seznam stavů se dá zjistit pomocí metody GET, více v sekci [Stavy objednávky](#states)
                + paid_date (date, optional) - Datum zaplacení objednávky [ISO 8601](https://en.wikipedia.org/wiki/ISO8601)
                + tracking_code (string, optional) - trackovací kód pro dopravu
                + resolved_yn (bool, optional) - příznak pro vyřešenou objednávku
                + internal_note (string, optional) - interní poznámka
                + variable_symbol (enum, optional) - variabilní symbol (maximální délka 10 znaků, jen číslice). Pokud není uvedeno, generuje se systémem z čísla obchodního případu
                    - case - doplní se automaticky variabilní symbol z čísla obchodního případu
                    - order - doplní se automaticky variabilní symbol z čísla objednávky
                    - variabilní symbol - (maximální délka 10 znaků, jen číslice) - doplní se vlastní hodnota
                + creation_time (date, optional) - čas vytvoření objednávky [ISO 8601](https://en.wikipedia.org/wiki/ISO8601)
                + customer (object, required) - zákazník
                    + email (email, required) - email zákazníka
                    + phone (string, optional) - telefon
                    + firstname_invoice (string, optional) - fakturační jméno
                    + surname_invoice (string, optional) - fakturační příjmení
                    + street_invoice (string, optional) - fakturační ulice a číslo
                    + city_invoice (string, optional) - fakturační město
                    + state_invoice (string, optional) - fakturační okres
                    + zip_invoice (string, optional) - fakturační PSČ
                    + country_id_invoice (country, optional) - fakturační země
                    + postal_yn (bool, optional) - příznak doručovací adresy. Pokud posíláte doručovací adresu, musí mít hodnotu `true`
                    + firstname_postal (string, optional) - doručovací jméno
                    + surname_postal (string, optional) - doručovací přijmení
                    + street_postal (string, optional) - doručovací ulice a číslo
                    + city_postal (string, optional) - doručovací město
                    + state_postal (string, optional) - doručovací okres
                    + zip_postal (string, optional) - doručovací PSČ
                    + country_id_postal (country, optional) - doručovací země
                    + company_postal (string, optional) - doručovací název firmy
                    + company_yn (bool, optional) - příznak, jestli je zákazník firma
                    * company (string, optional) - název firmy. Povinné, pokud je zákazníkem firma
                    + ico (string, optional) - IČO
                    + dic (string, optional) - DIČ
                    + vat_payer_yn (bool, optional) - příznak, jestli je firma plátce DPH
                    + pricelist_name (string, optional) - název ceníku
                    + pricelist_percent (int, optional) - procenta slevy ceníku (pouze informativní, s procenty se nikde nepočítá)
                    + customer_note (string, optional) - poznámka zákazníka
                + products (array, required) - pole objektů s produkty
                    + (object)
                        + code (string, optional) - kód produktu
                        + code_supplier (string, optional) - kód dodavatele
                        + ean (string, optional) - EAN produktu
                        + title (string, required) - název produktu
                        + quantity (float, optional) - počet kusů
                        + unit (string, optional) - jednotka
                        + price_per_unit (float, required) - cena za jednu jednotku produktu
                        + vat (float, required) - hodnota DPH v %
                        + buy_price (float, optional) - nákupní cena
                        + recycling_fee (float, optional) - recyklační poplatek
                        + weight (int, optional) - váha jedné jednotky produktu v gramech
                        + invoice_info (string, optional) - poznámka k produktu která se propisuje do faktury
                        + parameters (array, optional) - pole objektů s parametry produktu
                            + (object)
                                + name (string, required) - název parametru
                                + value (string, required) - hodnota parametru
                + shipment (object, optional) - doprava
                    + code (string, optional) - kód dopravy. Páruje se s kódem dopravy (ve vlastních polích) v administraci
                    + name (string, required) - název dopravy
                    + price (float, required) - cena dopravy
                    + vat (float, required) - hodnota DPH v %
                    + affiliate_id (string, optional) - ID pobočky dopravy
                    + affiliate_name (string, optional) - název pobočky
                + payment (object, optional) - platba
                    + code (string, optional) - kód platby. Páruje se s kódem platby (ve vlastních polích) v administraci
                    + name (string, required) - název platby
                    + price (float, required) - cena platby
                    + vat (float, required) - hodnota DPH v %
                    + eet_yn (bool, optional) - příznak jestli se má poslat objednávka do EET
                + metas (array, optional) - pole objektů s vlastními poli
                    + (object)
                        + key (string, required) - klíč vlastního pole
                        + value (string, required) - hodnota vlastního pole
                + invoice (object, optional) - faktura, možnost vygenerování faktury
                    + generate_yn (bool, optional) - příznak o vygenerování faktury. Pokud bude `FALSE`, nevygeneruje se  vůbec ani v případě, že je zapnuté automatické generování faktury
                    + expiration_date (date, optional) - datum splatnosti. Pokud není vyplněno, bere se aktuální datum + nastavená hodnota z administrace
                    + date_of_issuance (date, optional) - datum vystavení
                    + date_of_vat_revenue_recognition (date, optional) - datum zdanitelného plnění

+ Response 200 (application/json)

    + Attributes
        + orders (array) - pole objektů s objednávky
            + (object)
                + external_order_number (string, nullable) - externí číslo objednávky
                + order_number (string) - číslo objednávky. Pokud se objednávka nevytvoří, vrací `null`
                + order_url (string) - URL adresa, kde se nachází objednávka
                + created_yn (bool) - příznak, jestli se objednávka vytvořila
                + messages (ErrorMessage)

### Seznam objednávek [GET/api/v2/orders/{order_number}/{?order_numbers}{?creation_time_from}{?creation_time_to}{?last_update_time_from}{?paid_yn}{?status}{?status_id}{?status_ids}{?language}{?email}{?phone}{?external_order_number}{?payment_type}{?shipment_type}{?page}{?order_by}{?order_dir}]
Seznam objednávek je dostupný po jednotlivých stranách, výstup je omezený na 100 položek na stránku.

+ Parameters
    + order_number (string, optional) - číslo objednávky
    + order_numbers (string, optional) - čísla objednávek oddělená středníkem `;`
    + creation_time_from (date, optional) - vrátí objednávky vytvořené od tohoto data
    + creation_time_to (date, optional) - vrátí objednávky vytvořené do tohoto data včetně
    + last_update_time_from (date, optional) - vrátí objednávky změněné od tohoto data
    + paid_yn (bool, optional) - pokud je 1, vrátí zaplacené objednávky
    + status (string, optional) - stav objednávky. Pokud bude prázdný, vrátí objednávky, kde není zadaný žádný stav
    + status_id (int, optional) - ID stavu objednávky
    + status_ids (string, optional) - ID stavu objednávky oddělená středníkem `;`
    + language (language, optional) - jazyková mutace, na které objednávka vznikla
    + email (string, optional) - email zákazníka na objednávce
    + phone (string, optional) - telefon zákazníka na objednávce, ve formátu **MSISDN**
    + external_order_number (string, optional) - číslo objednávky z externího systému
    + payment_type (enum, optional) - typ platby
        - cash - hotově
        - cashOnDelivery - dobírka
        - command - převodem
        - paypal - PayPal
        - stripe - Stripe
        - payu - PayU
        - homecredit - Homecredit
        - tatrapay - TatraPay
        - tatracardpay - Tatra CardPay
        - comgate - ComGate
        - gopay - GoPay
        - gpwebpay - GP webpay
        - cofidis - Cofidis
        - essox - Essox
        - twisto - Twisto
        - cashOnCashRegister - hotově na pokladně
        - cardOnCashRegister - kartou na pokladně
        - thepay - ThePay
        - custom - vlastní
    + shipment_type (enum, optional) - typ dopravy
        - ceskaPosta - Česká pošta
        - slovenskaPosta - Slovenská pošta
        - ulozenka - Uloženka
        - zasilkovna - Zásilkovna
        - dpd - DPD
        - ppl - PPL
        - gls - GLS
        - custom - Vlastní doprava
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1
    + order_by (enum, optional) - řazení
        - creation_time - seřadí podle času vytvoření
        - last_update_time - seřadí podle času změny
    + order_dir (enum, optional) - směr řazení
        - asc - vzestupně
        - desc - sestupně

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + orders (array) - pole objektů s objednávkami
            + (object)
                + order_number (string) - číslo objednávky
                + order_id (int) - ID objednávky
                + case_number (string) - číslo obchodního případu
                + external_order_number (string, nullable) - číslo objednávky z externího systému
                + uuid (string) - unikátní identifikátor objednávky
                + language_id (language)
                + currency_id (currency)
                + default_currency_rate (float) - kurz pro výchozí měnu. Přepočet ceny do výchozí měny provedete jako: cena * (1 / `default_currency_rate`)
                + prices_with_vat_yn (bool) - příznak, jestli jsou ceny s DPH
                + status_id (int, nullable) - ID stavu objednávky
                + status (string, nullable) - název stavu objednávky
                + paid_date (date, nullable) - datum zaplacení objednávky
                + tracking_code (string, nullable) - trackovací kód pro dopravu
                + tracking_url (string, nullable) - trackovací URL pro dopravu
                + resolved_yn (bool) - příznak pro vyřešenou objednávku
                + oss_yn (bool) - příznak, jestli byla objednávka vytvořena v režimu OSS
                + internal_note (string, nullable) - interní poznámka
                + last_update_time (date) - datum aktualizace
                + creation_time (date) - datum vytvoření
                + variable_symbol (string) - variabilní symbol
                + total_weight (int) - celková váha objednávky v gramech
                + order_total (float) - celková cena s DPH
                + order_total_before_round (float) - celková cena s DPH před zaokrouhlením
                + order_total_rest (float) - hodnota zaokrouhlení celkové ceny s DPH
                + invoice_number (string, nullable) - číslo faktury
                + origin (enum) - původ vytvoření objednávky
                    - admin - vytvoření ručně v administraci
                    - frontend - vytvoření zákazníkem na e-shopu
                    - api - vytvoření posláním dat přes API
                    - cash–register - vytvoření přes pokladnu
                + admin_url (string) - URL do detailu objednávky v administraci
                + customer (object) - zákazník
                    + email (email, nullable) - email zákazníka, pokud `null` zákazník není vybraný
                    + phone (string, nullable) - telefon
                    + code (string, nullable) - zákaznické číslo
                    + customer_id (int, nullable) - ID zákazníka
                    + customer_pricelist_id (int, nullable) - ID ceníku zákazníka ve kterém zákazník napoupil
                    + pricelist_name (string, nullable) - název ceníku
                    + pricelist_percent (int, nullable) - procento slevy ceníku
                    + firstname_invoice (string, nullable) - fakturační jméno
                    + surname_invoice (string, nullable) - fakturační příjmení
                    + street_invoice (string, nullable) - fakturační ulice a číslo
                    + city_invoice (string, nullable) - fakturační město
                    + state_invoice (string, nullable) - fakturační okres
                    + zip_invoice (string, nullable) - fakturační PSČ
                    + country_id_invoice (country, nullable) - fakturační země
                    + postal_yn (bool) - příznak doručovací adresy
                    + firstname_postal (string, nullable) - doručovací jméno
                    + surname_postal (string, nullable) - doručovací přijmení
                    + street_postal (string, nullable) - doručovací ulice a číslo
                    + city_postal (string, nullable) - doručovací město
                    + state_postal (string, nullable) - doručovací okres
                    + zip_postal (string, nullable) - doručovací PSČ
                    + country_id_postal (country, nullable) - doručovací země
                    + company_postal (string, nullable) - doručovací název firmy
                    + company_yn (bool) - příznak, jestli je zákazník firma
                    + company (string, nullable) - název firmy
                    + ico (string, nullable) - IČO
                    + dic (string, nullable) - DIČ
                    + vat_payer_yn (bool) - příznak, jestli je firma plátce DPH
                    + customer_note (string, nullable) - poznámka zákazníka
                    + agreements (array) - pole objektů se souhlasy
                        + (object)
                            + name (string) - název souhlasu
                            + valid_to (date) - čas, do kdy je souhlas platný
                            + status (bool) - stav souhlasu
                + products (array) - pole objektů s produkty
                    + (object)
                        + product_id (int, nullable) - ID produktu z databáze (pouze orientačně, pro párování produktů slouží `code`). Pokud je `null` jedná se buď o ručně založenou položku objednávky, nebo o produkt který už není v databázi.
                        + option_set_id (int, nullable) - ID varianty z databáze (pouze orientačně, pro párování produktů slouží `code`). Bude vyplněno pouze tehdy, pokud je položka varianta produktu. Pokud je `null` jedná se buď o ručně založenou položku objednávky, produkt nemá variantu, nebo o variata už není v databázi.
                        + type (enum)
                            - product - standardní položka
                            - set - sada
                            - set_part - položka která je součástí sady, má UUID nadřazené položky což je sada samotná
                            - gift - dárek, má UUID nadřazené položky což je produkt ke kterému dárek patří
                            - discount - sleva, má UUID nadřazené položky což je produkt ke kterému sleva patří
                        + uuid (string) - unikátní identifikátor položky na objednávce
                        + parent_uuid (string, nullable) - UUID nadřazené položky
                        + code (string, nullable) - kód produktu nebo varianty produktu
                        + code_supplier (string, nullable) - kód dodavatele produktu nebo varianty produktu
                        + supplier (string, nullable) - dodavatel
                        + ean (string, nullable) - EAN produktu nebo varianty produktu
                        + title (string, nullable) - název produktu
                        + adult_yn (bool) - příznak  pouze pro dospělé
                        + unit (string) - jednotka
                        + length (string, nullable) - množství
                        + length_unit (string, nullable) - jednotka množství
                        + quantity (float) - počet jednotek
                        + price_per_unit (float) - cena za jednu jednotku produktu (cena je s nebo bez DPH podle příznaku `prices_with_vat_yn`)
                        + price (float) - celková cena za produkt (cena je s nebo bez DPH podle příznaku `prices_with_vat_yn`)
                        + price_with_vat (float) - celková cena za produkt s DPH
                        + price_without_vat (float) - celková cena za produkt bez DPH
                        + vat (float) - hodnota DPH v %
                        + buy_price (float, nullable) - nákupní cena za jednu jednotku produktu
                        + recycling_fee (float, nullable) - recyklační poplatek
                        + weight (int) - váha jedné jednotky produktu v gramech
                        + availability (string, nullable) - dostupnost produktu ve chvíli, kdy byl objednán
                        + stock_position (string, nullable) - pozice na skladě
                        + invoice_info (string, nullable) - poznámka k produktu, která se propisuje do faktury
                        + parameters (array) - pole objektů s parametry produktu
                            + (object)
                                + name (string) - název konfigurace
                                + value (string) - hodnota parametru
                        + configurations (array) - pole objektů s konfiguracemi produktu
                            + (object)
                                + name (string) - název parametru
                                + values (array) - pole hodnot
                                    + (object)
                                        + value (string) - hodnota
                                        + operation (string) - operace (+, -)
                                        + price (float) - cena konfigurace (je již připočtena k ceně produktu)
                        + categories (array) - pole objektů s kategoriemi, do kterých byl produkt zařazen v době vytvoření objednávky
                            + (object)
                                + category_id (int) - ID kategorie
                                + code (string, nullable) - kód kategorie
                        + image_url (string, nullable) - URL obrázku, hlavní obrázek z produktu
                + discount_voucher (object) - slevový kupón
                    + code (string) - kód slevového kupónu
                    + type (enum) - typ slevy
                        - percent - procentuální sleva
                        - price - pevná sleva
                    + amount (float) - výše slevy. Pokud je typ slevy `percent`, jsou to procenta. Pokud je typ `price`, jedná se o cenu
                    + discounts (array) - pole objektů se slevami rozpočítanými pro jednotlivé hladiny DPH
                        + (object)
                            + price (float) - hodnota slevy
                            + vat (float) - DPH v %
                + quantity_discount (object) - množstevní sleva
                    + type (enum) - typ slevy
                        - percent - procentuální sleva
                        - price - pevná sleva
                    + amount (float) - výše slevy. Pokud je typ slevy `percent`, jsou to procenta. Pokud je typ `price`, jedná se o cenu
                    + discounts (array) - pole objektů se slevami rozpočínanými pro jednotlivé hladiny DPH
                        + (object)
                            + price (float) - hodnota slevy
                            + vat (float) - DPH v %
                + loyalty_points (object) - věrnostní body
                    + one_point_for (float) - hodnota (cena) jednoho bodu
                    + amount (float) - výše slevy
                    + discounts (array) - pole objektů se slevami rozpočínanými pro jednotlivé hladiny DPH
                        + (object)
                            + price (float) - hodnota slevy
                            + vat (float) - DPH v %
                + shipment (object) - doprava
                    + id (int, nullable) - ID dopravy, pokud `null` jedná se o ručně založenou dopravu bez vazby na existující
                    + code (string, nullable) - kód dopravy. Páruje se s kódem dopravy (ve vlastních polích) v administraci
                    + name (string) - název dopravy
                    + price (float) - cena dopravy
                    + vat (float) - hodnota DPH v %
                    + affiliate_id (string, nullable) - ID pobočky dopravy
                    + affiliate_name (string, optional) - název pobočky
                    + type (string, nullable) - typ dopravy
                    + packeta_carrier_id (int) - ID dopravce, pouze pokud je typ dopravy Zásilkovna
                + payment (object) - platba
                    + id (int, nullable) - ID platby, pokud `null` jedná se o ručně založenou platbu bez vazby na existující
                    + code (string, nullable) - kód platby. Páruje se s kódem platby (ve vlastních polích) v administraci
                    + name (string) - název platby
                    + price (float) - cena platby
                    + vat (float) - hodnota DPH v %
                    + eet_yn (bool) - příznak, jestli se má poslat objednávka do EET
                    + type (string, nullable) - typ platby
                + attachments (array) - pole objektů s přílohami objednávky
                    + (object)
                        + id (string) - ID přílohy
                        + name (string, nullable) - název
                        + url (string) - URL
                        + code (string, nullable) - kód
                + metas (array) - pole objektů s vlastními poli
                    + (object)
                        + key (string) - klíč vlastního pole
                        + type (string) - typ vlastního pole (hodnoty mohou být: radio, checkbox, input, date, email, number, select, multiselect, textarea, formatted)
                        + value (string) - hodnota vlastního pole, v případě kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array) - pole objektů s hodnotami. V případě, kdy není hodnota vlastního pole společná pro všechny jazyky
                            + (object)
                                + language (language)
                                + value (string) - hodnota

### Aktualizace objednávek [PUT]
Při změně stavu se posílají emaily a SMS (pokud jsou nějaké u [stavu objednávky](https://www.upgates.cz/a/stavy) nastaveny) a pokud jsou nastaveny atributy `send_emails_yn` a `send_sms_yn`.

+ Request

    + Attributes
        + send_emails_yn (bool, optional) - poslání emailu při změně stavu (pokud je nějaký email nastaven). Výchozí hodnota je `true`
        + send_sms_yn (bool, optional) - poslání SMS která je navázána na stav objednávky. Výchozí hodnota je `true` (SMS služba není standardně aktivní, více najdete v [Nastavení SMS](https://upgates.cz/a/sms))
        + orders (array, optional) - pole objektů s objednávkami
            + (object)
                + order_number (string, required) - číslo objednávky
                + status (string, optional) - název stavu objednávky, stav musí být vytvořen v administraci. Seznam stavů se dá zjistit pomocí metody GET `/api/v2/orders/states`
                + status_id (int, optional) - ID stavu objednávky, stav musí být vytvořen v administraci. Seznam stavů se dá zjistit pomocí metody GET `/api/v2/orders/states`
                + paid_date (date, optional) - datum zaplacení objednávky [ISO 8601](https://en.wikipedia.org/wiki/ISO8601)
                + tracking_code (string, optional) - trackovací kód pro dopravu
                + resolved_yn (bool, optional) - příznak pro vyřešenou objednávku
                + internal_note (string, optional) - interní poznámka
                + metas (array, optional) - pole objektů s vlastními poli
                    + (object)
                        + key (string, required) - klíč vlastního pole
                        + value (string, required) - hodnota vlastního pole
                + invoice (object, optional) - faktura, možnost vygenerování faktury 
                    + generate_yn (bool, optional) - příznak o vygenerování faktury. Pokud bude `FALSE`, nevygeneruje se vůbec ani v případě, že je zapnuté automatické generování faktury. Pokud faktura už existuje, provede se její aktualizace podle dat objednávky.
                    + expiration_date (date, optional) - datum splatnosti. Pokud není vyplněno, bere se aktuální datum + nastavená hodnota z administrace [ISO 8601](https://en.wikipedia.org/wiki/ISO8601)
                    + date_of_issuance (date, optional) - datum vystavení [ISO 8601](https://en.wikipedia.org/wiki/ISO8601)
                    + date_of_vat_revenue_recognition (date, optional) - datum zdanitelného plnění [ISO 8601](https://en.wikipedia.org/wiki/ISO8601)

+ Response 200 (application/json)

    + Attributes
        + orders (array) - pole objektů z objednávky
            + (object)
                + order_number (string) - číslo objednávky
                + order_url (string) - URL adresa, kde se nachází objednávka
                + updated_yn (bool) - příznak, jestli se objednávka aktualizovala
                + messages (ErrorMessage)

### Smazání objednávek [DELETE/api/v2/orders/{?order_number}{?order_numbers}]

+ Parameters
    + order_number (string, optional) - číslo objednávky
    + order_numbers (string, optional) - čísla objednávek oddělená středníkem `;`

+ Response 200 (application/json)

    + Attributes
        + orders (array) - pole objektů s objednávky
            + (object)
                + order_number (string) - číslo objednávky
                + deleted_yn (bool) - příznak, jestli je objednávka smazaná
                + messages (ErrorMessage)

## Objednávka v PDF [/api/v2/orders/{order_number}/pdf]

### Objednávka v PDF [GET]
Vrací dokument objednávky ve formátu PDF.

+ Parameters
    + order_number (string, required) - číslo objednávky

+ Response 200 (application/pdf)

## Historie [/api/v2/orders/history]

### Přidání záznamu do historie objednávky [POST/api/v2/orders/{order_number}/history]
Přidá záznam do historie objednávky. Jeden pořadavek znamená přidání jednoho záznamu do historie. Slouží hlavně pro systémy třetích stran, které chtějí informovat administrátora e-shopu o tom, že proběhla nějaká událost. Čas události nelze upravovat. Pokud chcete, můžete si poslat čas v datech události.

+ Parameters
    + order_number (string, required) - číslo objednávky

+ Request

    + Attributes
        + data (array, required) - pole objektů s daty historie
            + (object)
                + name (string, required) - název, ořízne se na délku max. 50 znaků a odstraní se HTML značky
                + value (string, required) - hodnota, ořízne se na délku max. 500 znaků a odstraní se HTML značky

+ Response 200 (application/json)

### Historie objednávky [GET/api/v2/orders/{order_number}/history]
Vrací seznam událostí z historie objednávky. Data historie mohou obsahovat HTML značky.

+ Parameters
    + order_number (string, required) - číslo objednávky

+ Response 200 (application/json)

    + Attributes
        + number_of_items (int) - počet položek historie
        + history (array) - pole objektů s událostmi historie
            + (object)
                + event (string) - název události
                + user_name (string) - jméno uživatele, který událost provedl
                + changes (object) - pole objektů se změnami
                    + name (string) - název zněny
                    + before (string, nullable) - hodnota před změnou
                    + after (string, nullable) - hodnota po změně
                + admin_yn (bool) - příznak, jestli událost pochází z eshopu nebo z administrace. Pokud pochází událost z API, bude `true`
                + data (array) - pole objektů s daty
                    + (object)
                        + name (string) - název
                        + value (string) - hodnota
                + creation_time (date) - čas události

## Přílohy objednávky [/api/v2/orders/files]

### Přidání souboru [POST/api/v2/orders/{order_number}/file]
Poslání obsahu souboru přes **form-data**, parametry jsou:
- **file** (*file, required*) - obsah souboru
- **file_name** (*string, optional*) - název souboru
- **code** (*string, optinal*) - kód přílohy

+ Parameters
    + order_number (string, optional) - číslo objednávky

+ Response 200 (application/json)

    + Attributes
        + file (object)
            + id (string) - ID souboru
            + name (string) - název
            + mimetype (string) - MIMETYPE
            + size (string) - velikost v bytech
            + type (enum) - typ
                - image - obrázek
                - file - soubor
                - video - video
            + url (string) - URL obrázku
        + inserted_yn (bool) - vytvořeno
        + messages (ErrorMessage) - chybová zpráva

### Přidání odkazů [POST/api/v2/orders/{order_number}/urls]

+ Parameters
    + order_number (string, required) - číslo objednávky

+ Request

    + Attributes
        + urls (array, required) - pole objektů s daty přílohy
            + (object)
                + name (string, required) - název
                + url (string, required) - URL
                + code (string, optional) - kód

+ Response 200 (application/json)

    + Attributes
        + urls (object)
            + id (int) - ID přílohy
            + name (string) - název
            + url (string) - URL
            + code (string) - kód
            + inserted_yn (bool) - vytvořeno
            + messages (ErrorMessage) - chybová zpráva
        + messages (ErrorMessage) - chybová zpráva

### Smazání přílohy [DELETE/api/v2/orders/{order_number}/attachments{?ids}]

+ Parameters
    + order_number (string, required) - číslo objednávky
    + ids (string) - ID přílohy objednávky oddělené středníkem `;` nebo jako pole

+ Response 200 (application/json)

    + Attributes
        + attachments (object)
            + id (int) - ID přílohy objednávky
            + code (string) - kód přílohy objednávky
            + deleted_yn (bool) - příznak, jestli se stav smazal
            + messages (ErrorMessage)


<!-- ZRUŠENO D.H. 1.1.2025 ## Stavy objednávky [/api/v2/orders/states]
**Tento endpoint již není podporován a v dalších verzích bude zrušen! Používejte [nový endpoint na stavy objednávek](/#reference/stavy-objednavky)**

### Stavy objednávky [GET]
Vrací seznam stavů objednávek. V požadavku pro aktualizaci nebo vytvoření objednávky se dá použít název stavu v jakémkoliv jazyce.

+ Response 200 (application/json)

    + Attributes
        + states (array) - pole objektů se stavy
            + (object)
                + id (int) - ID stavu
                + type (enum) - typ stavu. Pokud je hodnota `null`, pak se jedná o vlastní stav. Jinak jsou to systémové stavy
                    - Received - Přijatá
                    - Canceled - Storno
                    - PaymentSuccessful - Platba úspěšná
                    - PaymentFailed - Platba selhala
                    - PaymentCanceled - Platba zrušena
                    - PaymentInProcess - Platba probíhá
                    - Unresolved - Nedořešená
                + color (string) - barva pro odlišení stavu v HTML HEX formátu
                + names (object) - názvy stavu objednávky v jednotlivých jazycích. Klíč v objektu je kód jazyka podle **ISO 8601** a hodnota je název stavu. Např. `{ "cs": "Přijatá" }`
-->

# Group Stavy objednávky

## Stavy objednávky [/api/v2/order-statuses]
Typy stavů Homecredit se zakládají automaticky při zapnuti doplňku Homecredit.

Pro práci se stavy objednávky lze využívat **[webhooky](https://www.upgates.cz/a/stav-objednavek)**.

Více o stavech objednávek v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/stavy).

### Vytvoření stavu [POST]
Typ se u nově založeného stavu dává vždy vlastní (`Custom`).

+ Request

    + Attributes
        + color (string, optional) - barva stavu v HTML HEX formátu
        + descriptions (array, required)
            + (object)
                + language_id (language)
                + name (string) - název
        + mark_resolved_yn (bool, optional) - příznak označovat objednávku jako vyřešenou, pokud není uvedeno bude `FALSE`
        + mark_paid_yn (bool, optional) - příznak označovat objednávku jako zaplacenou, pokud není uvedeno bude `FALSE`

+ Response 200 (application/json)

    + Attributes
        + order_status (object)
            + id (int) - ID stavu
            + created_yn (bool) - příznak, jestli se stav vytvořil
            + messages (ErrorMessage)

### Seznam stavů [GET/api/v2/order-statuses/{id}/{?type}]

+ Parameters
    + id (string, optional) - ID stavu
    + type (enum, optional) - typ stavu
        - Received - přijatá
        - Canceled - storno
        - Sent - odeslaná
        - PaymentSuccessful - platba úspěšná
        - PaymentFailed - platba selhala
        - PaymentCanceled - platba zrušena
        - PaymentInProcess - platba probíhá
        - Unresolved - nedořešená
        - Custom - vlastní
        - HomecreditProcessing - Homecredit - probíhá
        - HomecreditRejected - Homecredit - zamítnuto
        - HomecreditApproved - Homecredit - schváleno
        - HomecreditReadyToShip - Homecredit - připraveno k odeslání
        - HomecreditSent - Homecredit - odesláno
        - HomecreditDelivered - Homecredit - doručeno
        - HomecreditPaid - Homecredit - zaplaceno
        - HomecreditCanceled - Homecredit - zrušeno


+ Response 200 (application/json)

    + Attributes
        + order_statuses (array) - pole objektů se stavy
            + (object)
                + id (int) - ID stavu
                + type (enum) - typ stavu
                    - Received - přijatá
                    - Canceled - storno
                    - Sent - odeslaná
                    - PaymentSuccessful - platba úspěšná
                    - PaymentFailed - platba selhala
                    - PaymentCanceled - platba zrušena
                    - PaymentInProcess - platba probíhá
                    - Unresolved - nedořešená
                    - Custom - vlastní
                    - HomecreditProcessing - Homecredit - probíhá
                    - HomecreditRejected - Homecredit - zamítnuto
                    - HomecreditApproved - Homecredit - schváleno
                    - HomecreditReadyToShip - Homecredit - připraveno k odeslání
                    - HomecreditSent - Homecredit - odesláno
                    - HomecreditDelivered - Homecredit - doručeno
                    - HomecreditPaid - Homecredit - zaplaceno
                    - HomecreditCanceled - Homecredit - zrušeno
                + color (string) - barva stavu v HTML HEX formátu
                + descriptions (array)
                    + (object)
                        + language_id (language)
                        + name (string) - název
                + mark_resolved_yn (bool) - příznak označovat objednávku jako vyřešenou
                + mark_paid_yn (bool) - příznak označovat objednávku jako zaplacenou
                + last_update_time (date) - čas poslední aktualizace
                + creation_time (date) - čas vytvoření

### Aktualizace stavu [PUT]

+ Request

    + Attributes
        + id (int, required) - ID existujícího stavu
        + color (string, optional) - barva stavu v HTML HEX formátu
        + descriptions (array, required)
            + (object)
                + language_id (language)
                + name (string) - název
        + mark_resolved_yn (bool, optional) - příznak označovat objednávku jako vyřešenou
        + mark_paid_yn (bool, optional) - příznak označovat objednávku jako zaplacenou

+ Response 200 (application/json)

    + Attributes
        + order_status (object)
            + id (int) - ID stavu
            + updated_yn (bool) - příznak, jestli se stav aktualizoval
            + messages (ErrorMessage)

### Smazání stavu [DELETE/api/v2/order-statuses/{id}]

+ Parameters
    + id (int, required) - ID stavu

+ Response 200 (application/json)

    + Attributes
        + order_status (object)
            + id (int) - ID stavu
            + deleted_yn (bool) - příznak, jestli se stav smazal
            + messages (ErrorMessage)


# Group Faktury
Unikátním identifikátorem faktur je číslo faktury (`invoice_number`). Více o fakturách v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/dokument-faktura).

## Faktury [/api/v2/invoices]
Více o fakturaci v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/dokument-faktura).

### Seznam faktur [GET/api/v2/invoices/{invoice_number}{?invoice_numbers}{?creation_time_from}{?last_update_time_from}{?page}{?paid_yn}{?type}]
Některé údaje nejsou dostupné přímo ve faktuře, ale v detailu související objednávky. [Více zde](#reference/objednavky).
Seznam faktur je dostupný po jednotlivých stranách, výstup je omezený na 100 položek na stránku.

+ Parameters
    + invoice_number (string, optional) - číslo faktury
    + invoice_numbers (string, optional) - čísla faktur oddělená středníkem `;`
    + creation_time_from (date, optional) - vrátí faktury vytvořené od tohoto data
    + last_update_time_from (date, optional) - vrátí faktury změněné od tohoto data
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1
    + paid_yn (bool, optional) - pokud je 1, vrátí zaplacené faktury
    + type (enum, optional) - typ dokladu
        - invoice - faktura
        - creditNote - dobropis
        - receipt - účtenka

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + invoices (array) - pole objektů s fakturami
            + (object)
                + invoice_number (string) - číslo faktury
                + related_invoice_number (string, nullable) - číslo související faktury, **pouze u dobropisu**
                + type (enum) - typ faktury, hodnoty:
                    - invoice - faktura
                    - creditNote - dobropis
                    - receipt - účtenka
                + order_number (string) - číslo objednávky
                + external_order_number (string, nullable) - číslo objednávky z externího systému
                + case_number (string, nullable) - číslo obchodního případu
                + language_id (language)
                + currency_id (currency)
                + date_of_issuance (date) - datum vystavení
                + date_of_vat_revenue_recognition (date) - datum zdanitelného plnění
                + date_of_expiration (date) - datum splatnosti
                + creation_time (date) - datum vytvoření
                + variable_symbol (string) - variabilní symbol
                + specific_symbol (string) - specifický symbol
                + payment (string) - platba
                + paid_yn (bool) - zaplaceno
                + paid_date (date, nullable) - datum zaplacení
                + oss_yn (bool) - příznak jestli je faktura v režimu OSS
                + oss_country_id (country, nullable) - země režimu OSS
                + total_rest (float) - zaokrouhlení celkové částky
                + total_with_vat (float) - celková částka s DPH
                + total_without_vat (float) - celková částka bez DPH
                + note (string, nullable) - poznámka
                + invoice_pdf_url (string) - URL na PDF fakturu
                + supplier (object) - dodavatel
                    + email (string, nullable) - email
                    + phone (string, nullable) - telefon
                    + name (string, nullable) - jméno osoby nebo název firmy
                    + street (string, nullable) - ulice a číslo
                    + city (string, nullable) - město
                    + zip (string, nullable) - PSČ
                    + country_id (country, nullable) - stát
                    + company_yn (bool) - příznak, jestli je firma
                    + var_payer_yn (bool) - příznak, jestli je plátce DPH
                    + ico (string, nullable) - IČO
                    + dic (string, nullable) - DIČ
                    + account_number (string, nullable) - číslo účtu
                    + iban (string, nullable) - IBAN
                    + swift (string, nullable) - SWIFT
                    + web (string, nullable) - webová stránka
                + customer (object) - zákazník
                    + email (string, nullable) - email
                    + phone (string, nullable) - telefon
                    + name (string, nullable) - jméno osoby nebo název firmy
                    + street (string, nullable) - ulice a číslo
                    + city (string, nullable) - město
                    + zip (string, nullable) - PSČ
                    + country_id (country, nullable) - stát
                    + company_yn (bool) - příznak, jestli je zákazník firma
                    + ico (string, nullable) - IČO
                    + dic (string, nullable) - DIČ
                + items (array) - pole objektů s položkami
                    + (object)
                        + code (string, nullable) - kód
                        + name (string) - název
                        + description (string) - popis
                        + quantity (float) - počet kusů
                        + unit (string) - jednotka
                        + vat (float) - procentuální sazba DPH
                        + price_per_unit_with_vat (float) - cena za jednotku s DPH
                        + price_per_unit_without_vat (float) - cena za jednotku bez DPH
                        + price_with_vat (float) - cena za s DPH
                        + price_without_vat (float) - cena za bez DPH
                        + recycling_fee (float, optional) - recyklační poplatek
                        + type (enum) - typ položky, hodnoty:
                            - product - produkt
                            - discount - sleva
                            - shipment - doprava
                            - payment - platba
                + eet (object) - informace o EET (bude vyplněno pouze u faktury typu účtenka)
                    + send_yn (bool) - příznak, jestli se má poslat do EET. Určuje systém na základě nastavení v e-shopu
                    + production_yn (bool) - pokud je hodnota 0, není v e-shopu aktivován produkční režim napojení na EET a data se do EET posílají v neprodukčním testovacím režimu
                    + id_provoz (string) - ID provozovny
                    + id_pokl (string) - ID pokladního zažízení
                    + rezim (enum) - režim EET, hodnoty:
                        - common - běžný
                        - simplified - zjednodušený
                    + bkp (string) - BKP (bezpečnostní kód poplatníka)
                    + fik (string) - FIK (fiskální identifikační kód)
                    + pkp (string) - PKP (podpisový kód poplatníka)
                + recapitulation_currency_id (currency) - měna rekapitulace DPH. Pokud bude faktura v jiné měně než je měna země provozovatele e-shopu, jinými slovy pokud e-shop prodává do zahraničí, bude zde měna provozovatele eshopu. Tedy měna, ve které je přehled DPH. Pokud není uvedeno, je přehled DPH ve měně faktury.
                + recapitulation_currency_rate (float) - kurz měny rekapitulace DPH
                + recapitulation_vats (array) - přehled DPH, pole objektů s jednotlivými hladinami DPH. Klíč pole je procentuální sazba DPH
                    + (object)
                        + base (float) - základ
                        + vat (float) - výše DPH
                        + total (float) - celkem s DPH
                + recapitulation_vats_total (object) - přehled DPH celkem
                    + base (float) - základ
                    + vat (float) - výše DPH
                    + total (float) - celkem s DPH

## PDF faktura [/api/v2/invoices/{invoice_number}/pdf]

### PDF faktura [GET]
Vrací fakturu ve formátu PDF.

+ Parameters
    + invoice_number (string, required) - číslo faktury

+ Response 200 (application/pdf)


# Group Produkty
Unikátním identifikátorem produktů a variant je kód (`code`). **POZOR!** Kód produktu není povinný. Doporučujeme využívat při komunikaci spíše ID.
Pokud produkt nemá vyplněný kód, není možné jej založit, editovat a ani mazat.

Pro práci s produkty lze využívat **[webhooky](https://www.upgates.cz/a/produkty-1)**.

Více o produktech v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/seznamy-produktu).

## Produkty [/api/v2/products]

**Seznamy produktů:**
- produkty jsou dostupné po jednotlivých stranách, výstup je omezený na 50 položek na stránku. Pokud bude jakákoliv hodnota u variant `null`, dědí se z produktu.
- hodnota slevy na produkt (`product_discount`) + sleva na výrobce + sleva na kategorii (bere se sleva z hlavní kategorie, ve které je produkt zařazen). Výsledná hodnota slevy se omezí na hodnotu z nastavení *Maximální procento slevy*.

### Vytvoření produktů [POST]
+ produkty a varianty se párují podle hodnoty `code`, ta musí být unikátní
+ pokud bude jakákoliv hodnota u variant `null` dědí se od produktu
+ štítky u variant - když budou mít atributy `active_yn`, `active_from`, `active_to` hodnotu `NULL`, bude se štítek dědit z produktu
+ maximální počet produktů a variant založených při jednom pořadavku je 100, tzn. 100 produktů celkem a maximálně 100 variant v každém produktu. Při poslání většího počtu se všechny položky ignorují.

+ Request
    + Attributes
        + products (array, optional) - pole objektů s produkty
            + (object)
                + code (string, optional) - kód produktu
                + code_supplier (string, optional) - kód dodavatele
                + active_yn (bool, optional) - zobrazit produkt na webu
                + archived_yn (bool, optional) - archivovaný produkt
                + replacement_product_code (string, optional) - kód náhradního produktu, uvádět pouze pokud je produkt archivovaný
                + ean (string, optional) - EAN
                + descriptions (array, required)
                    + (object)
                        + language (language, required)
                        + active_yn (bool, optional) - aktivní v jazykové mutaci, výchozí je `TRUE`. Použitelné pouze pro deaktivaci jazykové mutace (skrytí produktu v jazykove mutaci)
                        + title (string, required) - název produktu. Povinné pouze v případě, že se nově zapíná jazyková mutace
                        + short_description (string, optional) - krátký popis, bez HTML formátování
                        + long_description (string, optional) - dlouhý popis, může obsahovat formátování pomocí HTML značek
                        + seo_title (string, optional) - SEO titulek
                        + seo_description (string, optional) - META popisek stránky produktu
                        + seo_url (string, optional) - vlastní koncovka URL adresy
                + stock (float, optional) - počet jednotek na skladě
                + stock_position (string, optional) - pozice na skladě
                + limit_orders (enum, optional) - omezení objednání
                    - 0 - vypnuto
                    - 1 - zapnuto
                    - sale - pouze pokud je produkt ve výprodeji
                    - null - dědí z nastavení eshopu
                + availability_id (int, optional) - ID dostupnosti
                + availability (string, optional) - název dostupnosti. Neimportuje se u položek s nastavením [dostupnosti dle stavu zásob](https://upgates.cz/a/nastaveni-dostupnosti-dle-stavu-zasob). Pokud však v tomto případě stav zásob není definován (hodnota `stock` musí být prázdná nebo úplně chybět), dostupnost se importuje
                + manufacturer_id (int, optional) - ID výrobce
                + manufacturer (string, optional) - název výrobce, pokud nebude existovat, založí
                + weight (int, optional) - váha v gramech. Zaokrouhlete na celá čísla.
                + shipment_group (string, nullable) - skupina doprav
                + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
                + adult_yn (bool, optional) - pouze pro dospělé
                + images (array, optional) - pole objektů s obrázky
                    + (object)
                        + file_id (int, optional) - ID souboru, hledá se soubor s konkrétním ID, soubor musí být typu `image` nebo `video`
                        + url (string, optional) - URL, obrázky se nestahují hned, ale jsou staženy na pozadí. Pokud chcete posílat obrázky tak aby byly vidět hned, pouzijte endpoint [Vložení obrázku](/#reference/produkty/produkty/pridani-obrazku)
                        + main_yn (bool, optional) - příznak pro hlavní obrázek. Pokud není definováno nebo je u šech obrázků `FALSE`, vezme se jako hlavní obrázek první
                        + list_yn (bool, optional) - příznak pro seznamový obrázek. Pokud není definováno nebo je u šech obrázků `FALSE`, vezme se jako seznamový obrázek první
                        + position (int, optional) - pozice
                + categories (array, optional) - pole objektů s kategoriemi
                    + (object)
                        + category_id (int, optional) - ID kategorie  Nelze napárovat na kategorie, které mají v parentid NULL.
                        + code (string, optional) - kód kategorie
                        + main_yn (bool, optional) - příznak pro hlavní kategorii. Pokud není definováno nebo je u šech kategorií `FALSE`, vezme se jako hlavní kategorie první
                        + position (int, optional) - pozice v kategorii
                + prices (array, optional) - pole objektů s cenami
                    + (object)
                        + language (language, required)
                        + pricelists (array, optional) - pole objektů s ceníky
                            + (object)
                                + name (string, required) - název ceníku. Pokud je při importu prázdné, chápe se jako výchozí ceník
                                + price_original (float, optional) - původní cena. Základní ceníková cena, od které se odvozují další
                                + product_discount (float, optional) - sleva na produkt v procentech
                                + price_sale (float, optional) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                        + price_purchase (float, optional) - nákupní cena, interní údaj pro orientaci administrátora
                        + price_common (float, optional) - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech
                + vats (object) - objekt s DPH v jednotlivých zemích (klíč každé položky v objektu je typu *country*)
                + labels (array, optional) - štítky
                    + (object)
                        + label_id (int, optional) - ID štítku
                        + name (object, optional) - objekt s názvy štítků v jednotlivých jazycích (klíč každé položky v objektu je typu *language*). Příklad vyplněné hodnoty najdete v *name* u GET ../api/v2/products/labels.
                        + active_yn (bool, optional) - aktivní
                        + active_from (date, optional) - aktivní od data
                        + active_to (date, optional) - aktivní do data
                + parameters (array, optional) - parametry
                    + (object)
                        + id (int, optional) - ID parametru
                        + descriptions (array) - název parametru
                            + (object)
                                + language (language, required)
                                + name (string, required)
                        + values (array, required) - hodnoty
                            + (object)
                                + id (int) + ID hodnoty
                                + descriptions (array)
                                    + (object)
                                        + language (language, required)
                                        + value (string, required)
                + variants (array, optional) - pole objektů s variantami
                    + (object)
                        + code (string, required) - kód varianty
                        + code_supplier (string, optional) - kód dodavatele
                        + active_yn (bool, optional) - zobrazit variantu na webu
                        + main_yn (bool, optional) - hlavní varianta
                        + ean (string, optional) - EAN
                        + stock (float, optional) - počet jednotek na skladě
                        + stock_position (string, optional) - pozice na skladě
                        + availability_id (int, optional) - ID dostupnosti
                        + availability (string, optional) - název dostupnosti. Neimportuje se u položek s nastavením [dostupnosti dle stavu zásob](https://upgates.cz/a/nastaveni-dostupnosti-dle-stavu-zasob). Pokud však v tomto případě stav zásob není definován (hodnota `stock` musí být prázdná nebo úplně chybět), dostupnost se importuje
                        + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
                        + image (object, optional) - obrázek varianty
                            + file_id (int, optional) - ID existujícího souboru, soubor musí být typu `image`
                            + url (string, optional) - URL adresa, obrázek se nestahuje hned, ale je stažen na pozadí
                        + prices (array, optional) - pole objektů s cenami
                            + (object)
                                + language (language, required)
                                + pricelists (array, optional) - pole objektů s ceníky
                                    + (object)
                                        + name (string, required) - název ceníku. Pokud je při importu prázdné, chápe se jako výchozí ceník
                                        + price_original (float, optional) - původní cena. Základní ceníková cena od které se odvozují další
                                        + product_discount (float, optional) - sleva na produkt v procentech
                                        + price_sale (float, optional) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                                + price_purchase (float, optional) - nákupní cena, interní údaj pro orientaci administrátora
                                + price_common (float, optional) - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech
                        + labels (array, optional)
                            + (object)
                                + label_id (int, optional) - ID štítku
                                + name (object, optional) - objekt s názvy štítků v jednotlivých jazycích (klíč každé položky v objektu je typu *language*). Příklad vyplněné hodnoty najdete v *name* u GET ../api/v2/products/labels.
                                + active_yn (bool, optional) - aktivní
                                + active_from (date, optional) - aktivní od data
                                + active_to (date, optional) - aktivní do data
                        + parameters (array, optional) - parametry varianty
                            + (object)
                                + id (int, optional) - ID parametru
                                + descriptions (array) - název parametru
                                    + (object)
                                        + language (language, required)
                                        + name (string, required)
                                + values (array, required) - hodnoty
                                    + (object)
                                        + id (int) + ID hodnoty
                                        + descriptions (array)
                                            + (object)
                                                + language (language, required)
                                                + value (string, required)
                        + metas (array, optional) - pole objektů s vlastnimi poli
                            + (object)
                                + key (string, optional) - klíč vlastního pole. Vlastní pole musí být v administraci založeno.
                                + value (string, optional) - hodnota vlastního pole. Použijte v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                                + values (array, optional) - pole hodnot vlastního pole podle jazykových mutací
                                    + (object)
                                        + language (language, optional) - jazyk hodnoty
                                        + value (string, optional) - hodnota
                + metas (array, optional) - pole objektů s vlastnimi poli
                    + (object)
                        + key (string, optional) - klíč vlastního pole. Vlastní pole musí být v administraci založeno.
                        + value (string, optional) - hodnota vlastního pole. Použijte v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array, optional) - pole hodnot vlastního pole podle jazykových mutací
                            + (object)
                                + language (language, optional) - jazyk hodnoty
                                + value (string, optional) - hodnota

+ Response 200 (application/json)

    + Attributes
        + products (array) - pole objektů s produkty
            + (object)
                + product_id (int) - ID produktu
                + code (string, nullable) - kód produktu
                + product_url (string) - URL adresa, kde se nachází produkt
                + inserted_yn (bool) - příznak, jestli se produkt založil
                + messages (ErrorMessage)
                + variants (array)
                    + (object)
                        + variant_id (int) - ID varianty
                        + code (string, nullable) - kód varianty
                        + inserted_yn (bool) - příznak, jestli se varianta založila
                        + messages (ErrorMessage)

### Aktualizace produktu [PUT]
+ produkty a varianty se párují podle hodnoty `code`, ta musí být unikátní
+ pokud bude jakákoliv hodnota u variant `null` dědí se od produktu
+ štítky u variant - když budou mít atributy `active_yn`, `active_from`, `active_to` hodnotu `NULL`, bude se štítek dědit z produktu
+ maximální počet produktů aktualizovaných v jedno požadavku je 100. Při poslání většího počtu se všechny položky ignorují.

+ Request
    + Attributes
        + products (array, optional) - pole objektů s produkty
            + (object)
                + code (string, required) - kód produktu, páruje se podle existující hodnoty v databázi
                + code_supplier (string, optional) - kód dodavatele
                + active_yn (bool, optional) - zobrazit produkt na webu
                + archived_yn (bool, optional) - archivovaný produkt
                + replacement_product_code (string, optional) - kód náhradního produktu, pouze pokud je produkt archivovaný
                + ean (string, optional) - EAN
                + descriptions (array, optional)
                    + (object)
                        + language (language, required)
                        + active_yn (bool, optional) - aktivní v jazykové mutaci, výchozí je `TRUE`. Použitelné pouze pro deaktivaci jazykové mutace (skrytí produktu v jazykove mutaci)
                        + title (string, optional) - název produktu. Povinné pouze v případě, že se nově zapíná jazyková mutace
                        + short_description (string, optional) - krátký popis, bez HTML formátování
                        + long_description (string, optional) - dlouhý popis, může obsahovat formátování pomocí HTML značek
                        + seo_title (string, optional) - SEO titulek
                        + seo_description (string, optional) - META popisek stránky produktu
                        + seo_url (string, optional) - vlastní koncovka URL adresy
                + stock (float, optional) - počet jednotek na skladě
                + stock_increment (float, optional) - provede změnu počtu jednotek na skladě o určitou hodnotu. Používají se "+" "-" pro přičítání a odčítání. Maximální počet míst je 10 a zápis se provede pouze tehdy, pokud je pole pro sklad vyplněno.
                + stock_position (string, optional) - pozice na skladě
                + limit_orders (enum, optional) - omezení objednání
                    - 0 - vypnuto
                    - 1 - zapnuto
                    - sale - pouze pokud je produkt ve výprodeji
                    - null - dědí z nastavení eshopu
                + availability_id (int, optional) - ID dostupnosti
                + availability (string, optional) - název dostupnosti. Neimportuje se u položek s nastavením [dostupnosti dle stavu zásob](https://upgates.cz/a/nastaveni-dostupnosti-dle-stavu-zasob). Pokud však v tomto případě stav zásob není definován (hodnota `stock` musí být prázdná nebo úplně chybět), dostupnost se importuje
                + manufacturer_id (int, optional) - ID výrobce
                + manufacturer (string, optional) - název výrobce, pokud nebude existovat, založí
                + weight (int, optional) - váha v gramech
                + shipment_group (string, nullable) - skupina doprav
                + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
                + adult_yn (bool, optional) - pouze pro dospělé
                + images (array, optional) - pole objektů s obrázky
                    + (object)
                        + file_id (int, optional) - ID souboru, hledá se soubor s konkrétním ID, soubor musí být typu `image` nebo `video`
                        + url (string, optional) - URL, obrázky se nestahují hned, ale jsou staženy na pozadí. Pokud chcete posílat obrázky tak aby byly vidět hned, pouzijte endpoint [Vložení obrázku](/#reference/produkty/produkty/pridani-obrazku)
                        + main_yn (bool, optional) - příznak pro hlavní obrázek. Pokud není definováno nebo je u šech obrázků `FALSE`, vezme se jako hlavní obrázek první
                        + list_yn (bool, optional) - příznak pro seznamový obrázek. Pokud není definováno nebo je u šech obrázků `FALSE`, vezme se jako seznamový obrázek první
                        + position (int, optional) - pozice
                + categories (array, optional) - pole objektů s kategoriemi
                    + (object)
                        + category_id (int, optional) - ID kategorie
                        + code (string, optional) - kód kategorie
                        + main_yn (bool, optional) - příznak pro hlavní kategorii. Pokud není definováno nebo je u šech kategorií `FALSE`, vezme se jako hlavní kategorie první
                        + position (int, optional) - pozice v kategorii
                + prices (array, optional) - pole objektů s cenami
                    + (object)
                        + language (language, required)
                        + pricelists (array, optional) - pole objektů s ceníky
                            + (object)
                                + name (string, required) - název ceníku. Pokud je při importu prázdné, chápe se jako výchozí ceník
                                + price_original (float, optional) - původní cena. Základní ceníková cena, od které se odvozují další
                                + product_discount (float, optional) - sleva na produkt v procentech
                                + price_sale (float, optional) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                        + price_purchase (float, optional) - nákupní cena, interní údaj pro orientaci administrátora
                        + price_common (float, optional) - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech
                + vats (object) - objekt s DPH v jednotlivých zemích (klíč každé položky v objektu je typu *country*)
                + labels (array, optional) - štítky
                    + (object)
                        + label_id (int, optional) - ID štítku
                        + name (object, optional) - objekt s názvy štítků v jednotlivých jazycích (klíč každé položky v objektu je typu *language*)
                        + active_yn (bool, optional) - aktivní
                        + active_from (date, optional) - aktivní od data
                        + active_to (date, optional) - aktivní do data
                + parameters (array, optional) - parametry
                    + (object)
                        + id (int, optional) - ID parametru
                        + descriptions (array) - název parametru
                            + (object)
                                + language (language, required)
                                + name (string, required)
                        + values (array, required) - hodnoty
                            + (object)
                                + id (int) + ID hodnoty
                                + descriptions (array)
                                    + (object)
                                        + language (language, required)
                                        + value (string, required)
                + variants (array, optional) - pole objektů s variantami
                    + (object)
                        + code (string, required) - kód varianty
                        + code_supplier (string, optional) - kód dodavatele
                        + active_yn (bool, optional) - zobrazit variantu na webu
                        + main_yn (bool, optional) - hlavní varianta
                        + ean (string, optional) - EAN
                        + stock (float, optional) - počet jednotek na skladě
                        + stock_increment (float, optional) - provede změnu počtu jednotek na skladě o hodnotu
                        + stock_position (string, optional) - pozice na skladě
                        + availability_id (int, optional) - ID dostupnosti
                        + availability (string, optional) - název dostupnosti. Neimportuje se u položek s nastavením [dostupnosti dle stavu zásob](https://upgates.cz/a/nastaveni-dostupnosti-dle-stavu-zasob). Pokud však v tomto případě stav zásob není definován (hodnota `stock` musí být prázdná nebo úplně chybět), dostupnost se importuje
                        + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
                        + image (object, optional) - obrázek varianty
                            + file_id (int, optional) - ID existujícího souboru, soubor musí být typu `image`
                            + url (string, optional) - URL adresa, obrázek se nestahuje hned, ale je stažen na pozadí
                        + prices (array, optional) - pole objektů s cenami
                            + (object)
                                + language (language, required)
                                + pricelists (array, optional) - pole objektů s ceníky
                                    + (object)
                                        + name (string, required) - název ceníku. Pokud je při importu prázdné, chápe se jako výchozí ceník
                                        + price_original (float, optional) - původní cena. Základní ceníková cena od které se odvozují další
                                        + product_discount (float, optional) - sleva na produkt v procentech
                                        + price_sale (float, optional) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                                + price_purchase (float, optional) - nákupní cena, interní údaj pro orientaci administrátora
                                + price_common (float, optional) - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech
                        + labels (array, optional)
                            + (object)
                                + label_id (int, optional) - ID štítku
                                + name (object, optional) - objekt s názvy štítků v jednotlivých jazycích (klíč každé položky v objektu je typu *language*)
                                + active_yn (bool, optional) - aktivní
                                + active_from (date, optional) - aktivní od data
                                + active_to (date, optional) - aktivní do data
                        + parameters (array, optional) - parametry varianty
                            + (object)
                                + id (int, optional) - ID parametru
                                + descriptions (array) - název parametru
                                    + (object)
                                        + language (language, required)
                                        + name (string, required)
                                + values (array, required) - hodnoty
                                    + (object)
                                        + id (int) + ID hodnoty
                                        + descriptions (array)
                                            + (object)
                                                + language (language, required)
                                                + value (string, required)
                        + metas (array, optional) - pole objektů s vlastnimi poli
                            + (object)
                                + key (string, optional) - klíč vlastního pole. Vlastní pole musí být v administraci založeno.
                                + value (string, optional) - hodnota vlastního pole. Použijte v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                                + values (array, optional) - pole hodnot vlastního pole podle jazykových mutací
                                    + (object)
                                        + language (language, optional) - jazyk hodnoty
                                        + value (string, optional) - hodnota
                + metas (array, optional) - pole objektů s vlastnimi poli
                    + (object)
                        + key (string, optional) - klíč vlastního pole. Vlastní pole musí být v administraci založeno.
                        + value (string, optional) - hodnota vlastního pole. Použijte v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array, optional) - pole hodnot vlastního pole podle jazykových mutací
                            + (object)
                                + language (language, optional) - jazyk hodnoty
                                + value (string, optional) - hodnota
        + variants (array, optional) - pole objektů s variantami (viz. varianty v produktu). Možno poslat i bez produktu, pouze jako seznam variant. Varianty se nezaloží, ale pouze aktualizují existující.

+ Response 200 (application/json)

    + Attributes
        + products (array) - pole objektů s produkty
            + (object)
                + product_id (int) - ID produktu
                + code (string) - kód produktu
                + product_url (string) - URL adresa, kde se nachází produkt
                + updated_yn (bool) - příznak, jestli se produkt aktualizoval
                + messages (ErrorMessage)
                + variants (array)
                    + (object)
                        + variant_id (int) - ID varianty
                        + code (string) - kód varianty
                        + updated_yn (bool) - příznak, jestli se varianta aktualizovala
                        + messages (ErrorMessage)

### Smazání produktů [DELETE/api/v2/products/{code}{?codes}]

+ Parameters
    + code (string) - kód produktu
    + codes (string) - kódy produktů oddělené středníkem `;` nebo jako pole

+ Response 200 (application/json)

    + Attributes
        + products (array) - pole objektů s produkty
            + (object)
                + code (string) - kód produktu
                + deleted_yn (bool) - příznak, jestli se produkt smazal
                + messages (ErrorMessage)

### Seznam produktů - kompletní [GET/api/v2/products{code}{?codes}{?product_id}{?product_ids}{?variant_codes}{?last_update_time_from}{?active_yn}{?archived_yn}{?can_add_to_basket_yn}{?exclude_from_search_yn}{?in_stock_yn}{?language}{?pricelist}{?page}]

+ Parameters
    + code (string, optional) - kód produktu
    + codes (string, optional) - kódy produktů oddělené středníkem `;`
    + product_id (string, optional) - ID produktu
    + product_ids (string, optional) - ID produktů oddělené středníkem `;`
    + variant_codes (string, optional) - kódy variant oddělené středníkem `;` (v případě použití tohoto parametru vrací produkt, který obsahuje požadovanou variantu)
    + last_update_time_from (date, optional) - vrátí produkty změněné od tohoto data
    + active_yn (bool, optional) - vrátí pouze aktivní nebo neaktivní produkty
    + archived_yn (bool, optional) - vrátí pouze archivované nebo nearchivované produkty
    + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
    + exclude_from_search_yn (bool, optional) - příznak vyřadit z vyhledávání
    + in_stock_yn (bool, optional) - vrátí pouze produkty skladem nebo produkty s ostatními dostupnostmi
    + language (language, optional) - jazyk. Vrací pouze produkty v aktivním jazyce a pouze s daty, které se vážou na jazyk (např. ceny a texty). Pokud není definováno, vrací produkty a data ve všech jazycích
    + pricelist (string, optional) - název ceníku. Vrátí produkty pouze s tímto ceníkem
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + products (array) - pole objektů s produkty
            + (object)
                + code (string, nullable) - kód produktu, páruje se podle existující hodnoty v databázi
                + code_supplier (string, nullable) - kód dodavatele
                + supplier (string, nullable) - dodavatel
                + ean (string, nullable) - EAN
                + product_id (int) - interní ID produktu
                + active_yn (bool) - zobrazit produkt na webu
                + archived_yn (bool) - archivovaný produkt
                + replacement_product_code (string, nullable) - kód náhradního produktu. Pouze pokud je produkt archivovaný
                + can_add_to_basket_yn (bool) - lze přidat do košíku
                + adult_yn (bool) - pouze pro dospělé
                + set_yn (bool) - produkt je sada
                + in_set_yn (bool) - produkt je v sadě
                + exclude_from_search_yn (bool) - příznak vyřadit z vyhledávání
                + descriptions (array) - pole objektů s texty
                    + (object)
                        + language (language)
                        + title (string) - název produktu
                        + short_description (string, nullable) - krátký popis, bez HTML formátování
                        + long_description (string, nullable) - dlouhý popis, může obsahovat formátování pomocí HTML značek
                        + url (string) - URL adresa produktu
                        + seo_title (string, nullable) - SEO titulek produktu
                        + seo_description (string, nullable) - META popisek stránky produktu
                        + seo_url (string, nullable) - vlastní koncovka URL adresy
                        + unit (string) - název jednotky v daném jazyce
                + manufacturer (string, nullable) - výrobce
                + stock (float) - počet jednotek na skladě
                + stock_position (string, nullable) - pozice na skladě
                + limit_orders (enum, optional) - omezení objednání
                    - 0 - vypnuto
                    - 1 - zapnuto
                    - sale - pouze pokud je produkt ve výprodeji
                    - null - dědí z nastavení eshopu
                + availability_id (int, nullable) - ID dostupnosti
                + availability (string, nullable) - název dostupnosti
                + availability_type (enum, nullable) - typ dostupnosti
                    - OnRequest - na dotaz
                    - NotAvailable - není skladem
                    - InStock - skladem
                    - Custom - vlastní
                + weight (int) - váha v gramech
                + shipment_group (string, nullable) - skupina doprav
                + images (array) - pole objektů s obrázky
                    + (object)
                        + file_id (int) - ID souboru
                        + url (string) - URL adresa obrázku
                        + main_yn (bool) - hlavní obrázek
                        + list_yn (bool) - seznamový obrázek
                        + position (int) - pozice obrázku
                        + titles (array) - pole objektů s popisky
                            + (object)
                            + language (language)
                            + title (string) - popisek obrázku
                + categories (array) - pole objektů s kategoriemi
                    + (object)
                        + category_id (int) - ID kategorie
                        + code (string, nullable) - kód kategorie
                        + main_yn (bool) - příznak hlavní kategorie. Pokud je `true`, je tato kategorie u tohoto produktu hlavní
                        + position (int) - pozice produktu v kategorii
                        + name (string) - pouze orientační název kategorie. Není zaručeno, z jakého jazyka se vezme
                + groups (array) - skupiny, do kterých je produkt zařazen
                + prices (array) - pole objektů s cenami
                    + (object)
                        + language (language)
                        + currency (currency)
                        + pricelists (array) - pole objektů s ceníky
                            + (object)
                                + name (string) - název ceníku. Pokud je při importu prázdné, chápe se jako výchozí ceník
                                + price_original (float) - původní cena. Základní ceníková cena, od které se odvozují další
                                + product_discount (float, nullable) - sleva na produkt v procentech
                                + product_discount_real (float) - reálná sleva na produkt použitá pro výpočet výsledné ceny, vypočítává se takto: 
                                hodnota slevy na produkt (product_discount) + sleva na výrobce + sleva na kategorii (bere se sleva z hlavní kategorie ve které je produkt zařazen). Výsledná hodnota slevy se omezí na hodnotu z nastavení Maximální procento slevy.
                                + price_sale (float, nullable) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                                + price_with_vat (float) - koncová cena s DPH
                                + price_without_vat (float) - koncová cena bez DPH
                        + price_purchase (float, nullable) - nákupní cena, interní údaj pro orientaci administrátora
                        + price_common (float) - běžná cena. Pro orientaci při nákupu, může to být např. cena v kamenných obchodech
                        + vat (float) - DPH použité k výpočtu cen v aktuálním objektu `price`
                        + recycling_fee (float, nullable) - recyklační poplatek
                + vats (object) - objekt s DPH v jednotlivých zemích (klíč každé položky v objektu je typu *country*)
                + variants (array) - pole objektů s variantami
                    + (object)
                        + code (string, nullable) - kód varianty
                        + code_supplier (string, nullable) - kód dodavatele
                        + ean (string, nullable) - EAN
                        + variant_id (int) - interní ID varianty
                        + active_yn (bool, nullable) - zobrazit variantu na webu
                        + main_yn (bool, optional) - hlavní varianta
                        + can_add_to_basket_yn (bool, nullable) - lze přidat do košíku
                        + stock (float, nullable) - počet jednotek na skladě
                        + stock_position (string, nullable) - pozice na skladě
                        + availability_id (int, nullable) - ID dostupnosti
                        + availability (string, nullable) - název dostupnosti
                        + availability_type (enum, nullable) - typ dostupnosti
                            - OnRequest - na dotaz
                            - NotAvailable - není skladem
                            - InStock - skladem
                            - Custom - vlastní
                        + weight (int, nullable) - váha v gramech
                        + image (string, nullable) - URL adresa obrázku varianty
                        + prices (array) - pole objektů s cenami
                            + (object)
                                + language (language)
                                + currency (currency)
                                + pricelists (array) - pole objektů s ceníky
                                    + (object)
                                        + name (string) - název ceníku
                                        + price_original (float) - původní cena. Základní ceníková cena, od které se odvozují další
                                        + product_discount (float, nullable) - sleva na produkt v procentech
                                        + product_discount_real (float) - reálná sleva na produkt, použitá pro výpočet výsledné ceny. Vypočítává se takto:
                                        hodnota slevy na produkt (product_discount) + sleva na výrobce + sleva na kategorii (bere se sleva z hlavní kategorie ve které je produkt zařazen). Výsledná hodnota slevy se omezí na hodnotu z nastavení Maximální procento slevy.
                                        + price_sale (float, nullable) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                                        + price_with_vat (float) - koncová cena s DPH
                                        + price_without_vat (float) - koncová cena bez DPH
                                + price_purchase (float, nullable) - nákupní cena, interní údaj pro orientaci administrátora
                                + price_common (float) - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech
                                + vat (float) - DPH použité k výpočtu cen v aktuálním objektu `price`
                        + metas (Metas)
                + metas (Metas)
                + creation_time (date) - čas vytvoření produktu
                + last_update_time (date) - čas poslední aktualizace produktu
                + admin_url (string) - URL do detailu produktu v administraci

### Seznam produktů - zjednodušený [GET/api/v2/products/{code}/simple/{?codes}{?product_id}{?product_ids}{?variant_codes}{?last_update_time_from}{?active_yn}{?archived_yn}{?can_add_to_basket_yn}{?exclude_from_search_yn}{?in_stock_yn}{?page}]

+ Parameters
    + code (string, optional) - kód produktu
    + codes (string, optional) - kódy produktů oddělené středníkem `;`
    + product_id (string, optional) - ID produktu
    + product_ids (string, optional) - ID produktů oddělené středníkem `;`
    + variant_codes (string, optional) - kódy variant oddělené středníkem `;` (v případě použití tohoto parametru vrací produkt, který obsahuje požadovanou variantu)
    + last_update_time_from (date, optional) - vrátí produkty změněné od tohoto data
    + active_yn (bool, optional) - vrátí pouze aktivní nebo neaktivní produkty
    + archived_yn (bool, optional) - vrátí pouze archivované nebo nearchivované produkty
    + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
    + exclude_from_search_yn (bool, optional) - příznak vyřadit z vyhledávání
    + in_stock_yn (bool, optional) - vrátí pouze produkty skladem nebo produkty s ostatními dostupnostmi
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + products (array) - pole objektů s produkty
            + (object)
                + code (string, nullable) - kód produktu, páruje se podle existující hodnoty v databázi
                + code_supplier (string, nullable) - kód dodavatele
                + supplier (string, nullable) - dodavatel
                + ean (string, nullable) - EAN
                + product_id (int) - interní ID produktu
                + active_yn (bool) - zobrazit produkt na webu
                + archived_yn (bool) - archivovaný produkt
                + replacement_product_code (string, nullable) - kód náhradního produktu, pouze pokud je produkt archivovaný
                + can_add_to_basket_yn (bool) - lze přidat do košíku
                + adult_yn (bool) - pouze pro dospělé
                + set_yn (bool) - produkt je sada
                + in_set_yn (bool) - produkt je v sadě
                + exclude_from_search_yn (bool) - příznak vyřadit z vyhledávání
                + manufacturer (string, nullable) - výrobce
                + stock (float, nullable) - počet jednotek na skladě
                + stock_position (string, nullable) - pozice na skladě
                + limit_orders (enum, nullable) - omezení objednání
                    - 0 - vypnuto
                    - 1 - zapnuto
                    - sale - pouze pokud je produkt ve výprodeji
                    - null - dědí z nastavení eshopu
                + availability_id (int, nullable) - ID dostupnosti
                + availability (string, nullable) - název dostupnosti
                + availability_type (enum, nullable) - typ dostupnosti
                    - OnRequest - na dotaz
                    - NotAvailable - není skladem
                    - InStock - skladem
                    - Custom - vlastní
                + weight (int, nullable) - váha v gramech
                + shipment_group (string, nullable) - skupina doprav
                + groups (array) - skupiny, do kterých je produkt zařazen
                + vats (object) - objekt s DPH v jednotlivých zemích (klíč každé položky v objektu je typu *country*), **pouze pokud je aktivní OSS**
                + variants (array) - pole objektů s variantami
                    + (object)
                        + code (string, nullable) - kód varianty
                        + code_supplier (string, nullable) - kód dodavatele
                        + ean (string, nullable) - EAN
                        + variant_id (int) - interní ID varianty
                        + active_yn (bool, nullable) - zobrazit variantu na webu
                        + main_yn (bool, optional) - hlavní varianta
                        + can_add_to_basket_yn (bool, nullable) - lze přidat do košíku
                        + stock (float, nullable) - počet jednotek na skladě
                        + stock_position (string, nullable) - pozice na skladě
                        + availability_id (int, nullable) - ID dostupnosti
                        + availability (string, nullable) - název dostupnosti
                        + availability_type (enum, nullable) - typ dostupnosti
                            - OnRequest - na dotaz
                            - NotAvailable - není skladem
                            - InStock - skladem
                            - Custom - vlastní
                        + weight (int, nullable) - váha v gramech
                        + image (string, nullable) - URL adresa obrázku varianty
                + creation_time (date) - čas vytvoření produktu
                + last_update_time (date) - čas poslední aktualizace produktu
                + admin_url (string) - URL do detailu produktu v administraci

## Ceny [/api/v2/products/prices/]

### Seznam produktů - ceny [GET/api/v2/products/{code}/prices/{?codes}{?product_id}{?product_ids}{?variant_codes}{?last_update_time_from}{?active_yn}{?archived_yn}{?can_add_to_basket_yn}{?exclude_from_search_yn}{?in_stock_yn}{?language}{?pricelist}{?page}]

+ Parameters
    + code (string, optional) - kód produktu
    + codes (string, optional) - kódy produktů oddělené středníkem `;`
    + product_id (string, optional) - ID produktu
    + product_ids (string, optional) - ID produktů oddělené středníkem `;`
    + variant_codes (string, optional) - kódy variant oddělené středníkem `;` (v případě použití tohoto parametru vrací produkt, který obsahuje požadovanou variantu)
    + last_update_time_from (date, optional) - vrátí produkty změněné od tohoto data
    + active_yn (bool, optional) - vrátí pouze aktivní nebo neaktivní produkty
    + archived_yn (bool, optional) - vrátí pouze archivované nebo nearchivované produkty
    + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
    + exclude_from_search_yn (bool, optional) - příznak vyřadit z vyhledávání
    + in_stock_yn (bool, optional) - vrátí pouze produkty skladem nebo produkty s ostatními dostupnostmi
    + language (language, optional) - jazyk. Vrací pouze produkty v aktivním jazyce a pouze s daty, které se vážou na jazyk (např. ceny a texty). Pokud není definováno, vrací produkty a data ve všech jazycích
    + pricelist (string, optional) - název ceníku, vrátí produkty pouze s tímto ceníkem
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + products (array) - pole objektů s produkty
            + (object)
                + code (string, nullable) - kód produktu, páruje se podle existující hodnoty v databázi
                + product_id (int) - interní ID produktu
                + action_currently_yn (bool) - přiznak produktu v akci
                + prices (array) - pole objektů s cenami
                    + (object)
                        + language (language)
                        + currency (currency)
                        + pricelists (array) - pole objektů s ceníky
                            + (object)
                                + name (string) - název ceníku. Pokud je při importu prázdné, chápe se jako výchozí ceník
                                + price_original (float) - původní cena. Základní ceníková cena, od které se odvozují další
                                + product_discount (float, nullable) - sleva na produkt v procentech
                                + product_discount_real (float) - reálná sleva na produkt použitá pro výpočet výsledné ceny, vypočítává se takto:
                                hodnota slevy na produkt (product_discount) + sleva na výrobce + sleva na kategorii (bere se sleva z hlavní kategorie ve které je produkt zařazen). Výsledná hodnota slevy se omezí na hodnotu z nastavení Maximální procento slevy.
                                + price_sale (float, nullable) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                                + price_with_vat (float) - koncová cena s DPH
                                + price_without_vat (float) - koncová cena bez DPH
                        + price_purchase (float, nullable) - nákupní cena, interní údaj pro orientaci administrátora
                        + price_common (float) - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech
                        + vat (float) - DPH použité k výpočtu cen v aktuálním objektu `price`
                        + recycling_fee (float, nullable) - recyklační poplatek
                + variants (array) - pole objektů s variantami
                    + (object)
                        + code (string, nullable) - kód varianty
                        + variant_id (int) - interní ID varianty
                        + action_currently_yn (bool) - přiznak varianty v akci
                        + prices (array) - pole objektů s cenami
                            + (object)
                                + language (language)
                                + currency (currency)
                                + pricelists (array) - pole objektů s ceníky
                                    + (object)
                                        + name (string) - název ceníku
                                        + price_original (float) - původní cena. Základní ceníková cena, od které se odvozují další
                                        + product_discount (float, nullable) - sleva na produkt v procentech
                                        + product_discount_real (float) - reálná sleva na produkt použitá pro výpočet výsledné ceny, vypočítává se takto:
                                        hodnota slevy na produkt (product_discount) + sleva na výrobce + sleva na kategorii (bere se sleva z hlavní kategorie ve které je produkt zařazen). Výsledná hodnota slevy se omezí na hodnotu z nastavení Maximální procento slevy.
                                        + price_sale (float, nullable) - akční cena. Exportuje se pouze tehdy, pokud je produkt v akci (štítek akce)
                                        + price_with_vat (float) - koncová cena s DPH
                                        + price_without_vat (float) - koncová cena bez DPH
                                + price_purchase (float, nullable) - nákupní cena, interní údaj pro orientaci administrátora
                                + price_common (float) - běžná cena, pro orientaci při nákupu. Může to být např. cena v kamenných obchodech
                                + vat (float) - DPH použité k výpočtu cen v aktuálním objektu `price`
                + admin_url (string) - URL do detailu produktu v administraci

## Parametry [/api/v2/products/parameters/]

### Seznam produktů - parametry [GET/api/v2/products/{code}/parameters/{?codes}{?product_id}{?product_ids}{?variant_codes}{?last_update_time_from}{?active_yn}{?archived_yn}{?can_add_to_basket_yn}{?exclude_from_search_yn}{?in_stock_yn}{?language}{?page}]

+ Parameters
    + code (string, optional) - kód produktu
    + codes (string, optional) - kódy produktů oddělené středníkem `;`
    + product_id (string, optional) - ID produktu
    + product_ids (string, optional) - ID produktů oddělené středníkem `;`
    + variant_codes (string, optional) - kódy variant oddělené středníkem `;` (v případě použití tohoto parametru vrací produkt, který obsahuje požadovanou variantu)
    + last_update_time_from (date, optional) - vrátí produkty změněné od tohoto data
    + active_yn (bool, optional) - vrátí pouze aktivní nebo neaktivní produkty
    + archived_yn (bool, optional) - vrátí pouze archivované nebo nearchivované produkty
    + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
    + exclude_from_search_yn (bool, optional) - příznak vyřadit z vyhledávání
    + in_stock_yn (bool, optional) - vrátí pouze produkty skladem nebo produkty s ostatními dostupnostmi
    + language (language, optional) - jazyk. Vrací pouze produkty v aktivním jazyce a pouze s daty, které se vážou na jazyk (např. ceny a texty). Pokud není definováno, vrací produkty a data ve všech jazycích
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + products (array) - pole objektů s produkty
            + (object)
                + code (string, nullable) - kód produktu, páruje se podle existující hodnoty v databázi
                + product_id (int) - interní ID produktu
                + parameters (ProductParameters)
                + parameters_new (array, optional) - parametry
                    + (object)
                        + id (int, optional) - ID parametru
                        + descriptions (array) - název parametru
                            + (object)
                                + language (language, required)
                                + name (string, required)
                        + values (array, required) - hodnoty
                            + (object)
                                + id (int) + ID hodnoty
                                + descriptions (array)
                                    + (object)
                                        + language (language, required)
                                        + value (string, required)
                + variants (array) - pole objektů s variantami
                    + (object)
                        + code (string, nullable) - kód varianty
                        + variant_id (int) - interní ID varianty
                        + parameters (ProductParameters)
                        + parameters_new (array, optional) - parametry
                            + (object)
                                + id (int, optional) - ID parametru
                                + descriptions (array) - název parametru
                                    + (object)
                                        + language (language, required)
                                        + name (string, required)
                                + values (array, required) - hodnoty
                                    + (object)
                                        + id (int) + ID hodnoty
                                        + descriptions (array)
                                            + (object)
                                                + language (language, required)
                                                + value (string, required)
                + admin_url (string) - URL do detailu produktu v administraci

## Štítky [/api/v2/products/labels/]

### Seznam produktů - štítky [GET/api/v2/products/{code}/labels/{?codes}{?product_id}{?product_ids}{?variant_codes}{?last_update_time_from}{?active_yn}{?archived_yn}{?can_add_to_basket_yn}{?exclude_from_search_yn}{?in_stock_yn}{?language}{?page}]

+ Parameters
    + code (string, optional) - kód produktu
    + codes (string, optional) - kódy produktů oddělené středníkem `;`
    + product_id (string, optional) - ID produktu
    + product_ids (string, optional) - ID produktů oddělené středníkem `;`
    + variant_codes (string, optional) - kódy variant oddělené středníkem `;` (v případě použití tohoto parametru vrací produkt, který obsahuje požadovanou variantu)
    + last_update_time_from (date, optional) - vrátí produkty změněné od tohoto data
    + active_yn (bool, optional) - vrátí pouze aktivní nebo neaktivní produkty
    + archived_yn (bool, optional) - vrátí pouze archivované nebo nearchivované produkty
    + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
    + exclude_from_search_yn (bool, optional) - příznak vyřadit z vyhledávání
    + in_stock_yn (bool, optional) - vrátí pouze produkty skladem nebo produkty s ostatními dostupnostmi
    + language (language, optional) - jazyk. Vrací pouze produkty v aktivní jazyce a pouze s daty, které se vážou na jazyk (např. ceny a texty). Pokud není definováno, vrací produkty a data ve všech jazycích
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + products (array) - pole objektů s produkty
            + (object)
                + code (string, nullable) - kód produktu, páruje se podle existující hodnoty v databázi
                + product_id (int) - interní ID produktu
                + labels (ProductLabels)
                + variants (array) - pole objektů s variantami
                    + (object)
                        + code (string, nullable) - kód varianty
                        + variant_id (int) - interní ID varianty
                        + labels (ProductLabels)
                + admin_url (string) - URL do detailu produktu v administraci

## Soubory [/api/v2/products/files/]

### Seznam produktů - soubory [GET/api/v2/products/{code}/files/{?codes}{?product_id}{?product_ids}{?variant_codes}{?last_update_time_from}{?active_yn}{?archived_yn}{?can_add_to_basket_yn}{?exclude_from_search_yn}{?in_stock_yn}{?language}{?with_files_yn}{?page}]

+ Parameters
    + code (string, optional) - kód produktu
    + codes (string, optional) - kódy produktů oddělené středníkem `;`
    + product_id (string, optional) - ID produktu
    + product_ids (string, optional) - ID produktů oddělené středníkem `;`
    + variant_codes (string, optional) - kódy variant oddělené středníkem `;` (v případě použití tohoto parametru vrací produkt, který obsahuje požadovanou variantu)
    + last_update_time_from (date, optional) - vrátí produkty změněné od tohoto data
    + active_yn (bool, optional) - vrátí pouze aktivní nebo neaktivní produkty
    + archived_yn (bool, optional) - vrátí pouze archivované nebo nearchivované produkty
    + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
    + exclude_from_search_yn (bool, optional) - příznak vyřadit z vyhledávání
    + in_stock_yn (bool, optional) - vrátí pouze produkty skladem nebo produkty s ostatními dostupnostmi
    + language (language, optional) - jazyk. Vrací pouze produkty v aktivní jazyce a pouze s daty, které se vážou na jazyk (např. ceny a texty). Pokud není definováno, vrací produkty a data ve všech jazycích
    + with_files_yn (bool, optional) - pokud je `TRUE`, vrátí pouze produkty se soubory
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + products (array) - pole objektů s produkty
            + (object)
                + code (string, nullable) - kód produktu
                + product_id (int) - interní ID produktu
                + files (array) - pole objektů se soubory
                    + (object)
                        + url (string) - URL adresa souboru
                        + position (int) - pozice souboru
                        + titles (array) - pole objektů s popisky
                            + (object)
                            + language (language)
                            + title (string) - popisek souboru
                + admin_url (string) - URL do detailu produktu v administraci

## Související [/api/v2/products/related/]

### Seznam produktů - související [GET/api/v2/products/{code}/related/{?codes}{?product_id}{?product_ids}{?variant_codes}{?last_update_time_from}{?active_yn}{?archived_yn}{?can_add_to_basket_yn}{?exclude_from_search_yn}{?in_stock_yn}{?page}]
Seznam produktů pouze s vazbami na související, alternativní, příslušenství, dárky a sady

+ Parameters
    + code (string, optional) - kód produktu
    + codes (string, optional) - kódy produktů oddělené středníkem `;`
    + product_id (string, optional) - ID produktu
    + product_ids (string, optional) - ID produktů oddělené středníkem `;`
    + variant_codes (string, optional) - kódy variant oddělené středníkem `;` (v případě použití tohoto parametru vrací produkt, který obsahuje požadovanou variantu)
    + last_update_time_from (date, optional) - vrátí produkty změněné od tohoto data
    + active_yn (bool, optional) - vrátí pouze aktivní nebo neaktivní produkty
    + archived_yn (bool, optional) - vrátí pouze archivované nebo nearchivované produkty
    + can_add_to_basket_yn (bool, optional) - lze přidat do košíku
    + exclude_from_search_yn (bool, optional) - příznak vyřadit z vyhledávání
    + in_stock_yn (bool, optional) - vrátí pouze produkty skladem nebo produkty s ostatními dostupnostmi
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + products (array) - pole objektů s produkty
            + (object)
                + code (string, nullable) - kód produktu, páruje se podle existující hodnoty v databázi
                + product_id (int) - interní ID produktu
                + related (array) - související produkty, pole kódů produktů
                + accessories (array) - příslušenství, pole kódů produktů
                + alternative (array) - alternativní produkty, pole kódů produktů
                + gifts (array) - dárky
                    + (object)
                        + code (string) - kód produktu nebo varianty
                        + type (enum) - typ varianty
                            - highest_stock_variant - varianta s nejvyšším skladem
                            - random_stock_variant - náhodná varianta
                            - variant - vybraná varianta
                + sets (array) - sady
                    + (object)
                        + code (string) - kód produktu nebo varianty
                        + quantity (float) - počet jednotek v sadě
                + admin_url (string) - URL do detailu produktu v administraci

## Obrázky [/api/v2/products/image]

### Přidání obrázku [POST/api/v2/products/{id}/image]
Poslání obsahu souboru přes **form-data**, parametry jsou:
- **file** (*file, required*) - obsah souboru
- **file_name** (*string, optional*) - název souboru

+ Parameters
    + id (string, optional) - ID produktu

+ Response 200 (application/json)

    + Attributes
        + file (object)
            + id (string) - ID souboru
            + name (string) - název
            + mimetype (string) - MIMETYPE
            + size (string) - velikost v bytech
            + type (enum) - typ
                - image - obrázek
                - file - soubor
                - video - video
            + url (string) - URL obrázku
        + inserted_yn (bool) - vytvořeno
        + messages (ErrorMessage) - chybová zpráva

## Varianty [/api/v2/products/variants]

### Smazání variant [DELETE/api/v2/products/variants{?codes}]

+ Parameters
    + codes (string) - kódy variant oddělené středníkem `;` nebo jako pole

+ Response 200 (application/json)

    + Attributes
        + variants (array) - pole objektů s variantami
            + (object)
                + code (string) - kód varianty
                + deleted_yn (bool) - příznak, jestli se varianta smazala
                + messages (ErrorMessage)

## Recenze a hodnocení [/api/v2/products/ratings-reviews]
Recenze a hodnocení jsou spojeny do jednoho záznamu.
Více informací na [Hodnocení a recenze](https://www.upgates.cz/a/hodnoceni-a-recenze)

### Vytvoření [POST]
Zákazník může jeden produkt hodnotit pouze jednou, tzn. že musí být vždy unikátní kombinace zákazníka - produktu. V případě, že vznikne duplicita, vrátí API chybovou hlášku.
V požadavku musí vždy být informace o hodnocení, produktu a zákazníkovi. Všechny ostatní informace jsou nepovinné.

Hodnocení a recenze přijaté přes API jsou:
- **automaticky schválené** bez ohledu na nastavení v administraci
- neřeší se věrnostní systém, tzn. po přijetí recenze nejsou připsány body

+ Request 200 (application/json)

    + Attributes
        + ratings_reviews (array, required) - pole objektů s recenzemi a hodnocením
            + (object)
                + product (object, required) - produkt
                    + code (string, required) - kód produktu
                + customer (object, required) - zákazník
                    + email (email, required) - email zákazníka
                    + customer_name (string) - jméno zákazníka, které se zobrazuje u recenze a hodnocení. Může jít i o nick. Pokud je prázdné, vezme se z účtu zákazníka
                + review (object) - recenze
                    + positives (string) - klady. HTML tagy budou odstraněny a text bude ořezán na délku 500 znaků
                    + negatives (string) - zápory. HTML tagy budou odstraněny a text bude ořezán na délku 500 znaků
                    + creation_time (date) - datum vytvoření recenze
                    + answer (object) - odpověď na recenzi
                        + user_name (string) - jméno uživatele, který odpovídal
                        + text (string) - text odpovědi
                        + creation_time (date) - datum vytvoření odpovědi
                + rating (object, required) - hodnocení
                    + score (int, required) - počet hvězdiček 1-5
                    + creation_time (date) - datum vytvoření recenze

+ Response 200 (application/json)

    + Attributes
        + ratings_reviews (array) - pole objektů s recenzemi a hodnocením
            + (object)
                + created_yn (bool) - příznak, jestli se položka vytvořil
                + messages (ErrorMessage)

### Seznam [GET/api/v2/products/ratings-reviews{?product_code}{?email}{?page}]

+ Parameters
    + product_code (string, optional) - kód produktu
    + email (string, optional) - email zákazníka
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + ratings_reviews (array) - pole objektů s recenzemi a hodnocením
            + (object)
                + rating_review_id (int) - ID
                + product (object) - produkt
                    + product_id (int) - ID produktu
                    + code (string, nullable) - kód produktu
                + customer (object) - zákazník
                    + email (int) - email zákazníka
                    + code (string) - kód zákazníka
                    + customer_name (string) - jméno zákazníka, které se zobrazuje u recenze a hodnocení. Může jít i o nick
                + review (object) - recenze
                    + positives (string) - klady
                    + negatives (string) - zápory
                    + creation_time (date) - datum vytvoření recenze
                    + answer (object) - odpověď na recenzi
                        + user_name (string) - jméno uživatele, který odpovídal
                        + text (string) - text odpovědi
                        + creation_time (date) - datum vytvoření odpovědi
                + rating (object) - hodnocení
                    + score (int) - počet hvězdiček 1-5
                    + creation_time (date) - datum vytvoření recenze
                + approved_yn (bool) - příznak, jestli je recenze a hodnocení schváleno
                + approved_time (date) - datum schválení

### Smazání [DELETE/api/v2/products/ratings-reviews{?rating_review_id}{?rating_review_ids}]

+ Parameters
    + rating_review_id (int) - ID hodnocení a recenze
    + rating_review_ids (string) - ID hodnocení a recenze oddělené středníkem `;` nebo jako pole

+ Response 200 (application/json)

    + Attributes
        + ratings_reviews (array) - pole objektů
            + (object)
                + rating_review_id (int) - kód varianty
                + deleted_yn (bool) - příznak, jestli se položka smazala
                + messages (ErrorMessage)


# Group Štítky

## Štítky [/api/v2/labels]
Pro práci se štítky lze využívat **[webhooky](https://www.upgates.cz/a/stitky)**.

Více o štítcích v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/akce-novinky-vyprodej-a-dalsi-stitky).

### Vytvoření [POST]

+ Request 200 (application/json)

    + Attributes
        + labels (array) - pole objektů se štítky
            + (object)
                + descriptions (array)
                    + (object)
                        + language_id (language)
                        + name (string) - název

+ Response 200 (application/json)

    + Attributes
        + labels (array) - pole objektů
            + (object)
                + label_id (int) - ID štítku
                + created_yn (bool) - příznak, jestli se položka vytvořila
                + messages (ErrorMessage)

### Seznam štítků [GET/api/v2/labels/{id}{?id}{?ids}{?page}{?type}]

+ Parameters
    + id (int, optional) - ID parametru
    + ids (string, optional) - ID parametru oddělené středníkem `;`
    + type (enum) - typ štítku
        - action - systémový štítek **akce**
        - new - systémový štítek **novinka**
        - sale - systémový štítek **výprodej**
        - custom - vlastní štítek
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + labels (array) - pole objektů se štítky
            + (object)
                + label_id (int) - ID štítku
                + type(enum) - typ štítku
                    - action - systémový štítek **akce**
                    - new - systémový štítek **novinka**
                    - sale - systémový štítek **výprodej**
                    - custom - vlastní štítek
                + color: #f9a03b (string, nullable) - barva štítku v HTML HEX formátu 
                + descriptions (array)
                    + (object)
                        + language_id (language)
                        + name
Seznam štítků je dostupný po jednotlivých stranách, výstup je omezený na 50 položek na stránku.

### Smazání [DELETE/api/v2/labels/{id}{?ids}]

+ Parameters
    + id (int, optional) - ID štítku
    + ids (string, optional) - ID štítků oddělené středníkem `;`

+ Response 200 (application/json)

    + Attributes
        + labels (array) - pole objektů
            + (object)
                + id (int) - ID štítku
                + deleted_yn (bool) - příznak, jestli se položka smazala
                + messages (ErrorMessage)


# Group Dostupnosti

## Dostupnosti [/api/v2/availabilities]
Více o dostupnostích v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/dostupnosti).

### Vytvoření [POST]
Název `descriptions` musí být vždy ve všech jazycích, ty které chybí se vezmou z výchozího jazyka, pokud není tak z prvního co je na řadě.

+ Request 200 (application/json)

    + Attributes
        + availabilities (array, required) - pole objektů s dostupnostmi
            + (object)
                + descriptions (array, required)
                    + (object)
                      + language (language, required) - jazyk
                      + name (string, required) - název

+ Response 200 (application/json)

    + Attributes
        + availabilities (array) - pole objektů s dostupnostmi
            + (object)
                + id (int) - ID dostupnosti
                + inserted_yn (bool) - příznak, jestli se položka vytvořila
                + messages (ErrorMessage)

### Aktualizace [PUT]

+ Request 200 (application/json)

    + Attributes
        + availabilities (array, required) - pole objektů s dostupnostmi
            + (object)
                + id (int, required) - ID dostupnosti
                + descriptions (array, required)
                    + (object)
                        + language (language, required) - jazyk
                        + name (string, required) - název

+ Response 200 (application/json)

    + Attributes
        + availabilities (array) - pole objektů s dostupnostmi
            + (object)
                + id (int) - ID dostupnosti
                + updated_yn (bool) - příznak, jestli se položka vytvořila
                + messages (ErrorMessage)

### Seznam dostupností [GET/api/v2/availabilities/{id}{?ids}{?page}]
Seznam dostupností je dostupný po jednotlivých stranách, výstup je omezený na 50 položek na stránku.

+ Parameters
    + id (string, optional) - ID dostupnosti
    + ids (array, optional) - ID dostupností
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + availabilities (array) - pole objektů s dostupnostmi
            + (object)
                + id (int) - ID dostupnosti
                + default_yn (bool) - výchozí
                + descriptions (array)
                    + (object)
                        + language (language)
                        + name (string)

### Smazání [DELETE/api/v2/products/availabilities{?id}{?ids}]

+ Parameters
    + id (int) - ID dostupnosti
    + ids (string) - ID dostupností oddělené středníkem `;` nebo jako pole

+ Response 200 (application/json)

    + Attributes
        + availabilities (array) - pole objektů s dostupnostmi
            + (object)
                + id (int) - ID dostupnosti
                + deleted_yn (bool) - příznak, jestli se položka smazala
                + messages (ErrorMessage)


# Group Výrobci

## Výrobci [/api/v2/manufacturers]
Více o výrobcích v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/vyrobci2).

### Seznam výrobců [GET/api/v2/manufacturers/{id}{?ids}{?page}]
Seznam výrobců je dostupný po jednotlivých stranách, výstup je omezený na 50 položek na stránku.

+ Parameters
    + id (string, optional) - ID výrobce
    + ids (array, optional) - ID výrobců
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + manufacturers (array) - pole objektů s výrobci
            + (object)
                + manufacturer_id (int) - ID výrobce
                + name (string) - název
                + discount (float, nullable) - sleva na výrobce v procentech
                + logo (object, nullable)
                    + id (int) - ID obrázku
                    + url (string) - URL obrázku

### Smazání [DELETE/api/v2/manufacturers/{?id}{?ids}]

+ Parameters
    + id (int) - ID výrobce
    + ids (string) - ID výrobců oddělené středníkem `;` nebo jako pole

+ Response 200 (application/json)

    + Attributes
        + manufacturers (array) - pole objektů s výrobci
            + (object)
                + manufacturer_id (int) - ID výrobce
                + deleted_yn (bool) - příznak, jestli se položka smazala
                + messages (ErrorMessage)


# Group Parametry

## Parametry [/api/v2/parameters]
Více o produktech v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/princip-a-zobrazeni-parametru).
Názvy parametrů a hodnot parametrů a musí být vždy ve všech jazycích, ty které chybí se vezmou z výchozího jazyka, pokud není tak z prvního co je na řadě.

### Vytvoření [POST]

+ Request 200 (application/json)

    + Attributes
        + parameters (array) - pole objektů s parametry
            + (object)
                + descriptions (array)
                    + (object)
                        + language (language)
                        + name (string) - název
                + values (array) - hodnoty
                    + (object)
                        + descriptions (array)
                            + (object)
                                + language (language)
                                + value (string) - hodnota
                        + position (int) - pozice
                + position (int) - pozice
                + display_type (enum) - pozice, hodnoty:
                    - select - standardní zobrazení (výchozí)
                    - listing - zobrazení s obrázky (není možné nastavit `display_in_filters_as_slider_yn` = `TRUE`)
                    - tile - zobrazení textově v dlaždici
                + display_in_product_list_yn (bool) - zobrazit v seznamu produktů
                + display_in_product_detail_yn (bool) - zobrazit v detailu produktu
                + display_in_filters_as_slider_yn (bool) - zobrazit ve filtrech jako slider

+ Response 200 (application/json)

    + Attributes
        + parameters (array) - pole objektů
            + (object)
                + id (int) - ID parametru
                + created_yn (bool) - příznak, jestli se položka vytvořila
                + messages (ErrorMessage)

### Aktualizace [PUT]

+ Request 200 (application/json)

    + Attributes
        + parameters (array) - pole objektů s parametry
            + (object)
                + id (int, required) - ID parametru
                + descriptions (array)
                    + (object)
                        + language (language)
                        + name (string) - název
                + values (array) - hodnoty
                    + (object)
                        + id (int) - ID hodnoty parametru
                        + descriptions (array)
                            + (object)
                                + language (language)
                                + value (string) - hodnota
                        + position (int) - pozice
                + position (int) - pozice
                + display_type (enum) - pozice, hodnoty:
                    - select - standardní zobrazení (výchozí)
                    - listing - zobrazení s obrázky (není možné nastavit `display_in_filters_as_slider_yn` = `TRUE`)
                    - tile - zobrazení textově v dlaždici
                + display_in_product_list_yn (bool) - zobrazit v seznamu produktů
                + display_in_product_detail_yn (bool) - zobrazit v detailu produktu
                + display_in_filters_as_slider_yn (bool) - zobrazit ve filtrech jako slider

+ Response 200 (application/json)

    + Attributes
        + parameters (array) - pole objektů
            + (object)
                + id (int) - ID parametru
                + created_yn (bool) - příznak, jestli se položka vytvořila
                + messages (ErrorMessage)

### Seznam [GET/api/v2/parameters/{id}{?ids}{?page}]

+ Parameters
    + id (int, optional) - ID parametru
    + ids (string, optional) - ID parametru oddělené středníkem `;`
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + parameters (array) - pole objektů s parametry
            + (object)
                + id (int) - ID parametru
                + descriptions (array)
                    + (object)
                        + language (language)
                        + name (string) - název
                + values (array) - hodnoty
                    + (object)
                        + id (int) - ID hodnoty parametru
                        + descriptions (array)
                            + (object)
                                + language (language)
                                + value (string) - hodnota
                        + image (object) - obrázek
                            + id (int) - ID souboru
                            + url (string) - URL adresa
                        + position (int) - pozice
                + position (int) - pozice
                + display_type (enum) - pozice, hodnoty:
                    - select - standardní zobrazení (výchozí)
                    - listing - zobrazení s obrázky
                    - tile - zobrazení textově v dlaždici
                + display_in_product_list_yn (bool) - zobrazit v seznamu produktů
                + display_in_product_detail_yn (bool) - zobrazit v detailu produktu
                + display_in_filters_as_slider_yn (bool) - zobrazit ve filtrech jako slider

### Smazání [DELETE/api/v2/parameters/{id}{?ids}]

+ Parameters
    + id (int, optional) - ID parametru
    + ids (string, optional) - ID parametru oddělené středníkem `;`

+ Response 200 (application/json)

    + Attributes
        + parameters (array) - pole objektů
            + (object)
                + id (int) - ID parametru
                + deleted_yn (bool) - příznak, jestli se položka smazala
                + messages (ErrorMessage)

## Hodnoty parametrů [/api/v2/parameters/values]

### Smazání hodnoty [DELETE/api/v2/parameters/values{?ids}]

+ Parameters
    + ids (string, optional) - ID hodnoty parametru oddělené středníkem `;`

+ Response 200 (application/json)

    + Attributes
        + parameters (array) - pole objektů
            + (object)
                + id (int) - ID hodnoty
                + deleted_yn (bool) - příznak, jestli se položka smazala
                + messages (ErrorMessage)


# Group Kategorie
Unikátním identifikátorem kategorie je kód (`code`) nebo ID (`category_id`).

Pro práci s kategoriemi lze využívat **[webhooky](https://www.upgates.cz/a/kategorie)**.

Více o kategoriích v Upgates najdete [zde](https://www.upgates.cz/a/princip-a-zobrazeni-kategorii).

## Kategorie [/api/v2/categories]

### Vytvoření kategorií [POST]

Při vytváření stromu kategorií je potřeba poslat kategorie ve správném pořadí, tzn. napřed rodičovské kategorie a potom potomky.

+ Request
    + Attributes
        + categories (array) - pole objektů s kategoriemi
            + (object)
                + code (string, nullable) - kód kategorie
                + parent_code (string, nullable) - kód nadřazené kategorie
                + parent_id (int, nullable) - ID nadřazené kategorie
                + position (int) - pozice v nadřazené kategorii
                + active_yn (bool) - zobrazit kategorii na webu
                + type (enum) - typ kategorie
                    - homepage - odkaz na hlavní stránku
                    - news - odkaz na aktuality
                    - individual - odkaz na samostatnou stránku
                    - url - externí odkaz
                    - site - stránka
                    - siteWithProducts - stránka s produkty
                    - linkCategory - odkaz na kategorii
                    - advisor - odkaz na rádce
                + type_of_items (enum) - Typ položek
                    - withoutSubcategories - bez podkategorií (výchozí, v kategorii budou ručně vložené produkty)
                    - label - štítek (v kategorii budou produkty, které mají aktivní určený štítek)
                    - manufacturer - výrobce (v kategorii budou produkty, které mají určeného výrobce)
                + target_category_id (int, nullable) - ID kategorie na kterou tato kategorie odkzuje. Bere se v úvahu pouze pokud má kategorie typ položek `linkCategory`
                + manufacturer (string, nullable) - název výrobce. Bere se v úvahu pouze pokud má kategorie typ položek `manufacturer`
                + manufacturer_id (int, nullable) - ID výrobce. Bere se v úvahu pouze pokud má kategorie typ položek `manufacturer`
                + label (string, nullable) - název štítku. Bere se v úvahu pouze pokud má kategorie typ položek `label`
                + label_id (int, nullable) - ID štítku. Bere se v úvahu pouze pokud má kategorie typ položek `label`
                + show_in_menu_yn (bool) - zobrazit kategorii v menu
                + descriptions (array) - pole objektů s texty
                    + (object)
                        + language (language)
                        + active_yn (bool) - aktivní v jazykové mutaci, výchozí je TRUE. Použitelné pouze pro deaktivaci jazykové mutace (skrytí kategorie v jazykove mutaci)
                        + name - název kategorie
                        + name_h1 (string, nullable) - nadpis stránky v kategorii
                        + description_text (string, nullable) - text stránky
                        + link_url (string, nullable) - URL adresa, na kterou bude vést kategorie. Bere se v úvahu pouze pokud je v tagu `type` hodnota `linkCategory`.
                        + seo_title (string, nullable) - SEO titulek
                        + seo_description (string, nullable) - META popisek stránky kategorie
                        + seo_url (string, nullable) - vlastní koncovka URL adresy
                + images (array) - pole objektů s cenami
                    + (object)
                        + file_id (int) - ID souboru
                        + url (string) - URL adresa obrázku
                        + main_yn (bool) - hlavní obrázek
                        + list_yn (bool) - seznamový obrázek
                        + position (int) - pozice obrázku
                + metas (array) - pole objektů s vlastními poli
                    + (object)
                        + key (string) - klíč vlastního pole
                        + type (string) - typ vlastního pole (hodnoty mohou být: radio, checkbox, input, date, email, number, select, multiselect, textarea, formatted)
                        + value (string) - hodnota vlastního pole v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array) - pole objektů s hodnotami v případě, kdy není hodnota vlastního pole společná pro všechny jazyky
                            + (object)
                                + language (language)
                                + value (string) - hodnota

+ Response 200 (application/json)

    + Attributes
        + categories (array) - pole objektů s kategoriemi
            + (object)
                + code (string) - kód kategorie
                + category_id (int) - ID kategorie
                + inserted_yn (bool) - příznak, jestli se kategorie založila
                + messages (ErrorMessage)

### Aktualizace kategorií [PUT]

Kategorie párují podle kódu (`code`) nebo ID (`category_id`). Pro správnou aktualizaci je potřeba poslat jeden z těchto údajů.

Systémové kategorie které mají `"parent_id": NULL` nelze aktualizovat!

+ Request
    + Attributes
        + categories (array) - pole objektů s kategoriemi
            + (object)
                + code (string, nullable) - kód kategorie
                + category_id (int) - ID kategorie
                + parent_code (string, nullable) - kód nadřazené kategorie
                + parent_id (int, nullable) - ID nadřazené kategorie
                + position (int) - pozice v nadřazené kategorii
                + active_yn (bool) - zobrazit kategorii na webu
                + type (enum) - typ kategorie
                    - homepage - odkaz na hlavní stránku
                    - news - odkaz na aktuality
                    - individual - odkaz na samostatnou stránku
                    - url - externí odkaz
                    - site - stránka
                    - siteWithProducts - stránka s produkty
                    - linkCategory - odkaz na kategorii
                    - advisor - odkaz na rádce
                + type_of_items (enum) - Typ položek
                    - withoutSubcategories - bez podkategorií (výchozí, v kategorii budou ručně vložené produkty)
                    - label - štítek (v kategorii budou produkty, které mají aktivní určený štítek)
                    - manufacturer - výrobce (v kategorii budou produkty, které mají určeného výrobce)
                + target_category_id (int, nullable) - ID kategorie na kterou tato kategorie odkzuje. Bere se v úvahu pouze pokud má kategorie typ položek `linkCategory`
                + manufacturer (string, nullable) - název výrobce. Bere se v úvahu pouze pokud má kategorie typ položek `manufacturer`
                + manufacturer_id (int, nullable) - ID výrobce. Bere se v úvahu pouze pokud má kategorie typ položek `manufacturer`
                + label (string, nullable) - název štítku. Bere se v úvahu pouze pokud má kategorie typ položek `label`
                + label_id (int, nullable) - ID štítku. Bere se v úvahu pouze pokud má kategorie typ položek `label`
                + show_in_menu_yn (bool) - zobrazit kategorii v menu
                + descriptions (array) - pole objektů s texty
                    + (object)
                        + language (language)
                        + active_yn (bool) - aktivní v jazykové mutaci, výchozí je TRUE. Použitelné pouze pro deaktivaci jazykové mutace (skrytí kategorie v jazykove mutaci)
                        + name - název kategorie
                        + name_h1 (string, nullable) - nadpis stránky v kategorii
                        + description_text (string, nullable) - text stránky
                        + link_url (string, nullable) - URL adresa, na kterou bude vést kategorie. Bere se v úvahu pouze pokud je v tagu `type` hodnota `linkCategory`.
                        + seo_title (string, nullable) - SEO titulek
                        + seo_description (string, nullable) - META popisek stránky kategorie
                        + seo_url (string, nullable) - vlastní koncovka URL adresy
                + images (array) - pole objektů s cenami
                    + (object)
                        + file_id (int) - ID souboru
                        + url (string) - URL adresa obrázku
                        + main_yn (bool) - hlavní obrázek
                        + list_yn (bool) - seznamový obrázek
                        + position (int) - pozice obrázku
                + metas (array) - pole objektů s vlastními poli
                    + (object)
                        + key (string) - klíč vlastního pole
                        + type (string) - typ vlastního pole (hodnoty mohou být: radio, checkbox, input, date, email, number, select, multiselect, textarea, formatted)
                        + value (string) - hodnota vlastního pole v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array) - pole objektů s hodnotami v případě, kdy není hodnota vlastního pole společná pro všechny jazyky
                            + (object)
                                + language (language)
                                + value (string) - hodnota

+ Response 200 (application/json)

    + Attributes
        + categories (array) - pole objektů s kategoriemi
            + (object)
                + code (string) - kód kategorie
                + category_id (int) - ID kategorie
                + updated_yn (bool) - příznak, jestli se kategorie aktualizovala
                + messages (ErrorMessage)

### Seznam kategorií [GET/api/v2/categories{?creation_time_from}{?last_update_time_from}{?code}{?codes}{?category_id}{?ids}{?parent_id}{?active_yn}{?language}{?page}]
Seznam kategorií je dostupný po jednotlivých stranách, výstup je omezený na 100 položek na stránku.
Seznam kategorií je seřazen podle rodiče a podle pozice, tzn. že první jsou rodičovské kategorie a potom potomci.

+ Parameters
    + creation_time_from (date, optional) - pouze kategorie vytvořené od data
    + last_update_time_from (date, optional) - pouze kategorie, u kterých došlo ke změně od data
    + code (string, optional) - kód kategorie
    + codes (string, optional) - kódy kategorií oddělené středníkem `;`
    + category_id (int, optional) - ID kategorie
    + ids (string, optional) - ID kategorií oddělené středníkem `;`
    + parent_id (int, optional) - ID nadřazené kategorie
    + active_yn (bool, optional) - aktivní / neaktivní
    + language (language, optional) - jazyk kategorie
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + categories (array) - pole objektů s kategoriemi
            + (object)
                + code (string, nullable) - kód kategorie
                + category_id (int) - ID kategorie
                + parent_code (string, nullable) - kód nadřazené kategorie, pokud je NULL nelze použít při zařazování produktů
                + parent_id (int, nullable) - ID nadřazené kategorie
                + position (int) - pozice v nadřazené kategorii
                + active_yn (bool) - zobrazit kategorii na webu
                + type (enum) - typ kategorie
                    - homepage - odkaz na hlavní stránku
                    - news - odkaz na aktuality
                    - individual - odkaz na samostatnou stránku
                    - url - externí odkaz
                    - site - stránka
                    - siteWithProducts - stránka s produkty
                    - linkCategory - odkaz na kategorii
                    - advisor - odkaz na rádce
                    - manufacturers - stránka s výrobci
                    - contact - stránka s kontakty
                    - why-us - odkaz na výhody obchodu
                    - contactMenu - kontaktní menu (systémová kategorie)
                + type_of_items (enum) - Typ položek
                    - withoutSubcategories - bez podkategorií (výchozí, v kategorii budou ručně vložené produkty)
                    - label - štítek (v kategorii budou produkty, které mají aktivní určený štítek)
                    - manufacturer - výrobce (v kategorii budou produkty, které mají určeného výrobce)
                + target_category_id (int, nullable) - ID kategorie na kterou tato kategorie odkzuje. Bere se v úvahu pouze pokud má kategorie typ položek `linkCategory`
                + manufacturer (string, nullable) - název výrobce. Bere se v úvahu pouze pokud je v tagu `type_of_items` hodnota `manufacturer`
                + label (string, nullable) - název štítku. Bere se v úvahu pouze pokud je v tagu `type_of_items` hodnota `label`
                + show_in_menu_yn (bool) - zobrazit kategorii v menu
                + descriptions (array) - pole objektů s texty
                    + (object)
                        + language (language)
                        + name - název kategorie
                        + name_h1 (string, nullable) - nadpis stránky v kategorii
                        + description_text (string, nullable) - text stránky
                        + url (string) - url kategorie
                        + link_url (string, nullable) - URL adresa, na kterou bude vést kategorie. Bere se v úvahu pouze pokud je v tagu `type` hodnota `linkCategory`.
                + images (array) - pole objektů s cenami
                    + (object)
                        + file_id (int) - ID souboru
                        + url (string) - URL adresa obrázku
                        + main_yn (bool) - hlavní obrázek
                        + list_yn (bool) - seznamový obrázek
                        + position (int) - pozice obrázku
                        + titles (array) - pole objektů s popisky
                            + (object)
                                + language (language)
                                + title (string) - popisek obrázku
                + metas (array) - pole objektů s vlastními poli
                    + (object)
                        + key (string) - klíč vlastního pole
                        + type (string) - typ vlastního pole (hodnoty mohou být: radio, checkbox, input, date, email, number, select, multiselect, textarea, formatted)
                        + value (string) - hodnota vlastního pole v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array) - pole objektů s hodnotami v případě, kdy není hodnota vlastního pole společná pro všechny jazyky
                            + (object)
                                + language (language)
                                + value (string) - hodnota
                + creation_time (date) - datum a čas vytvoření
                + last_update_time (date) - datum a čas poslední změny
                + admin_url (string) - URL do detailu kategorie v administraci

### Smazání kategorií [DELETE/api/v2/categories{?id}{?ids}{?code}]

POZOR - při zmazání kategorií se smažou i všichni její potomci (podkategorie).
Nelze mazat systémové kategorie nejvyšší úrovně, ty které mají `parent_id` = `NULL`

+ Parameters
    + id (int, optional) - ID kategorie
    + ids (array, optional) - pole ID kategorií
    + code (string, optional) - kód kategorie

+ Response 200 (application/json)

    + Attributes
        + categories (array) - pole objektů se kategoriemi
            + (object)
                + category_id (int) - ID kategorie 
                + code (string) - kód kategorie
                + deleted_yn (bool) - příznak, jestli se kategorie smazala
                + messages (ErrorMessage)

# Group Zákazníci
Unikátním identifikátorem zákazníků je email (`email`).

Pro práci se zákazníky lze využívat **[webhooky](https://www.upgates.cz/a/zakaznici)**.

Více o zákaznících v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/seznamy-zakazniku).

## Zákazníci [/api/v2/customers]

### Vytvoření zákazníků [POST]

+ Request
    + Attributes
        + customers (array) - pole objektů se zákazníky
            + (object)
                + type (enum, required) - typ
                    - contact - kontakt (neregistrovaný zákazník)
                    - customer - zákazník (registrovaný zákazník)
                    - company - firma (registrovaný zákazník, který má navíc firemní údaje)
                + degree (string) - titul
                + firstname (string) - křestní jméno
                + surname (string) - příjmení
                + nickname (string) - přezdívka
                + code (string) - kód zákazníka
                + language (language, required) - jazyk zákazníka
                + newsletter_accept (enum) - akceptuje zákazník newsletter
                    - notset - nenastaveno
                    - no - ne
                    - yes - ano
                    - excluded - vyloučený zákazník. Dle nastavení zákazník neotevřel určitý počet newsletterů
                + pricelist (string) - ceník
                + base_turnover (float) - výchozí hodnota obratu
                + note (string) - poznámka
                + company (object) - firemní údaje
                    + name (string) - název firmy
                    + company_number (string) - IČO
                    + vat_number (string) - DIČ
                    + vat_payer_yn (bool) - plátce DPH
                + communication (object) - komunikace
                    + phone (string) - telefon
                    + fax (string) - FAX
                    + im (string) - instant messaging
                    + salutation (string) - oslovení
                    + declension (string) - skloňování
                + login (object, required) - přihlašovací údaje
                    + active_yn (bool) - aktivní / neaktivní
                    + blocked_yn (bool) - blokovaný / neblokovaný
                    + email (string, required) - email
                    + password (string) - heslo, pokud není specifikováno použije se náhodné
                + groups (array) - skupiny, do kterých je zákazník zařazený
                    + (object)
                        + id (int) - ID skupiny
                + addresses (object) - adresy
                    + billing (object) - fakturační adresa
                        + street (string) - ulice
                        + city (string) - město
                        + state (string) - kraj
                        + zip_code (string) - PSČ
                        + country_id (country)
                    + postal (array) - doručovací adresy
                        + (object)
                            + company_name (string) - název firmy
                            + firstname (string) - křestní jméno
                            + surname (string) - příjmení
                            + street (string) - ulice
                            + city (string) - město
                            + state (string) - kraj
                            + zip_code (string) - PSČ
                            + country_id (country)
                + metas (array) - pole objektů s vlastními poli
                    + (object)
                        + key (string) - klíč vlastního pole
                    + value (string) - hodnota vlastního pole

+ Response 200 (application/json)

    + Attributes
        + customers (array) - pole objektů se zákazníky
            + (object)
                + email (string) - email zákazníka
                + inserted_yn (bool) - příznak, jestli se zákazník založil
                + messages (ErrorMessage)

### Aktualizace zákazníků [PUT]

+ Request
    + Attributes
        + customers (array) - pole objektů se zákazníky
            + (object)
                + type (enum) - typ
                    - contact - kontakt (neregistrovaný zákazník)
                    - customer - zákazník (registrovaný zákazník)
                    - company - firma (registrovaný zákazník, který má navíc firemní údaje)
                + degree (string) - titul
                + firstname (string) - křestní jméno
                + surname (string) - příjmení
                + nickname (string) - přezdívka
                + code (string) - kód zákazníka
                + language (language)
                + newsletter_accept (enum) - akceptuje zákazník newsletter
                    - notset - nenastaveno
                    - no - ne
                    - yes - ano
                    - excluded - vyloučený zákazník. Dle nastavení zákazník neotevřel určitý počet newsletterů
                + pricelist (string) - ceník
                + base_turnover (float) - výchozí hodnota obrazu
                + note (string) - poznámka
                + company (object) - firemní údaje
                    + name (string) - název firmy
                    + company_number (string) - IČO
                    + vat_number (string) - DIČ
                    + vat_payer_yn (bool) - plátce DPH
                + communication (object) - komunikace
                    + phone (string) - telefon
                    + fax (string) - FAX
                    + im (string) - instant messaging
                    + salutation (string) - oslovení
                    + declension (string) - skloňování
                + login (object) - přihlašovací údaje
                    + active_yn (bool) - aktivní / neaktivní
                    + blocked_yn (bool) - blokovaný / neblokovaný
                    + email (string) - email
                    + password (string) - heslo
                + groups (array) - skupiny, do kterých je zákazník zařazený
                    + (object)
                        + id (int) - ID skupiny
                + addresses (object) - adresy
                    + billing (object) - fakturační adresa
                        + street (string) - ulice
                        + city (string) - město
                        + state (string) - kraj
                        + zip_code (string) - PSČ
                        + country_id (country)
                    + postal (array) - doručovací adresy
                        + (object)
                            + company_name (string) - název firmy
                            + firstname (string) - křestní jméno
                            + surname (string) - příjmení
                            + street (string) - ulice
                            + city (string) - město
                            + state (string) - kraj
                            + zip_code (string) - PSČ
                            + country_id (country)
                + metas (array) - pole objektů s vlastními poli
                    + (object)
                        + key (string) - klíč vlastního pole
                    + value (string) - hodnota vlastního pole

+ Response 200 (application/json)

    + Attributes
        + customers (array) - pole objektů se zákazníky
            + (object)
                + email (string) - email zákazníka
                + updated_yn (bool) - příznak, jestli se zákazník aktualizoval
                + messages (ErrorMessage)

### Seznam zákazníků [GET/api/v2/customers{?creation_time_from}{?last_update_time_from}{?code}{?customer_id}{?ids}{?active_yn}{?blocked_yn}{?language}{?pricelist}{?email}{?phone}{?company_name}{?company_number}{?company_vat_number}{?page}{?newsletter_accept}]
Seznam zákazníků je dostupný po jednotlivých stranách, výstup je omezený na 100 položek na stránku.

+ Parameters
    + creation_time_from (date, optional) - pouze zákazníci vytvoření od data
    + last_update_time_from (date, optional) - pouze zákazníci, u kterých došlo ke změně od data
    + code (string, optional) - kód zákazníka
    + customer_id (int, optional) - ID zákazníka
    + ids (array, optional) - ID zákazníků oddělené středníkem ;
    + active_yn (bool, optional) - aktivní / neaktivní
    + blocked_yn (bool, optional) - blokovaní / neblokovaní
    + language (language, optional) - jazyk zákazníka
    + pricelist (string, optional) - ceník
    + email (string, optional) - email
    + phone (string, optional) - telefon
    + company_name (string, optional) - název firmy
    + company_number (string, optional) - DIČ
    + company_vat_number (string, optional) - IČO
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1
    + newsletter_accept (enum) - akceptuje zákazník newsletter
        - notset - nenastaveno
        - no - ne
        - yes - ano
        - excluded - vyloučený zákazník. Dle nastavení zákazník neotevřel určitý počet newsletterů

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + customers (array) - pole objektů se zákazníky
            + (object)
                + customer_id (int) - ID zákazníka
                + type (enum) - typ
                    - contact - kontakt (neregistrovaný zákazník)
                    - customer - zákazník (registrovaný zákazník)
                    - company - firma (registrovaný zákazník, který má navíc firemní údaje)
                + degree (string, nullable) - titul
                + firstname (string, nullable) - křestní jméno
                + surname (string, nullable) - příjmení
                + nickname (string, nullable) - přezdívka
                + code (string, nullable) - kód zákazníka
                + language (language)
                + newsletter_yn (bool) - chce / nechce dostávat newsletter
                + newsletter_accept (enum) - akceptuje zákazník newsletter
                    - notset - nenastaveno
                    - no - ne
                    - yes - ano
                    - excluded - vyloučený zákazník. Dle nastavení zákazník neotevřel určitý počet newsletterů
                + pricelist (string) - ceník
                + base_turnover (float) - výchozí hodnota obrazu
                + turnover (string) - obrat
                + turnover_currency (currency) - měna obratu
                + company (object, nullable) - firemní údaje
                    + name (string, nullable) - název firmy
                    + company_number (string, nullable) - IČO
                    + vat_number (string, nullable) - DIČ
                    + vat_payer_yn (bool) - plátce DPH
                + communication (object) - komunikace
                    + phone (string, nullable) - telefon
                    + fax (string, nullable) - FAX
                    + im (string, nullable) - instant messaging
                    + salutation (string, nullable) - oslovení
                    + declension (string, nullable) - skloňování
                + login (object) - přihlašovací údaje
                    + active_yn (bool) - aktivní / neaktivní
                    + blocked_yn (bool) - blokovaný / neblokovaný
                    + email (string) - email
                + groups (object) - skupiny, do kterých je zákazník zařazený. Klíč pole je ID skupiny, hodnota je název skupiny.
                + note (string, nullable) - poznámka
                + addresses (object) - adresy
                    + billing (object) - fakturační adresa
                        + street (string, nullable) - ulice
                        + city (string, nullable) - město
                        + state (string, nullable) - kraj
                        + zip_code (string, nullable) - PSČ
                        + country_id (country, nullable) - země
                    + postal (array) - pole objektů s doručovacímy adresami
                        + (object)
                            + company_name (string, nullable) - název firmy
                            + firstname (string, nullable) - křestní jméno
                            + surname (string, nullable) - příjmení
                            + street (string, nullable) - ulice
                            + city (string, nullable) - město
                            + state (string, nullable) - kraj
                            + zip_code (string, nullable) - PSČ
                            + country_id (country)
                + metas (array) - pole objektů s vlastními poli zákazníků
                    + (object)
                        + key (string) - klíč vlastního pole
                        + type (string) - typ vlastního pole (hodnoty mohou být: radio, checkbox, input, date, email, number, select, multiselect, textarea, formatted)
                        + value (string) - hodnota vlastního pole v případě, kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array) - pole objektů s hodnotami v případě, kdy není hodnota vlastního pole společná pro všechny jazyky
                            + (object)
                                + language (language)
                                + value (string) - hodnota
                + creation_time (date) - datum a čas vytvoření
                + last_update_time (date) - datum a čas poslední změny
                + admin_url (string) - URL do detailu zákazníka v administraci

### Smazání zákazníků [DELETE/api/v2/customers{?id}{?ids}{?email}]

+ Parameters
    + id (int, optional) - ID zákazníka
    + ids (array, optional) - pole ID zákazníků
    + email (string, optional) - email

+ Response 200 (application/json)

    + Attributes
        + customers (array) - pole objektů se zákazníky
            + (object)
                + customer_id (int) - ID zákazníka 
                + email (string) - email
                + deleted_yn (bool) - příznak, jestli se zákazník smazal
                + messages (ErrorMessage)

## Seznam souhlasů [/api/v2/customers/{customer_id}/agreements{?email}{?only_valid_yn}{?status}{?agreement_id}]
Více o souhlacech a GDPR v Upgates najdete [zde](https://www.upgates.cz/a/gdpr-souhlasy).

### Seznam souhlasů [GET/api/v2/customers/{customer_id}/agreements{?email}{?only_valid_yn}{?status}{?agreement_id}]

+ Parameters
    + customer_id (int, optional) - ID zákazníka, povinný parametr
    + email (email, optional) - email zákazníka
    + only_valid_yn (bool, optional) - vrátí pouze platné souhlasy
    + status (bool, optional) - pokud bude `TRUE`, vrátí pouze souhlasy, kde zákazník zaklikl svůj souhlas
    + agreement_id (int, optional) - ID souhlasu

+ Response 200 (application/json)

    + Attributes
        + agreements (array) - pole objektů se souhlasy
            + (object)
                + name (string) - název souhlasu
                + description (bool) - popis souhlasu
                + agreement_id (int, nullable) - ID souhlasu
                + time (date) - datum a čas udělení souhlasu/nesouhlasu
                + validity (date, nullable) - datum a čas, do kdy je souhlas platný
                + status (bool) - souhlas / nesouhlas
                + form (string) - název formuláře, ze kterého souhlas pochází

## Ověření přihlášení [/api/v2/customers/login]
Ověření emailu a hesla zákazníka.

### Ověření přihlášení [POST]

+ Request

    + Attributes
        + email (email) - přihlašovací email
        + password (string) - heslo

+ Response 200 (application/json)

    + Attributes
        + authenticated (bool) - když vrací `true`, je to platný přihlašovací email a heslo
        + messages (ErrorMessage)

## Skupiny zákazníků [/api/v2/groups]
Více o skupinách v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/skupiny-zakazniku).

### Vytvoření skupin [POST]

+ Request
    + Attributes
        + groups (array) - pole objektů se skupinami
            + (object)
                + name (string, required) - název

+ Response 200 (application/json)

    + Attributes
        + groups (array) - pole objektů se skupinami
            + (object)
                + name (string) - název
                + inserted_yn (bool) - příznak, jestli se skupina založila
                + messages (ErrorMessage)

### Aktualizace skupin [PUT]

+ Request
    + Attributes
        + groups (array) - pole objektů se skupinami
            + (object)
                + id (string, required) - ID skupiny
                + name (string, required) - název

+ Response 200 (application/json)

    + Attributes
        + groups (array) - pole objektů se skupinami
            + (object)
                + name (string) - název
                + updated_yn (bool) - příznak, jestli se skupina založila
                + messages (ErrorMessage)

### Seznam skupin [GET/api/v2/customers{?name}{?ids}{?page}]
Seznam skupin je dostupný po jednotlivých stranách, výstup je omezený na 100 položek na stránku.

+ Parameters
    + name (string, optional) - název
    + ids (array, optional) - ID skupin oddělené středníkem ;
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + groups (array) - pole objektů se skupinami
            + (object)
                + id (string) - ID skupiny
                + name (string) - název

### Smazání skupin [DELETE/api/v2/customers{?id}{?ids}]

+ Parameters
    + id (int, optional) - ID skupiny
    + ids (array, optional) - pole ID skupin

+ Response 200 (application/json)

    + Attributes
        + groups (array) - pole objektů se skupinami
            + (object)
                + id (string) - ID skupiny
                + deleted_yn (bool) - příznak, jestli se skupina smazala
                + messages (ErrorMessage)




# Group Košíky
## Košíky [/api/v2/carts/{id}/{?id}{?creation_time_from}{?language}{?filled_delivery_info_yn}{?customer_logged_in_yn}{?page}]
Více o košících v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/nedokoncene-kosiky).

### Seznam košíků [GET]
Seznam košíků je dostupný po jednotlivých stranách. Výstup je omezen na 100 položek na stránku.

+ Parameters
    + id (int, optional) - id konkrétního košíku
    + creation_time_from (date, optional) - datum, od kterého se košíky vrátí
    + language (language, optional) - jazyk
    + filled_delivery_info_yn (bool, optional) - pouze košíky s vyplněnými dodacími údaji
    + customer_logged_in_yn (bool, optional) - pouze košíky s přihlášenými zákazníky
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + carts (array) - pole objektů s košíky
            + (object)
                + id (int) - ID košíku
                + uuid (string) - UUID košíku, při vytvoření objednávky z košíku se toto UUID použije v objednávce
                + language (language)
                + datetime (date) - čas poslední aktualizace
                + customer (object) - zákazník
                    + email (email, nullable) - email zákazníka. Vyplněno pouze pokud má nepřihlášený zákazník již účet, nebo je zákazník přihlášený, jinak bude `null`
                    + voucher_code (string, nullable) - kód slevového kuponu zadaného v košíku
                    + voucher_type (string, nullable) - typ slevového kuponu zadaného v košíku
                    + points (int, nullable) - body věrnostního systému uplatněné zákazníkem v košíku
                    + customer_logged_in_yn (bool) - příznak, jestli je zákazník přihlášený
                    + filled_delivery_info_yn (bool) - příznak, jestli zákazník vyplnil dodací údaje
                + shipment (object, nullable) - doprava
                    + name (string) - název dopravy
                + payment (object, nullable) - platba
                    + name (string) - název platby
                + products (array) - pole objektů s produkty v košíku
                    + (object)
                        + id (int) - ID produktu v košíku (nesouhlasí s ID produktu)
                        + code (string, nullable) - kód produktu
                        + variant_code (string, nullable) - kód varianty
                        + length (string, nullable) - metráž
                        + quantity (float) - počet jednotek
                        + gift_code (string, nullable) - kód dárku k produktu
                        + gift_variant_code (string, nullable) - kód varianty dárku k produktu
                        + invoice_info (string, nullable) - poznámka k produktu, která se propisuje do faktury
                        + related_id (int, nullable) - vazba na jiný produkt v košíku, viz. funkce *Doplňky*


# Group Přesměrování

## Přesměrování [/api/v2/redirections]
Více o přesměrování v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/presmerovani-starych-url-adres-na-nove-1).

### Vytvoření přesměrování [POST]
Lze vytvořit pouze přesměrování typu `Custom` (manuální).

+ Request
    + Attributes
        + redirections (array) - pole objektů s přesměrováním
            + (object)
                + old (string, required) - stará adresa. Musí začínat https://
                + new (string, required) - nová adresa. Musí začínat https://
                + code (int) - kód přesmerování (301 - 308), výchozí hodnota je 301

+ Response 200 (application/json)

### Seznam přesměrování [GET/api/v2/redirections/{id}/{?ids}{?code}{?type}{?language_id_from}{?url_from}{?language_id_to}{?url_to}{?page}]

+ Parameters
    + id (int, optional) - ID přesměrování
    + ids (array, optional) - ID přesměrování oddělené středníkem `;`
    + code (string, optional) - kód přesměrování
    + type (enum, optional) - typ
        - Custom - manuální
        - Product - produkt
        - Variant - varianta
        - Advisor - rádce
        - Article - článek
        - Category - kategorie
        - News - aktualita
    + language_id_from (language, optional) - jazyk staré adresy
    + url_from (string, optional) - stará adresa
    + language_id_to(language, optional) - jazyk nové adresy
    + url_to (string, optional) - nová adresa
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + redirections (array) - pole objektů s přesměrováním
            + (object)
                + id (int) - ID přesměrování
                + type (enum) - typ
                    - Custom - manuální
                    - Product - produkt
                    - Variant - varianta
                    - Advisor - rádce
                    - Article - článek
                    - Category - kategorie
                    - News - aktualita
                + page_id (int) - ID stránky (pouze pokud není typ `Custom`)
                + language_id_from (bool) - jazyk staré adresy
                + url_from (date, nullable) - stará adresa
                + language_id_to (date, nullable) - jazyk nové adresy
                + url_to (string) - nová adresa
                + code (float) - kód přesměrování
                + last_update_time (date) - čas změny

### Smazání přesměrování [DELETE/api/v2/redirections/{?ids}]

+ Parameters
    + ids (string, optional) - ID přesměrování oddělené středníkem `;`

+ Response 200 (application/json)

    + Attributes
        + redirections (array) - pole objektů s přesměrováním
            + (object)
                + id (string) - ID přesměrování
                + deleted_yn (bool) - příznak, jestli se přesměrování smazalo
                + messages (ErrorMessage)


# Group Slevové kupóny

## Slevové kupóny [/api/v2/vouchers]
Více o slevových kupónech v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/slevove-karty).

### Vytvoření kupónů [POST]
Jedním požadavkem lze vytvořit jeden druh kupónů se stejnými parametry, definuje se počet. Pro vytvoření více druhů kupónů (s jinými parametry) je nutné udělat další požadavek.

+ Request

    + Attributes
        + count (int, optional) - počet kupónů (výchozí hodnota je 1)
        + active_yn (bool, optional) - příznak aktivní (výchozí hodnota je `true`)
        + global_yn (bool, optional) - příznak globální (výchozí hodnota je `false`)
        + for_products_in_action_yn (bool, optional) - příznak použitelný pro produkty v akci (výchozí hodnota je `false`)
        + date_from (date, optional) - použitelný od data
        + date_to (date, optional) - použitelný do data
        + type (enum, required) - typ kuponu
            - price - cena
            - percentage - procenta z objednávky
            - payment_shipment - doprava a platba
        + currency_id (currency, required) - měna
        + amount (float, required) - hodnota kupónu, podle typu buď procenta nebo částka
        + used_from (float, optional) - hodnota objednávky, od které lze kupón použít
        + note (string, optional) - poznámka

+ Response 200 (application/json)

    + Attributes
        + vouchers (array) - pole kódů nově vygenerovaných slevových kupónů

### Seznam kupónů [GET/api/v2/vouchers/{voucher_code}{?voucher_code}{?voucher_codes}{?currency_id}{?active_yn}{?for_products_in_action_yn}{?date_from}{?date_to}{?global_yn}{?page}]
Seznam kupónů je dostupný po jednotlivých stranách, výstup je omezen na 100 položek na stránku.

+ Parameters
    + voucher_code (string, optional) - kód kupónu
    + voucher_codes (string, optional) - kódy kupónů oddělené středníkem `;`
    + currency_id (currency, optional) - měna
    + active_yn (bool, optional) - aktivní
    + for_products_in_action_yn (bool, optional) - lze použít na produkty v akci
    + date_from (date, optional) - datum platnosti od
    + date_to (date, optional) - datum platnosti do
    + global_yn (bool, optional) - globální kupón
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + vouchers (array) - pole objektů s kupóny
            + (object)
                + voucher_code (string) - kód kupónu
                + active_yn (bool) - aktivní
                + global_yn (bool) - globální (lze použít vícekrát)
                + for_products_in_action_yn (bool) - lze použít na produkty v akci
                + date_from (date, nullable) - datum planosti od
                + date_to (date, nullable) - datum planosti do
                + type (enum) - typ kuponu
                    - price - cena
                    - percentage - procenta z objednávky
                + currency_id (currency)
                + amount (float) - hodnota kupónu
                + used_from (float) - lze použít od částky
                + note (string, nullable) - poznámka
                + creation_time (date) - datum vytvoření

### Smazání kupónů [DELETE/api/v2/vouchers/{voucher_code}{?voucher_code}{?voucher_codes}]

+ Parameters
    + voucher_code (string, optional) - kód kupónu
    + voucher_codes (string, optional) - kódy kupónů oddělené středníkem `;`

+ Response 200 (application/json)

    + Attributes
        + vouchers (array) - pole objektů s kupóny
            + (object)
                + code (string) - kód kupónu
                + deleted_yn (bool) - příznak, jestli se kupón smazal
                + messages (ErrorMessage)


# Group Aktuality

## Aktuality [/api/v2/news/{id}/{?id}{?creation_time_from}{?last_update_time_from}{?active_yn}{?language}{?page}]
Více o aktualitách v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/aktuality).

### Seznam aktualit [GET]
Seznam aktualit je dostupný po jednotlivých stranách. Výstup je omezen na 100 položek na stránku.

+ Parameters
    + id (int, optional) - ID konkrétní aktuality
    + creation_time_from (date, optional) - pouze aktuality vytvořené od zadaného data
    + last_update_time_from (date, optional) - pouze aktuality, u kterých došlo ke změně od zadaného data
    + active_yn (bool, optional) - aktivní / neaktivní
    + language (language, optional) - jazyk
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + news (array) - pole objektů s aktualitami
            + (object)
                + news_id (int) - ID aktuality
                + active_yn (date) - zobrazit aktualitu na webu
                + creation_time (date) - čas vytvoření aktuality
                + last_update_time (date) - čas poslední aktualizace
                + descriptions (array) - pole objektů s texty
                    + (object)
                        + language_id (language)
                        + title (string) - nadpis aktuality
                        + short_description (string, nullable) - krátký popis, bez HTML formátování
                        + long_description (string, nullable) - dlouhý popis, může obsahovat formátování pouze pomocí HTML značek
                        + url (string) - URL adresa aktuality
                + images (array) - pole objektů s obrázky
                    + (object)
                        + file_id (int) - ID souboru
                        + url (string) - URL adresa obrázku
                        + main_yn (bool) - hlavní obrázek
                        + list_yn (bool) - seznamový obrázek
                        + position (int) - pozice obrázku


# Group Články

## Články [/api/v2/articles/{id}/{?id}{?creation_time_from}{?last_update_time_from}{?active_yn}{?language}{?category_code}{?with_subcategories_yn}{?page}]
Více o článcích v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/clanky-1).

### Seznam článků [GET]
Seznam článků je dostupný po jednotlivých stranách. Výstup je omezen na 100 položek na stránku.

+ Parameters
    + id (int, optional) - ID konkrétního článku
    + creation_time_from (date, optional) - pouze články vytvořené od zadaného data
    + last_update_time_from (date, optional) - pouze články, u kterých došlo ke změně od zadaného data
    + active_yn (bool, optional) - aktivní / neaktivní
    + language (language, optional) - jazyk
    + category_code (string, optional) - pouze články patřící do kategorie s kódem
    + with_subcategories_yn (bool, optional) - specifikace filtru `category_code`, rozšiřuje i o články z podkategorie
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + articles (array) - pole objektů s články
            + (object)
                + article_id (int) - ID článku
                + active_yn (date) - zobrazit článek na webu
                + creation_time (date) - čas vytvoření článků
                + last_update_time (date) - čas poslední aktualizace
                + descriptions (array) - pole objektů s texty
                    + (object)
                        + language_id (language)
                        + title (string) - název článku
                        + short_description (string, nullable) - krátký popis, bez HTML formátování
                        + long_description (string, nullable) - dlouhý popis, může obsahovat formátování pouze pomocí HTML značek
                        + url (string) - URL adresa článku
                + images (array) - pole objektů s obrázky
                    + (object)
                        + file_id (int) - ID souboru
                        + url (string) - URL adresa obrázku
                        + main_yn (bool) - hlavní obrázek
                        + list_yn (bool) - seznamový obrázek
                        + position (int) - pozice obrázku
                + metas (array) - pole objektů s vlastními poli článků
                    + (object)
                        + key (string) - klíč vlastního pole
                        + type (string) - typ vlastního pole (hodnoty mohou být: radio, checkbox, input, date, email, number, select, multiselect, textarea, formatted)
                        + value (string) - hodnota vlastního pole, v případě kdy je hodnota vlastního pole společná pro všechny jazyky
                        + values (array) - pole objektů s hodnotami. V případě, když není hodnota vlastního pole společná pro všechny jazyky
                            + (object)
                                + language (language)
                                + value (string) - hodnota


# Group Rádce

## Rádce [/api/v2/advisor/{id}/{?id}{?creation_time_from}{?last_update_time_from}{?active_yn}{?language}{?page}]
Více o rádcích v Upgates e-shopech naleznete [zde](upgates.cz/a/radce).

### Seznam rad [GET]
Seznam rad je dostupný po jednotlivých stranách. Výstup je omezen na 100 položek na stránku.

+ Parameters
    + id (int, optional) - ID konkrétní rady
    + creation_time_from (date, optional) - pouze rady vytvořené od zadaného data
    + last_update_time_from (date, optional) - pouze rady, u kterých došlo ke změně od zadaného data
    + active_yn (bool, optional) - aktivní / neaktivní
    + language (language, optional) - jazyk
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + advices (array) - pole objektů s radami
            + (object)
                + advice_id (int) - ID rady
                + active_yn (date) - zobrazit radu na webu
                + creation_time (date) - čas vytvoření rady
                + last_update_time (date) - čas poslední aktualizace
                + descriptions (array) - pole objektů s texty
                    + (object)
                        + language_id (language)
                        + title (string) - nadpis rady
                        + short_description (string, nullable) - krátký popis, bez HTML formátování
                        + long_description (string, nullable) - dlouhý popis, může obsahovat formátování pouze pomocí HTML značek
                        + url (string) - URL adresa rady
                + images (array) - pole objektů s obrázky
                    + (object)
                        + file_id (int) - ID souboru
                        + url (string) - URL adresa obrázku
                        + main_yn (bool) - hlavní obrázek
                        + list_yn (bool) - seznamový obrázek
                        + position (int) - pozice obrázku


# Group Soubory
Více o souborech v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/spravce-souboru).

## Soubory [/api/v2/files]
Při nahrání se kontroluje unikátnost souboru, pokud systém zjistí že nahrávaný soubor již existuje, vrátí data již existujícího souboru.

### Nahrání souborů [POST]
Nahrání více souborů najednou pomocí stažení z URL adresy obsažené v požadavku. V JSONu lze poslat 3 objekty `file`. Timeout na stažení jednoho souboru je 20 vteřin, connection timeout je 3 vteřiny.

+ Request

    + Attributes
        + files (array, required) - pole objektů se soubory
            + (object)
                + url (string, required) - URL adresa souboru, je možné použít URL adresu na HTTP i FTP server
                + category_id (int, optional) - ID kategorie pro zařazení souboru

+ Response 200 (application/json)

    + Attributes
        + files (array)
            + (object)
                + id (string) - ID souboru
                + url (string) - URL obrázku
                + messages (ErrorMessage) - chybová zpráva
        + inserted_yn (bool) - vytvořeno
        + messages (ErrorMessage) - chybová zpráva

### Nahrání souboru [POST/api/v2/files/file]
Poslání obsahu souboru přes jako **form-data**, parametry jsou:
- **file** (*file, required*) - obsah souboru
- **file_name** (*string, optional*) - název souboru
- **category_id** (*int, optional*) - ID kategorie pro zařazení souboru

+ Response 200 (application/json)

    + Attributes
        + file (object)
            + id (string) - ID souboru
            + name (string) - název
            + mimetype (string) - MIMETYPE
            + size (string) - velikost v bytech
            + type (enum) - typ
                - image - obrázek
                - file - soubor
                - video - video
            + url (string) - URL obrázku
        + inserted_yn (bool) - vytvořeno
        + messages (ErrorMessage) - chybová zpráva

### Seznam souborů [GET/api/v2/files/{id}{?id}{?ids}{?type}{?category_id}{?deleted_yn}{?page}]

+ Parameters
    + id (int, optional) - ID souboru
    + ids (int, optional) - ID souborů
    + type (enum) - typ
        - image - obrázek
        - file - soubor
        - video - video
    + category_id (int, optional) - ID kategorie
    + deleted_yn (bool, optional) - příznak smazaného souboru
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + files (array) - pole objektů se soubory
            + (object)
                + id (string) - ID souboru
                + name (string) - název
                + mimetype (string) - MIMETYPE
                + size (string) - velikost v bytech
                + type (enum) - typ
                    - image - obrázek
                    - file - soubor
                    - video - video
                + deleted_yn (bool) - příznak smazaného obrázku
                + url (string) - URL obrázku, pokud je obrázek smazaný bude `NULL`

### Smazání souboru [DELETE/api/v2/files/{id}{?id}{?ids}]
Při smazání souboru nedojde k jeho fyzickému smazání, ale pouze k **přesunutí do koše**. V API (metoda `GET`) má smazaný soubor příznak `deleted_yn`

+ Parameters
    + id (int, required) - ID souboru
    + ids (array, optional) - ID souborů

+ Response 200 (application/json)

    + Attributes
        + files (array, required)
            + (object)
                + id (string) - ID souboru
                + delete_yn (bool) - příznak smazáno
                + messages (ErrorMessage) - chybová zpráva

## Kategorie souborů [/api/v2/files/categories]

### Seznam kategorií [GET/api/v2/files/categories{?page}{?id}{?ids}]

+ Parameters
    + id (int, optional) - ID kategorie
    + ids (array, optional) - ID kategorií
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + categories (array) - pole objektů s kategoriemi
            + (object)
                + id (string) - ID kategorie
                + name (string) - název
                + parent_id (string, nullable) - ID nadřazené kategorie


# Group Doprava
Pro práci s dopravami lze využívat **[webhooky](https://www.upgates.cz/a/dopravy)**.

Více o dopravách v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/nastaveni-moznosti-dopravy).

## Doprava [/api/v2/shipments/{id}]

### Seznam doprav [GET/api/v2/shipments/{id}/{?ids}{?code}{?codes}{?type}{?page}]

+ Parameters
    + id (int, optional) - ID dopravy
    + ids (array, optional) - ID dopravy oddělené středníkem `;`
    + code (string, optional) - kód dopravy
    + codes (array, optional) - kódy dopravy
    + type (string, optional) - typ dopravy
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + shipments (array) - pole objektů s dopravami
            + (object)
                + id (string) - ID
                + code (string, nullable) - kód dopravy
                + image_url (string, nullable) - URL adresa obrázku
                + type (enum) - typ dopravy
                    - custom - vlastní doprava
                    - ceskaPosta - Česká pošta
                    - slovenskaPosta - Slovenská pošta
                    - ulozenka - Uloženka
                    - zasilkovna - Zásilkovna (Packeta)
                    - dpd - DPD
                    - ppl - PPL
                    - gls - GLS
                    - wedo - WEDO
                    - depo - Depo
                + active_yn (bool) - příznak aktivní
                + affiliates (array, nullable) - pole typů poboček, pokud je `null`, nemá doprava pobočky
                    - balikovna (string) - Balíkovna, pouze Česka pošta
                    - balikobox (string) - Balíkobox, pouze Slovenská pošta
                    - naPostu (string) - na poštu, pouze Česka pošta a Slovenská pošta
                    - dpdBox (string) - výdejní box, pouze DPD
                    - pickupPoint (string) - výdejní místo, DPD
                    - parcelBox (string) - výdejní box, pouze GLS, PPL
                    - parcelShop (string) - výdejní místo, pouze GLS, PPL
                    - wedoBox (string) - výdejní box, pouze WEDO
                    - wedoPoint (string) - výdejní místo, pouze WEDO
                    - zasilkovna (string) - pouze Zásilkovna
                    - ulozenka (string) - pouze Uloženka
                    - depo (string) - pouze DEPO
                    - custom (string) - vlastní pobočky
                + tracking_url (string, nullable) - URL pro sledování zásilek
                + internal_note (string, nullable) - interní poznámka
                + descriptions (array)
                    + (object)
                        + language_id (language)
                        + name (string) - název
                        + description (string, nullable) - popis
                        + price (float, nullable) - cena
                        + free_from (float, nullable) - zdarma od
                + metas (Metas) - vlastní pole

## Pobočky dopravy [/api/v2/shipments/{id}/affiliates/]
Pracuje vždy s pobočkami jedné konkrétní dopravy.

### Seznam poboček dopravy [GET/api/v2/shipments/{id}/affiliates/{?page}]
Seznam poboček jde získat k jakémukoliv typu dopravy.

+ Parameters
    + id (int, required) - ID dopravy
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + affiliates (array) - pole objektů pobočkami
            + (object)
                + affiliate_id (string) - ID pobočky
                + name (string) - název pobočky
                + street (string) - ulice
                + city (string) - město
                + zip (string) - PSČ
                + country (country)
                + note (string, nullable) - poznámka

### Vytvoření pobočky dopravy [POST/api/v2/shipments/{id}/affiliates/]
Pobočky lze vytvážet pouze u vlastního typu dopravy. Pokud se pokusíte vytvořit pobočky u dopravy jiného typu, API vrátí chybu 403.

+ Parameters
    + id (int, required) - ID dopravy

+ Request (application/json)

    + Attributes
        + affiliates (array, required)
            + (object)
                + affiliate_id (string, optional) - ID pobočky, pokud není uvedeno použije se interní ID, může obsahovat pouze alfanumerické znaky bez mezer a bez diakritiky
                + name (string, required) - název pobočky
                + street (string, required) - ulice
                + city (string, required) - město
                + zip (string, required) - PSČ
                + country (country, required) - země
                + note (string) - poznámka

+ Response 200 (application/json)

    + Attributes
        + affiliates (array, required)
            + (object)
                + created_yn (bool) - vytvořeno
                + messages (ErrorMessage) - chybová zpráva

### Smazání pobočky dopravy [DELETE/api/v2/shipments/{id}/affiliates/{?affiliate_ids}{?delete_all_yn}]
Pobočky lze smazat pouze u vlastního typu dopravy. Pokud se pokusíte smazat pobočky u dopravy jiného typu, API vrátí chybu 403.

+ Parameters
    + id (int, required) - ID dopravy
    + affiliate_ids (array, optional) - ID poboček ke smazání
    + delete_all_yn (bool, optional) - pokud je `TRUE`, smaže všechny pobočky dopravy

+ Response 200 (application/json)

    + Attributes
        + affiliates (array, required)
            + (object)
                + affiliate_id (string) - ID pobočky
                + messages (ErrorMessage) - chybová zpráva

## Skupiny dopravy [/api/v2/shipments/groups/]
Více o skupinách doprav v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/zvlastni-zasilky#skupiny-doprav).

### Seznam skupin dopravy [GET/api/v2/shipments/groups/{?page}]

+ Parameters
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + groups (array) - pole objektů pobočkami
            + (object)
                + id (int) - ID skupiny
                + name (string) - název
                + position (int) - pozice


# Group Platba
Pro práci s platbami lze využívat **[webhooky](https://www.upgates.cz/a/platby-1)**.

Více o platbách v Upgates e-shopech naleznete [zde](https://www.upgates.cz/a/platby).

## Platba [/api/v2/payments/{id}]

### Seznam plateb [GET/api/v2/payments/{id}/{?ids}{?code}{?codes}{?type}{?page}]

+ Parameters
    + id (int, optional) - ID platby
    + ids (array, optional) - ID platby oddělené středníkem `;`
    + code (string, optional) - kód platby
    + codes (array, optional) - kódy platby
    + type (string, optional) - typ platby
    + page (int, optional) - stránka. Pokud není definováno, vrací vždy stranu 1

+ Response 200 (application/json)

    + Attributes
        + current_page (int) - aktuální strana
        + current_page_items (int) - počet položek na aktuální straně
        + number_of_pages (int) - celkový počet stran
        + number_of_items (int) - celkový počet položek
        + payments (array) - pole objektů s platbami
            + (object)
                + id (string) - ID
                + code (string, nullable) - kód platby
                + image_url (string, nullable) - URL adresa obrázku
                + type (enum) - typ platby
                    - cash - hotově
                    - cashOnDelivery - dobírka
                    - command - příkazem
                    - paypal - PayPal
                    - stripe - Stripe
                    - payu- PayU
                    - homecredit - Homecredit
                    - tatrapay - TatraPay
                    - tatracardpay - Tatra CardPay
                    - comgate - Comgate
                    - gopay - Gopay
                    - gpwebpay - GPwebpay
                    - cofidis - Cofidis
                    - essox - Essox
                    - twisto - Twisto
                    - cashOnCashRegister - hotově na pokladně
                    - cardOnCashRegister - kartou na pokladně
                    - thepay - ThePay
                    - custom - vlastní
                + active_yn (bool) - příznak aktivní
                + descriptions (array)
                    + (object)
                        + language_id (language)
                        + name (string) - název
                        + description (string, nullable) - popis
                        + price (float) - cena
                        + price_type (enum) - typ ceny
                            - fixed - pevná cena
                            - percentage - procentuální cena
                        + free_from (float, nullable) - zdarma od
                + metas (Metas) - vlastní pole


# Group Konverzní kódy
Konverzní kódy jsou vázány na **uživatele API.** Odstraněním API přístupu (anebo odinstalaci [doplňku](https://www.upgates.cz/a/pro-vyvojare-doplnky)), se konverzní kódy smažou.

Pokud budete využívat měřící scripty, můžete nahlédnout do naší dokumentace [Dynamických zástupců](https://www.upgates.cz/a/dokumentace-zastupci-v-konverznich-kodech).

V rámci API, nelze zasáhnout do [vlastních konverzních kódů](https://www.upgates.cz/a/princip-konverznich-kodu), které si vytváří majitel e-shopu ručně v adminsitraci.

Konverzní kód (`code`) je vložen přímo do HTML, tzn. že JavaScriptový kód musí být obalen do tagu `<script>`.



## Konverzní kódy [/api/v2/conversion-codes]

### Vytvoření konverzního kódu [POST]

+ Request (application/json)

    + Attributes
        + conversion_codes (array, required)
            + (object)
                + position (ConversionCodePosition, required) - Pozice
                + language_id (language, required) - Jazyk
                + code (string, required) - Chybová zpráva

+ Response 200 (application/json)

    + Attributes
        + conversion_codes (array, required)
            + (object)
                + position (ConversionCodePosition) - Pozice
                + language_id (language)
                + messages (ErrorMessage) - Chybová zpráva

### Seznam konverzních kódů [GET/api/v2/conversion-codes/{position}{?language_id}]

+ Response 200 (application/json)

    + Attributes
        + conversion_codes (array, required)
            + (object)
                + position (ConversionCodePosition) - Pozice
                + language_id (language)
                + code (string) - Konverzní kód

+ Parameters
    + position (string, optional)
    + language_id (language, optional)

### Aktualizace konverzního kódu [PUT]

+ Request (application/json)

    + Attributes
        + conversion_codes (array, required)
            + (object)
                + position (ConversionCodePosition, required) - Pozice
                + language_id (language, required) - Jazyk
                + code (string, required) - Chybová zpráva

+ Response 200 (application/json)

    + Attributes
        + conversion_codes (array, required)
            + (object)
                + position (string) - Pozice
                + language_id (language)
                + messages (ErrorMessage) - Chybová zpráva

### Smazání konverzního kódu [DELETE/api/v2/conversion-codes/{position}{?language_id}]

+ Parameters
    + position (string, optional)
    + language_id (language, optional)

+ Response 200 (application/json)

    + Attributes
        + conversion_codes (array, required)
            + (object)
                + position (ConversionCodePosition) - Pozice
                + language_id (language)
                + messages (ErrorMessage) - Chybová zpráva


# Group Webhooky
Více na téma webhooky v Upgates najdete [zde](https://www.upgates.cz/a/webhooky). Endpoint nevyžaduje nastavení oprávnění, je povolen vždy pro všechny API uživatele.

## Webhooky [/api/v2/webhooks]

### Vytvoření webhooku [POST]

+ Request
    + Attributes
        + active_yn (bool, optional) - příznak, jestli je webhook aktivní. Výchozí hodnota je `true`
        * name (string, required) - název webhooku, pouze pro interní označení
        * url (string, required) - URL adresa, musí obsahovat schéma a doménu ([Absolute URI](https://www.rfc-editor.org/rfc/rfc3986#page-27)). Může obsahovat i přihlašovací údaje
        * event (string, required) - událost, seznam dostupných událostí můžete získat pomocí metody GET `/api/v2/webhooks/events`

+ Response 200 (application/json)

    + Attributes
        + webhook (object)
            + id (int) - ID webhooku
            + active_yn (bool) - příznak, jestli je webhook aktivní
            + name (string, required) - název webhooku, pouze pro interní označení
            + url (string, required) - URL adresa
            + event (string, required) - událost

### Aktualizace webhooku [PUT]
Webhooky se párují podle hodnoty `id`

+ Request
    + Attributes
        + id (int, required) - ID webhooku
        + active_yn (bool, optional) - příznak, jestli je webhook aktivní
        + name (string, optional) - název webhooku, pouze pro interní označení
        + url (string, optional) - validní URL adresa, může obsahovat i přihlašovací údaje
        + event (string, optional) - událost, seznam událostí můžete získat pomocí metody GET `/api/v2/webhooks/events`

+ Response 200 (application/json)

    + Attributes
        + webhook (object)
            + id (int) - ID webhooku
            + active_yn (bool) - příznak, jestli je webhook aktivní
            + name (string) - název webhooku, pouze pro interní označení
            + url (string) - URL adresa
            + event (string) - událost

### Smazání webhooku [DELETE/api/v2/webhooks/{id}{?ids}]

Musí být definováno ID webhooku v jednom z parametrů.

+ Parameters
    + id (string, optional) - ID webhooku
    + ids (string, optional) - ID webhooků oddělená středníkem `;`

+ Response 200 (application/json)

    + Attributes
        + webhooks (array) - pole objektů s webhooky
            + (object)
                + id (string) - ID webhooku
                + deleted (bool) - příznak, jestli je webhook smazaný
                + messages (ErrorMessage)

### Seznam webhooků [GET/api/v2/webhooks/{id}]

+ Parameters
    + id (string, optional) - ID webhooku

+ Response 200 (application/json)

    + Attributes
        + webhooks (array) - pole objektů s webhooky
            + (object)
                + id (int) - ID webhooku
                + active_yn (bool) - příznak, jestli je webhook aktivní
                + name (string) - název webhooku, pouze pro interní označení
                + url (string) - URL adresa
                + event (string) - událost
                + last_success_call (date, nullable) - čas posledního úspěšného volání
                + last_success_call_status (int, nullable) - HTTP status posledního úspěšného volání
                + last_error_call (date, nullable) - čas posledního neúspěšného volání
                + last_error_call_status (int, nullable) - HTTP status posledního neúspěšného volání
                + creation_time (date) - čas vytvoření

### Události webhooků [GET/api/v2/webhooks/events]
Vrací seznam dostupných událostí.

+ Response 200 (application/json)

    + Attributes
        + events (array) - pole objektů s událostmi
            + (object)
                + name (string) - název události
                + allowed_yn (string) - příznak, jestli je událost pro aktuálního uživatele API povolena


# Group E-shop

## Nastavení eshopu [/api/v2/config]
Vrací atributy nastavení e-shopu.

### Nastavení eshopu [GET]

+ Response 200 (application/json)

    + Attributes
        + config (object, required)
            + prices_with_vat_yn (bool) - příznak o ukládání cen s a bez DPH. Pokud je `TRUE`, e-shop ukládá ceny s DPH
            + vat_payer_yn (bool) - příznak, jestli je provozovatel e-shopu plátcem DPH
            + oss_yn (bool) - příznak, jestli se používá režim OSS
            + limit_orders (enum, optional) - omezení objednání
                - 0 - vypnuto
                - 1 - zapnuto pro všechny produkty
                - sale - pouze pokud jsou produkty ve výprodeji
        + languages (object, required) - **NEPOUŽÍVAT ZASTARALÉ, BUDE ODSTRANĚNO, místo tohoto použít endpoint na [jazyky](https://upgates.cz/a/api-v2-jazyky)**
        + pricelists (object, required) - **NEPOUŽÍVAT ZASTARALÉ, BUDE ODSTRANĚNO, místo tohoto použít endpoint na [ceníky](https://upgates.cz/a/api-v2-ceniky)**


# Group Ceníky
## Ceníky [/api/v2/pricelists]
Pro práci s ceníky lze využívat **[webhooky](https://www.upgates.cz/a/ceniky)**.

Více na téma ceníky v Upgates naleznete [zde](https://www.upgates.cz/a/ceniky-maloobchod-a-velkoobchod).

### Vytvoření ceníků [POST]

+ Request
    + Attributes
        + pricelists (array)
            + (object)
                + name (string) - název ceníku
                + percent (int) - procenta slevy
            
+ Response 200 (application/json)

    + Attributes
        + pricelists (array) 
            + (object)
                + customer_pricelist_id (int) - ID ceníku
                + name (string) - název ceníku, musí být unikátní 
                + created_yn (bool) - příznak, jestli se ceník vytvořil
                + messages (ErrorMessage)

### Seznam ceníků [GET]

+ Response 200 (application/json)

    + Attributes (object)
        + pricelists (array, required)
            + (object)
                + id (int) - ID ceníku
                + name (string) - název ceníku
                + percent (float) - procentuální sleva nastavená v ceníku
                + default_yn (string) - příznak, jestli je ceník výchozí

### Smazání ceníku [DELETE/api/v2/pricelists/{id}]
Nelze smazat výchozí ceník.

+ Parameters
    + id (string, optional) - ID ceníku

+ Response 200 (application/json)

    + Attributes
        + webhooks (array) - pole objektů s webhooky
            + (object)
                + id (string) - ID ceníku
                + deleted_yn (bool) - příznak, jestli je ceník smazaný
                + messages (ErrorMessage)


# Group Jazyky
## Jazyky [/api/v2/languages]
Pro práci s jazyky lze využívat **[webhooky](https://www.upgates.cz/a/jazyky)**.

Více na téma jazyky a jazykové mutace v Upgates naleznete [zde](https://www.upgates.cz/a/typy-jazykovych-mutaci).

### Jazyky eshopu [GET]

+ Response 200 (application/json)

    + Attributes (object)
        + languages (array, required)
            + (object)
                + language_id (language) - ID jazyka
                + actual_language_id (language) - ID skutečného jazyka (pokud má e-shop např. na více jazykových mutacích stejný jazyk)
                + active_yn (bool) - příznak, jestli je jazyk aktivní
                + default_yn (bool) - příznak, jestli je jazyk hlavní
                + domain (string) - doména jazykové mutace
                + currency_id (currency)
                + default_country_id (country, nullable) - výchozí země
                + logo_url (string, nullable) - URL adresa loga jazykové mutace, může vést na SVG soubor
                + logo_no_svg (string, nullable) - URL adresa loga jazykové mutace, nebude vést na SVG soubor

# Group Provozovatel eshopu
## Fakturační údaje [/api/v2/owner]
Více na téma  provozovatel e-shopu v Upgates najdete [zde](https://www.upgates.cz/a/nastaveni-fakturacnich-udaju-e-shopu).

### Provozovatel eshopu [GET]

+ Response 200 (application/json)

    + Attributes (object)
        + owner (array)
            + (object)
                + company (string) - název firmy
                + company_number (string, nullable) - IČO
                + vat_number (string, nullable) - DIČ
                + vat_country_id (string, nullable) - Registrace DPH v zemi
                + street (string) - Ulice
                + city (string) - Město
                + state (string) - Kraj
                + zip (string) - PSČ
                + country_id (string) - Země
                + language_id (string) - Jazyk
                + email (email, nullable) - Emailová adresa
                + phone (string, nullable) - Telefon
                + firstname (string, nullable) - Jméno
                + surname (string, nullable) - Příjmení
                + bank_account (string, nullable) - Číslo účtu
                + bank_symbol (string, nullable) - Kód banky
                + bank_specific_symbol (string, nullable) - Specifický symbol
                + iban (string, nullable) - IBAN
                + swift (string, nullable) - BIC / SWIFT


# Group Stav API
Slouží pro zjištění stavu API. Vrací seznam povolených endpointů pro aktuálního uživatele. Endpoint nevyžaduje nastavení oprávnění, je povolen vždy pro všechny API uživatele.

## Stav API [/api/v2/status]

### Informace o stavu API [GET]

+ Response 200 (application/json)

    + Attributes (object)
        + services (array, required) - API endpointy
            + (object)
                + service (string) - název služby
                + url (string) - URL adresa endpointu
                + privilege (enum) - práva na přístup k endpointu
                    - deny - není povolen žádný přístup
                    - readonly - povolena pouze HTTP GET metoda
                    - all - povoleno vše
        + documentation_link (string) - URL adresa dokumentace API


# Group Grafika

## Číselník Errors
 `type` | doplňující informace
---|--------
 InputError | chybná vstupní data
 CodeValidationError | nevalidní obsah souboru, je možnost využít property `line`
 BackupCountError | chyba při vytvoření zálohy 
 PermissionsError | chyba při neoprávněné manipulaci s položkou

## Editor kodu [/api/v2/graphics/code]
Slouží pro práci se soubory na [testovací verzi grafiky](https://www.upgates.cz/a/eshop-pohled-zakaznika#testovaci-verze-e-shopu) e-shopu. Tento endpoint slouží pro práci s nástrojem [Editor kódu](https://www.upgates.cz/a/editor-kodu) v administraci.

Více informací ohledně [struktury souborů a složek](https://www.upgates.cz/a/struktura-adresaru-a-souboru) nebo [základní dokumentace grafických šablon](https://www.upgates.cz/a/dokumentace-latte) naleznete v [nápovědách](https://www.upgates.cz/pruvodce).

Všechny cesty jsou vzhledem k root složce `/`. Dle [verze grafiky](https://www.upgates.cz/a/finalizace-grafiky#zjisteni-aktualni-verze-grafiky) se mohou měnit názvy a umístění systémovách souborů.

### Seznam souborů [GET/api/v2/graphics/code{?pathname}]
Seznam souboru ovlivňují zapnuté [Rozšířené možnosti](https://www.upgates.cz/a/editor-kodu#rozsirene-moznosti-scroll) Editoru kódu

+ Parameters
    + pathname (string, optional) - výpis konkrétní složky(souborů a složek). Pokud není uvedeno, vylistuje se rootovská složka `/`

+ Response 200 (application/json)

    + Attributes
        + pathname (string) - cesta ke složce
        + last_update_time (date) - datum poslední změny
        + custom_yn (bool) - vlastně vytvořená složka
        + items (array)
            + (object)
                + type (enum, required)
                    - directory - složka
                    - file - soubor
                + pathname (string, required) - cesta k souboru/složce
                + last_update_time (date, required) - datum poslední změny
                + custom_yn (bool, required) - vlastně vytvořený/á soubor/složka
                + size (int) - informaci o velikosti souboru
                + readonly_yn (bool) - soubor pouze pro čtení
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object)
                + type (string, required)
                + message (string, required) 
        
+ Response 500 (application/json)

### Obsah souboru [GET/api/v2/graphics/code{?pathname}]

+ Parameters
    + pathname (string, required) - cesta k souboru

+ Response 200 (application/json)

    + Attributes
        + pathname (string) - cesta k souboru
        + last_update_time (date) - datum poslední změny
        + custom_yn (bool) - vlastně vytvořený soubor
        + size (int) - informaci o velikosti souboru
        + content (string) - obsah souboru
        + readonly_yn (bool) - pouze pro čtení
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object) - např. název není validní
                + type (string, required)
                + message (string, required)
                
+ Response 500 (application/json)

### Vytvoření souboru/složky [POST]

Je omezeno pouze vypnutý grafický editor [Designer](https://www.upgates.cz/a/designer-modul) a na složku `/templates` a soubory `.phtml`

+ Request
    + Attributes
        + pathname (string, required) - název souboru/složky(`/path/<name><.><extension>`), musí být úspešně zvalidován REGEX `/^([a-zA-Z0-9_-]){1,50}$/i`
        + type (enum, required)
            - directory - složka
            - file - soubor
        + content (string) - volitelný obsah souborů
            
+ Response 200 (application/json)

    + Attributes
        + pathname (string)
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object) - např. název není validní, cesta k nadřazené složce neexistuje, obsah souboru není validní
                + type (string, required)
                + message (string, required) 
                + line(int)
        
+ Response 500 (application/json)

### Aktualizace obsahu souboru [PUT]

+ Request

    + Attributes
        + pathname (string, required) - cesta k souboru
        + content (string, required) - obsah souboru

+ Response 200 (application/json)

    + Attributes
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object) - např. zadaný pathname není cesta k souboru, obsah není validní
                + type (string, required)
                + message (string, required) 
                + line(int)
        
+ Response 500 (application/json)

### Smazání souboru/složky [DELETE]

+ Request
    + Attributes
        + pathname (string, required) - cesta k souboru/složce
            
+ Response 200 (application/json)

    + Attributes
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object) - např. zadaný pathname neexistuje, položka je systémová, takže nejde smazat, složka obsahuje soubory
                + type (string, required)
                + message (string, required) 
        
+ Response 500 (application/json)

## Zálohy [/api/v2/graphics/backups]
Slouží pro přehled grafických záloh a správu [manuálních záloh](https://www.upgates.cz/a/zalohy-grafiky-napoveda#manualni-zalohy-grafiky).

### Seznam záloh [GET]

 `type` | popis | `addition_data`
---|--------|---
manual | ručně vytvořena
system.updateFinal | [překlopení](https://www.upgates.cz/a/finalizace-grafiky) testovací verze grafiky na [ostrou verzi](https://www.upgates.cz/a/eshop-pohled-zakaznika#ostra-verze-e-shopu-na-domene) grafiky na doméně
system.updateConfigurator | změna verze grafiky | informace o konkrétních verzích v `from` a `to` 
system.disableConfigurator | vypnutí grafického editoru Designer/zapnutí editoru kodu
system.enableConfigurator | zapnutí grafického editoru Designer/vypnutí editoru kodu

+ Response 200 (application/json)
    
    + Attributes
        + backups (array)
            + (object)
                + token (string, required)
               + creation_time (date, required) - datum vytvoření zálohy
                + type (enum, required)
                    - manual
                    - system.updateFinal
                    - system.updateConfigurator
                    - system.disableConfigurator
                    - system.enableConfigurator
                + aditional_data (array) - dodatečné informace
                    + (object)
                + name (string) - pouze v případě `type` = `manual`
                + expiration_time (date) - pouze u záloh systémových
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object)
                + type (string, required)
                + message (string, required) 

+ Response 500 (application/json)

### Vytvoření zálohy [POST]

+ Request
    + Attributes
        + name (string, required) - název zálohy, max. délka 256 znaků
            
+ Response 200 (application/json)
    + Attributes
        + token (string)
        + creation_time (date) - datum vytvoření zálohy
        + type (string) - `manual` - ručně vytvořena
        + name (string)
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object) -  např. překročena délka názvu
                + type (string, required)
                + message (string, required)
        
+ Response 500 (application/json)

### Obnovení zálohy [PUT]

+ Request
    + Attributes
        + token (string, required)
            
+ Response 200 (application/json)

    + Attributes
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object) -  např. záloha nebyla nalezena
                + type (string, required)
                + message (string, required)
        
+ Response 500 (application/json)

### Smazání zálohy [DELETE]

+ Request
    + Attributes
        + token (string, required)
            
+ Response 200 (application/json)

    + Attributes
        + success (bool, required)
        + errors (array) - pokud je `success` = `false`
            + (object) -  např. záloha nebyla nalezena
                + type (string, required)
                + message (string, required)
        
+ Response 500 (application/json)

# Group Doplňky

Jak vytvářet doplňky zjistíte v naší sekci [Pro vývojáře](https://www.upgates.cz/a/api-dokumentace-doplnku).

<!-- Slouží pro napojení doplňku do administrace Upgates e-shopů. Jakmile klient požádá o aktivaci, deaktivaci nebo otevření daného doplňku, systém vyhodnotí odpověď na požadavek zaslaný na endpoint doplňku. Následně zobrazí klientovi výsledek (úspěšný nebo neúspěšný). 
- Vyžadujeme **SSL certifikát** na všech API endpointech.
- Dbát při implementaci na nepřetěžování serveru(využívat [webhooky](https://app.apiary.io/upgatesapiv2/editor)) - porušení může způsobit blokaci API přístupů doplňku na všechny eshopy.

## Best practices
- Při návrhu doplňku byste měli počítat s tím, že z naší strany, i když ne přímo cíleně, může přijít více požadavku na aktivaci, již aktivovaného doplňku nebo také požadavek na deaktivaci, aktuálně neaktivního doplňku.
- V případě práce s API více e-shopů na jednom serveru je potřeba vytížení rozdělit časově během celého dne, a nestahovat data např. pouze během noci nebo v 00:00 apod.
    - Např. si rozdělit pool e-shopů a přidávat offsety po hodinách nebo jiných větších časových úsecích:
        - 2 e-shopy v 00:00
        - 2 e-shopy v 01:00
        - atd.
- Hlavním atributem pro testování doplňků z vaší strany, by měla být uživatelská přívětivost. Než nám doplněk předáte k testování, prosím ověřte si, že dokážete váš doplněk obsluhovat jako běžný zákazník (správně se vytvoří uživatelský účet, funguje odhlášení a opětovné přihlášení do vašeho prostředí, atd.). Ulehčí se tím celkový proces schvalování doplňku.
- Hlavním cílem při kontrole z naší strany vašeho doplňku, bude zajistit co nejlepší používání API.
    - Místo opakovaných dotazů (například na stavy objednávek, jazyky, majitel, atd.) využívejte co nejvíce cache
    - Nepoužívejte tlačítko "Synchronizovat". Pokud jej pro fungování opravdu potřebujete, nastavte u něj ochranu opakovaného klikání, a také aby nebylo možné tlačítko stiknout znovu, pokud běží ještě původní proces synchronizace.

## Podepisování
Data podepisujeme privátním klíčem a vy si je můžete zkontrolovat [veřejným klíčem](https://files.upgates.com/addons/signature/api.signature.pub.key) metodou *OPENSSL_ALGO_SHA256*. Podpis můžete nalézt v každém těle požadavku pod klíčem `signature`. Dle požadavků se podepisují příslušná data.
- Z podepisovaných dat je vyjmut `current_admin_language`.
- Jednotlivá podepisovaná data nalezenete u každého endpointu.
- Doporučujeme vždy načítat aktuální [veřejný klíč](https://files.upgates.com/addons/signature/api.signature.pub.key) při ověřování podpisu a neukládat jej u sebe pro pozdější použití. Důvodem je možnost změny klíčů.


## Testování
Během žádosti o implementaci doplňku v administraci jste vyplňovali testovací projekt/e-shop. V případě schválení techniky Upgates bude možné vidět váš doplněk pouze v administraci tohoto konkrétního projektu, v seznamu doplňků. Budete mít možnost si jej aktivovat, deaktivovat a případně zobrazit/přejít na jeho detail.

### Příklad ověření podpisu v PHP

```PHP
<?php
$data = implode(";",[...]);
$signature = 'a0e0a3e7689bd4c80e4d6ffcccb05235b864e1d0';
$signaturePublicKey = file_get_contents("https://files.upgates.com/addons/signature/api.signature.pub.key");
$verify = openssl_verify($data, base64_decode($signature), $signaturePublicKey, OPENSSL_ALGO_SHA256);
```

## FAQ
Často kladené otázky.

#### Chci pracovat s informacemi o aktuálně přihlášeném uživateli při otevření doplňku?
Bude možné využít nový endpoint pro stažení informací o uživatelích, na kterém aktuálně pracujeme. V endpointu pro otevření doplňku přibude informace s indentifikátorem uživatele. Je nutno vyžádat si a zdůvodnit si přístup pro tento nový endpoint při žádosti o založení doplňků. 


## Aktivace doplňku [/vášInstalačníAPIEndoint]

### Instalační API endpoint [POST]

#### Podpis
```PHP
$data = implode(";",[
    "token" => "...",
    "apiUser" => "...",
    "apiKey" => "...",
    "apiUrl" => "https://...",
]);
```

#### Neúspěšná instalace
- Doplněk nelze aktivovat, pokud:
    - Vaše odpověď je **delší než 5 vteřin**.
    - Jakákoliv jiná odpověď než se stavovým kódem **HTTP 200**.
    - Odpověď **HTTP 200** není validní.

#### Odpověď (Validace)
- `required` attribut `error`
    - `TRUE` (bool) - Problém na straně doplňku - instalace by proběhla v pořádku, ale zákazník musí před instalací splnit dodatečné podmínky, než bude moct nainstalovat doplněk.
    - `FALSE` (bool) - Vše proběhlo v pořádku, doplněk je úspěšně nainstalován.

+ Request 200 (application/json)

    + Attributes (object)
        + token (string) - identifikátor e-shopu
        + apiUser (string) - uživatelský přistup do API e-shopu
        + apiKey (string) - uživatelské přistupové heslo do API e-shopu
        + apiUrl (string) - [BASE API URI eshopu](https://upgatesapiv2.docs.apiary.io/#introduction/zakladni-informace)
        + current_admin_language (enum) - jazyk administrace podle ISO 639-1 (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
            - cs - Čeština
            - sk - Slovenština
            - en - Angličtina
        + signature (string) - **base64_encode** podpis specifikovaných atributů pomocí privatního klíče

+ Response 200 (application/json)

    + Attributes (object)
        + error (bool, required)
        + message (string) - potřebné pokud je `error = TRUE`.


## Deaktivace doplňku [/vášOdinstalačníAPIEndoint]

### Odinstalační API endpoint [POST]

- nečeká se na odpověď HTTP 200 - při jakékoliv odpovědi se provede odinstalace v Upgates.
- smažou se API přístupy(bude se vracet 401 Unauthorized).
- smažou se navázané věci na API uživatele (konverzní kódy, webhooky).

#### Podpis
```PHP
$data = implode(";",[
    "token" => "..."
]);
```

+ Request 200 (application/json)

    + Attributes (object)
        + token (string) - identifikátor e-shopu.
        + signature (string) - **base64_encode** podpis specifikovaných atributů pomocí privatního klíče.

+ Response 200 (application/json)

## Otevření doplňku [/vášAPIEndointProZískáníOdkazu]

### Odkaz pro přesměrování / iframe [POST]

#### Podpis
```PHP
$data = implode(";",[
    "token" => "..."
]);
```

#### Doplněk není dostupný
- Jakákoliv jiná odpověď než se stavovým kódem **HTTP 200**.
- Odpověď **HTTP 200** není validní.

#### Iframe
- Je potřeba se přiblížit stylům v administrace Upgates do té míry, jak je to možné.
- Komunikace mezi iframe a administrací Upgates **nebude probíhat**.

+ Request 200 (application/json)

    + Attributes (object)
        + token (string) - identifikátor e-shopu.
        + current_admin_language (enum) - jazyk administrace podle ISO 639-1 (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes):
            - cs - Čeština
            - sk - Slovenština
            - en - Angličtina
        + signature (string) - **base64_encode** podpis specifikovaných atributů pomocí privatního klíče.

+ Response 200 (application/json)

    + Attributes (object)
        + url (string) - včetně SSL
        + type (enum)
            - iframe - 
            - redirect - přesměrujeme na vámi zadanou URL, např. se automaticky přihlásí do vašeho IS.
        
-->

# Data Structures

## bool (boolean)

    true / false, 1 / 0

## int (number)

    Celé číslo

## float (number)

    Desetinné číslo, jako oddělovač desetinných míst používejte tečku

## date (string)

    Datum zapsané jako řeťezec znaků dle [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)

## email (string)

    Validní emailová adresa

## language (string)

    Kód jazyka dle [ISO 639-1](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)

## country (string)

    Kód země dle [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

## currency (string)

    Kód měny dle [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217)

## ErrorMessage (array)
+ (object)
    + object (string, nullable) - název objektu (část JSONu), kterého se zpráva týká
    + property (string, nullable) - hodnota, které se zpráva týká
    + message (string) - text zprávy
    + level (enum) - úroveň chyby
        - info - informační sdělení
        - warning - varování
        - error - chyba, pravděpodobně nedošlo ke zpracování 
        - fatal_error - chyba API, kontaktujte technickou podporu

## ConversionCodePosition (enum)
- head - kód je umístěn mezi tagy `<head>` a `</head>` na každé stránce
- body_top - kód je umístěn na začátku tagu `<body>` na každé stránce
- body_bottom - kód je umístěn před tagem `</body>` na každé stránce
- order_head - kód je umístěn mezi tagy `<head>` a `</head>` na stránce po dokončení objednávky
- order_body_top - kód je umístěn na začátku tagu `<body>` na stránce po dokončení objednávky
- order_body_bottom - kód je umístěn před tagem `</body>` na stránce po dokončení objednávky

## ProductParameters (array)
+ (object)
    + name (object) - objekt s názvy parametrů v jednotlivých jazycích (klíč každé položky v objektu je typu *language*)
    + values (array) - pole objektů s hodnoty parametrů v jednotlivých jazycich (klíč každé položky v objektu je typu *language*)

## ProductLabels (array)
+ (object)
    + label_id (int) - interní ID štítku
    + name (object) - objekt s názvy štítků v jednotlivých jazycích (klíč každé položky v objektu je typu *language*)
    + active_currently_yn (bool) - štítek aktuálně aktivní, zohledňuje i data od a do
    + active_yn (bool) - štítek aktivní
    + active_from (date) - štítek aktivní od data
    + active_to (date) - štítek aktivní do data

## Metas (array)
+ (object)
    + key (string) - klíč vlastního pole
    + type (enum) - typ vlastního pole
        - radio
        - checkbox
        - input
        - date
        - email
        - number
        - select
        - multiselect
        - textarea
        - formatted
    + value (string) - hodnota vlastního pole v případě, když je hodnota vlastního pole společná pro všechny jazyky
    + values (array) - pole objektů s hodnotami v případě, když není hodnota vlastního pole společná pro všechny jazyky
        + (object)
            + language (language)
            + value (string) - hodnota


---