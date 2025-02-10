#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
CLI tool for managing Upgates API sync, translation, and configuration.

Usage:
    python cli.py [COMMAND]

Commands:
    start-webhook       Start webhook server for real-time updates.
    start-scheduler     Start scheduled auto-sync process.
    sync-all            Sync all data: products, customers, orders.
    sync-products       Sync products data.
    sync-customers      Sync customers data.
    sync-orders         Sync orders data.
    list-product-fields List all available product fields
    search-product      Search for a product by product_code.
    show-products       Show all products with related data.
    show-customers      Show all customers.
    show-orders         Show all orders.
    translate-product   Translate product descriptions for a given language.
    save-translation    Save the updated product translations back to Upgates.cz API.
    clear-cache         Force-clear the DuckDB cache file.
    
    
File:
    $> upgates --help
"""

import sys
import os
import click
import asyncio
import subprocess

import duckdb
import IPython
import yaml


from rich.console import Console

# Ensure the package directory is included in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from upgates.client import UpgatesClient
from upgates import config

# Configure Rich Console output
console = Console()

def _clear_cache() -> int:
    """Clear the DuckDB cache file."""
    db_file = config.default_db_path
    if os.path.exists(db_file):
        os.remove(db_file)
        console.print(f"DuckDB cache file cleared: {db_file}")
        return 1
    else:
        console.print("Cache file not found, nothing to clear.")
        return 0


# Define the CLI commands

# CLI group
@click.group()
def cli():
    """CLI for managing Upgates API sync, translation, and configuration.""" 
    pass

# CMD: Start Webhook
@click.command()
def start_webhook():
    """Start webhook server for real-time updates.""" 
    subprocess.run(["python", "webhook_server.py"])

# CMD: Start Scheduler
@click.command()
def start_scheduler():
    """Start scheduled auto-sync process.""" 
    subprocess.run(["python", "scheduler.py"])


####


@click.command()
@click.option('--clear-cache', is_flag=True, help="Clear the cache before syncing.")
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
@click.option('--embed', is_flag=True, help="Launch ipython.embed() shell after syncing.")
def sync_products(clear_cache, page_count, embed):
    """Sync products data."""
    
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
        
    client = UpgatesClient()
    asyncio.run(client.sync_products(page_count=page_count))
    
    if embed:
        IPython.embed()

@click.command()
@click.option('--clear-cache', is_flag=True, help="Clear the cache before syncing.")
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
def sync_customers(clear_cache, page_count):
    """Sync customers data."""
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    client = UpgatesClient()
    asyncio.run(client.sync_customers(page_count=page_count))

@click.command()
@click.option('--clear-cache', is_flag=True, help="Clear the cache before syncing.")
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
def sync_orders(clear_cache, page_count):
    """Sync orders data."""
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    client = UpgatesClient()
    asyncio.run(client.sync_orders(page_count=page_count))

@click.command()
@click.option('--page-count', default=None, type=int, help="Number of pages to fetch. Default is all pages.")
def sync_all(page_count):
    """Sync all data: products, customers, orders."""
    client = UpgatesClient()
    asyncio.run(client.sync_all(page_count=page_count))


####

@click.command()
def list_product_fields():
    """List all available product fields."""
    client = UpgatesClient()
    fields = client.db_api.get_product_fields()
    console.print(f"📦 Available product fields ({len(fields)})")
    console.print(fields)


# CMD: Translate Product 
@click.command()
@click.argument("product_code")
@click.argument("target_lang")
@click.argument("prompt", nargs=-1)
@click.option("--save", is_flag=True, default=False, help="Save the translation back to Upgates.cz API.")
@click.option("--update", is_flag=True, default=False, help="Update the product translations before saving.")
def translate_product(product_code, target_lang, prompt, save, update):
    """Translate a product's descriptions from Czech to TARGET_LANG."""
    prompt = " ".join(prompt) if prompt else None
    client = UpgatesClient()
    try:
        asyncio.run(client.translate_product(product_code, target_lang, prompt))
    except ValueError as e:
        console.print(f"❌ Translation failed: {e}")
        return
    search_product.callback(product_code, "json", target_lang, False, list())
    if save:
        save_translation.callback(product_code, target_lang, update)

