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

import asyncio
import os
import subprocess
import sys

import click
import duckdb
import IPython
from rich.console import Console
from upgates import config
from upgates.client import UpgatesClient

# Ensure the package directory is included in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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


# CMD: Start Webhook
@click.command()
def start_webhook():
    """Start webhook server for real-time updates."""
    subprocess.run(["python", "webhook_server.py"], check=True)


# CMD: Start Scheduler
@click.command()
def start_scheduler():
    """Start scheduled auto-sync process."""
    subprocess.run(["python", "scheduler.py"], check=True)


####


@click.command()
@click.option("--reset-cache", is_flag=True, help="Clear the cache before syncing.")
@click.option(
    "--page-count",
    default=None,
    type=int,
    help="Number of pages to fetch. Default is all pages.",
)
@click.option(
    "--embed", is_flag=True, help="Launch ipython.embed() shell after syncing."
)
def sync_products(reset_cache, page_count, embed):
    """Sync products data."""

    if reset_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set

    client = UpgatesClient()
    asyncio.run(client.sync_products(page_count=page_count))

    if embed:
        IPython.embed()


@click.command()
@click.option("--reset-cache", is_flag=True, help="Clear the cache before syncing.")
@click.option(
    "--page-count",
    default=None,
    type=int,
    help="Number of pages to fetch. Default is all pages.",
)
def sync_customers(reset_cache, page_count):
    """Sync customers data."""
    if reset_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    client = UpgatesClient()
    asyncio.run(client.sync_customers(page_count=page_count))


@click.command()
@click.option("--clear-cache", is_flag=True, help="Clear the cache before syncing.")
@click.option(
    "--page-count",
    default=None,
    type=int,
    help="Number of pages to fetch. Default is all pages.",
)
def sync_orders(reset_cache, page_count):
    """Sync orders data."""
    if reset_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    client = UpgatesClient()
    asyncio.run(client.sync_orders(page_count=page_count))


@click.command(name="sync-parameters")
@click.option("--clear-cache", is_flag=True, help="Clear the cache before syncing.")
@click.option(
    "--page-count",
    default=None,
    type=int,
    help="Number of pages to fetch. Default is all pages.",
)
def sync_parameters(reset_cache, page_count):
    """Show all parameters."""
    if reset_cache:
        _clear_cache()  # Ensure clear_cache is called if the flag is set
    client = UpgatesClient()
    asyncio.run(client.sync_parameters(page_count=page_count))


# --


@click.command()
@click.option(
    "--page-count",
    default=None,
    type=int,
    help="Number of pages to fetch. Default is all pages.",
)
def sync_all():
    """Sync all data: products, customers, orders."""
    client = UpgatesClient()
    asyncio.run(client.sync_all())


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
@click.option(
    "--save",
    is_flag=True,
    default=False,
    help="Save the translation back to Upgates.cz API.",
)
def translate_product(product_code, target_lang, prompt, save):
    """Translate a product's descriptions from Czech to TARGET_LANG."""
    target_lang = target_lang.lower().strip()
    prompt = " ".join(prompt) if prompt else None
    client = UpgatesClient()

    product_codes = (
        [product_code] if "," not in product_code else product_code.split(",")
    )

    languages = [target_lang] if "," not in target_lang else target_lang.split(",")

    def translate(product_code, target_lang, prompt, save) -> None:
        """Translate product descriptions."""
        console.print(f"▶️ Translate product: {product_code}")
        asyncio.run(client.translate_product(product_code, target_lang, prompt))

        if not save:
            return

        console.print(f"💾 Saving translation for product: {product_code}")
        # Save the translation back to Upgates.cz API but avoid updating the product again
        asyncio.run(client.save_translation(product_code, target_lang))

    _ = [
        translate(code, lang, "", save) for code in product_codes for lang in languages
    ]
    console.print(
        f"✅ Translations completed. \nLanguages: {languages}\nProduct Codes: {product_codes}"
    )


# CMD: Save Translation
@click.command()
@click.option(
    "--update",
    is_flag=False,
    default=False,
    help="Update the product translations before saving.",
)
@click.argument("product_code")
@click.argument("target_lang")
def save_translation(product_code, target_lang, update):
    """Save the updated product translations back to Upgates.cz API."""
    client = UpgatesClient()
    if update:
        empty_prompt = ""
        asyncio.run(client.translate_product(product_code, target_lang, empty_prompt))
    asyncio.run(client.save_translation(product_code, target_lang))


