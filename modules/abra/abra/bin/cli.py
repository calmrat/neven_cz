#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cli.py - Abra Invoice CLI

This script provides a command-line interface for importing, searching, and migrating invoices
to and from a DuckDB database. It uses the `click` library for command-line argument parsing
and the `rich` library for console output.

Usage:
    python /Users/cward/Repos/neven_cz/modules/abra/bin/cli.py [COMMAND] [OPTIONS]

Commands:
    init_db         Initialize the DuckDB database for invoices
    import_invoices Import invoices from a single XML to DuckDB
    search_invoices Search invoices in the DuckDB database
    migrate_invoices Migrate invoices to Pohoda format (XML)

Options:
    --reset         Reset the database
    --db-path       Specify the database path
    --migrate       Migrate invoices to Pohoda format
    --embed         Embed IPython shell after operation
    --output-filename Specify the output filename for migrated invoices
    --last          Display only the last invoice

Example:
    $> abra --help
"""

import logging
import os
from pathlib import Path

import click
import IPython
from abra import config
from abra.handlers import InvoiceHandler
from rich.console import Console

logger = logging.getLogger(__name__)

# Configure Rich Console output
console = Console()

sample_input_filename = "abra/faktura_vydana-sample-1.xml"
sample_input_path = config.input_path / sample_input_filename

if not sample_input_path.exists():
    logger.error("Sample XML file not found.")
    logger.debug(f"Expected path: {sample_input_path}")
    logger.debug("Please provide a valid XML file path.")

logger.info("abra - Fully Nested Invoice Import to DuckDB")


# CLI entrypoint
@click.group()
def cli():
    "Abra Invoice Importer"
    pass


# Import invoices command
@click.command()
@click.option("--reset", is_flag=True, help="Reset the database")
@click.option(
    "db_path", "--db-path", default=config.default_db_path, help="Database path"
)
def init_db(reset, db_path):
    "Initialize the DuckDB database for invoices"
    client = InvoiceHandler(db_path)

    if (
        client.conn.execute(
            "SELECT * FROM information_schema.tables WHERE table_name = 'invoices'"
        ).fetchone()
        or client.conn.execute(
            "SELECT * FROM information_schema.tables WHERE table_name = 'invoice_items'"
        ).fetchone()
    ):
        if reset:
            client.conn.execute("DROP TABLE IF EXISTS invoices")
            client.conn.execute("DROP TABLE IF EXISTS invoice_items")
            console.print("Database reset")
        else:
            console.print("Database already initialized")
            return

    logger.info("Initializing database...")
    client.init_tables()
    logger.debug("Database initialized successfully")


# Import invoices command
@click.command()
@click.option(
    "db_path", "--db-path", default=config.default_db_path, help="Database path"
)
@click.option("--reset", is_flag=True, help="Reset the database")
@click.option("--migrate", is_flag=True, help="Migrate invoices to Pohoda format")
@click.option("--embed", is_flag=True, help="Embed IPython shell after import")
@click.argument("input-xml-path", default=sample_input_path)
def import_invoices(
    db_path: Path, reset: bool, migrate: bool, embed: bool, input_xml_path: Path
):
    "Import invoices from a single XML to DuckDB"
    # TODO: rename to import_invoices, as it imports multiple invoices
    input_xml_path = os.path.abspath(input_xml_path)

    if reset:
        init_db.callback(reset=True, db_path=db_path)

    logger.info("Starting import process...")
    logger.debug(f"Database path: {db_path}")
    logger.debug(f"Input XML: {input_xml_path}")

    xml_file = Path(input_xml_path)

    if not xml_file.exists():
        console.print("No XML file found.")
        return

    client = InvoiceHandler(db_path)
    logger.info(f"Processing {xml_file.name}...")
    client.parse_invoices(xml_file)
    client.sync_invoices()
    logger.debug("Processing is complete.")

    if migrate:
        client.migrate_invoices()
        client.save_migrated_invoices()
        logger.debug("Invoices migrated to Pohoda format.")

    if embed:
        import ipdb

        ipdb.set_trace()


# Search invoices command
@click.command()
@click.option(
    "db_path", "--db-path", default=config.default_db_path, help="Database path"
)
@click.option("--embed", is_flag=True, help="Embed IPython shell after search")
@click.option("--last", is_flag=True, help="Display only the first 1 invoices")
def search_invoices(db_path: str, embed: bool, last: bool):
    "Search invoices in the DuckDB database"
    client = InvoiceHandler(db_path)
    invoices = client.load_invoices()

    if not invoices:
        logger.error("No invoices found.")
        return

    logger.info("Invoices found:")

    start_idx = -2 if last else 0
    end_idx = -1

    if embed:
        IPython.embed()
    else:
        for invoice in invoices[start_idx:end_idx]:
            console.print(invoice.model_dump())


# Migrate invoices command
@click.command()
@click.option("--db-path", default=config.default_db_path, help="Database path")
@click.option("--embed", is_flag=True, help="Embed IPython shell after search")
@click.option("--output-filename", default=None)
def migrate_invoices(db_path: str, embed: bool, output_filename: str):
    "Migrate invoices from to Pohoda format (XML)"

    client = InvoiceHandler(db_path=db_path)
    client.migrate_invoices()
    client.save_migrated_invoices(output_filename)

    if embed:
        IPython.embed()


cli.add_command(import_invoices)
cli.add_command(init_db)
cli.add_command(search_invoices)
cli.add_command(migrate_invoices)

if __name__ == "__main__":
    cli()

# EOF