# CMD: Save Translation
@click.command()
@click.option("--update", is_flag=True, default=False, help="Update the product translations before saving.")
@click.argument("product_code")
@click.argument("target_lang")
def save_translation(product_code, target_lang, update):
    """Save the updated product translations back to Upgates.cz API."""
    client = UpgatesClient()
    if update:
        empty_prompt = ""
        asyncio.run(client.translate_product(product_code, target_lang, empty_prompt))
    asyncio.run(client.save_translation(product_code, target_lang))


@click.command()
@click.argument("product_code")
@click.option("--format", default="json", type=click.Choice(["yaml", "json", "df"]), help="Output format: JSON (default), TOML, or DataFrame (df).")
@click.option("--language", default="cz", help="Language code for the product mutation.")
@click.option("--embed", is_flag=True, help="Launch ipython.embed() shell after searching for product.")
@click.argument("fields", nargs=-1)
def search_product(product_code, format, language, embed, fields):
    """Search for a product by product_code.""" 
    client = UpgatesClient()
    product = asyncio.run(client.db_api.get_product_details(product_code))

    if product is None:
        console.print(f"❌ Product '{product_code}' not found.")
        return
    elif product.empty:
        console.print(f"❌ Product '{product_code}' not found.")
        return
    
    required_fields = set(['product_id', 'code', 'ean', 'descriptions'])
    fields = set(fields) if fields else required_fields
    fields |= required_fields
    fields = list(fields)
    
    #import ipdb; ipdb.set_trace()

    if fields:
        product = product.loc[:, fields]

    if 'descriptions' in fields:
        product['descriptions'] = product['descriptions'].apply(
            lambda x: [desc for desc in x if desc['language'] == language])

    if format == "df":
        msg = product.to_string(index=False)
    elif format == "json":
        msg = product.to_json(orient="records", indent=2)
    elif format == "csv":
        raise NotImplementedError("CSV output format not yet implemented.")
    elif format == "toml":
        raise NotImplementedError("TOML output format not yet implemented.")
    elif format == "yaml":
        msg = yaml.dump(product.to_dict(orient="records"), indent=2)
    else:
        msg = product.to_string(index=False)

    console.print(msg)
    
    if embed:
            IPython.embed()

@click.command(name="show-products")
@click.option("--embed", is_flag=False, default=True, help="Launch ipython.embed() shell after showing products.")
def show_products(embed):
    """Show all products with related data."""
    client = UpgatesClient()
    # Get all product details (with foreign key relationships)
    products = asyncio.run(client.db_api.get_all_products())
    
    console.print(products.to_json(orient="records", indent=2))

    if embed:
        IPython.embed()
    
    



@click.command(name="show-customers")
def show_customers():
    """Show all customers."""
    db_file = config.default_db_path
    conn = duckdb.connect(db_file)
    df = conn.execute("SELECT * FROM customers").fetchdf()
    conn.close()
    console.print(df.head())

@click.command(name="show-orders")
def show_orders():
    """Show all orders."""
    db_file = config.default_db_path
    conn = duckdb.connect(db_file)
    df = conn.execute("SELECT * FROM orders").fetchdf()
    conn.close()
    console.print(df.head())

@click.command()
def clear_cache():
    """Force-clear the DuckDB cache file."""
    db_file = config.default_db_path
    # Ensure the cache file exists before attempting to remove
    if os.path.exists(db_file):
        console.print(f"ℹ️ Cache file: {db_file}")
        try:
            os.remove(db_file)
            console.print("✅ Database cache file cleared successfully.")
        except Exception as e:
            console.print(f"❌ Failed to clear cache file: {e}")
    else:
        console.print("⚠️ Cache file does not exist.")

cli.add_command(start_webhook)
cli.add_command(start_scheduler)
cli.add_command(sync_all)
cli.add_command(sync_products)
cli.add_command(sync_customers)
cli.add_command(sync_orders)
cli.add_command(search_product)
cli.add_command(show_products)
cli.add_command(show_customers)
cli.add_command(show_orders)
cli.add_command(clear_cache)

# Register the new commands with the CLI group:
cli.add_command(translate_product)
cli.add_command(save_translation)

cli.add_command(list_product_fields)


if __name__ == "__main__":
    cli()