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
@click.argument("product_code")
@click.argument("target_lang")
def translate_product(product_code, target_lang):
    """Translate a product's descriptions from Czech to TARGET_LANG."""
    asyncio.run(client.translate_product(product_code, target_lang))

@click.command()
@click.argument("product_code")
@click.argument("target_lang")
@click.argument("update")
def save_translation(product_code, target_lang, update):
    """Save the updated product translations back to Upgates.cz API."""

    if update:
        asyncio.run(client.translate_product(product_code, target_lang))
    asyncio.run(client.save_translation(product_code, target_lang))

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
@click.option('--embed', is_flag=True, help="Launch ipython.embed() shell after syncing.")
def sync_products(clear_cache, page_count, embed):
    """Sync products data."""
    
    if clear_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    asyncio.run(client.sync_products(page_count=page_count))
    
    if embed:
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
cli.add_command(init_config)
cli.add_command(search_product)
cli.add_command(show_products)
cli.add_command(show_customers)
cli.add_command(show_orders)
cli.add_command(clear_cache)

# Register the new commands with the CLI group:
cli.add_command(translate_product)
cli.add_command(save_translation)


if __name__ == "__main__":
    cli()