async def save_product_translation(
    client: UpgatesClient, code: str, target_lang: str
) -> list:
    """bla bla"""
    groups = []
    async with asyncio.TaskGroup() as tg:
        tg.create_task(client.translate_product(code, target_lang, ""))
        tg.create_task(client.save_translation(code, target_lang))
        groups.append(tg)
    return groups


async def save_product_translations(target_lang: str) -> None:
    """Async wrapper to batch save product translations."""
    target_lang = target_lang.lower()
    client = UpgatesClient()
    codes = await client.db_api.get_all_product_codes()

    chunk_size = 10
    chunks = [codes[x : x + chunk_size] for x in range(0, len(codes), chunk_size)]

    async def save(code, target_lang):
        async with asyncio.TaskGroup() as tg:
            query = """
            SELECT 1 FROM descriptions AS d 
                WHERE 
                    d.product_id = (SELECT p.product_id from products AS p WHERE p.code = ?) 
                    AND 
                    d.language = ?
                    AND 
                    d.long_description IS NOT NULL
                    AND 
                    d.long_description <> ''
            """.strip()

            exists = client.db_api.conn.execute(query, [code, target_lang]).fetchone()

            if exists:
                print(f"☑️ Skipped: {code}")
                return

            try:
                await client.translate_product(code, target_lang, "")
            except AttributeError:
                console.print(f"❌ Translation failed: {code}")
                return
            else:
                tg.create_task(client.save_translation(code, target_lang))

    for chunk in chunks:
        tasks = list()
        for code in chunk:
            if "X" in code:
                console.print(f"❌ Skip: {code}")
                continue
            tasks.append(save(code, target_lang))
        await asyncio.gather(*tasks)


# CMD: Save all translations
@click.command()
@click.argument("target_lang")
def save_all_translations(target_lang: str):
    """Save all product translations back to Upgates.cz API."""
    asyncio.run(save_product_translations(target_lang))


@click.command()
@click.argument("product_code")
@click.option(
    "--language", default="cz", help="Language code for the product mutation."
)
@click.option(
    "--embed",
    is_flag=True,
    help="Launch ipython.embed() shell after searching for product.",
)
@click.argument("fields", nargs=-1)
def search_product(product_code, language, embed, fields):
    """Search for a product by product_code."""
    client = UpgatesClient()
    product = asyncio.run(client.db_api.get_product_details(product_code))

    if product is None:
        console.print(f"❌ Product '{product_code}' not found.")
        return
    elif product.empty:
        console.print(f"❌ Product '{product_code}' not found.")
        return

    required_fields = set(["product_id", "code", "ean", "descriptions"])
    fields = set(fields) if fields else required_fields
    fields |= required_fields
    fields = list(fields)

    if fields:
        product = product.loc[:, fields]

    if "descriptions" in fields:
        product["descriptions"] = product["descriptions"].apply(
            lambda x: [desc for desc in x if desc["language"] == language]
        )

    msg = product.to_json(orient="records", indent=2)
    console.print(msg)

    if embed:
        IPython.embed()


@click.command(name="show-products")
@click.option(
    "--embed",
    is_flag=False,
    default=True,
    help="Launch ipython.embed() shell after showing products.",
)
def show_products(embed):
    """Show all products with related data."""
    client = UpgatesClient()
    # Get all product details (with foreign key relationships)
    products = asyncio.run(client.db_api.get_all_products())

    console.print(products[0])

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


@click.command(name="show-parameters")
def show_parameters():
    """Show all parameters."""
    db_file = config.default_db_path
    conn = duckdb.connect(db_file)
    df = conn.execute("SELECT * FROM parameters").fetchdf()
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
        except RuntimeError as e:
            console.print(f"❌ Failed to clear cache file: {e}")
    else:
        console.print("⚠️ Cache file does not exist.")


cli.add_command(start_webhook)
cli.add_command(start_scheduler)
cli.add_command(sync_all)
cli.add_command(sync_products)
cli.add_command(sync_customers)
cli.add_command(sync_orders)
cli.add_command(sync_parameters)
cli.add_command(search_product)
cli.add_command(show_products)
cli.add_command(show_customers)
cli.add_command(show_parameters)
cli.add_command(show_orders)
cli.add_command(clear_cache)

# Register the new commands with the CLI group:
cli.add_command(translate_product)
cli.add_command(save_translation)
cli.add_command(save_all_translations)

cli.add_command(list_product_fields)


if __name__ == "__main__":
    cli()
