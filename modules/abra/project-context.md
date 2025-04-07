🚀 System Prompt for Python 3.12 Development 🚀

References:
https://ai.pydantic.dev/api/
https://logfire.pydantic.dev/docs/
https://docs.pydantic.dev/latest/

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