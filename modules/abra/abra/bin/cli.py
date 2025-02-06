# abra v0.1.0.0 - Fully Nested Invoice Import to DuckDB

import os
import click
from rich.console import Console
import IPython

from pathlib import Path

from abra.config import input_path, sample_db_path
from abra.handlers import InvoiceHandler


# Configure logging
console = Console()

sample_input_filename = "faktura_vydana-leden_2025.xml"
sample_input_path = input_path / sample_input_filename

# CLI entrypoint
@click.group()
def cli():
    "Abra Invoice Importer"
    pass

# Import invoices command
@click.command()
@click.option("--reset", is_flag=True, help="Reset the database")
@click.option("db_path", "--db-path", default=sample_db_path, help="Database path")
def init_db(reset, db_path):
    "Initialize the DuckDB database for invoices"
    client = InvoiceHandler(db_path)
    
    if client.conn.execute("SELECT * FROM information_schema.tables WHERE table_name = 'invoices'").fetchone():
        if reset:
            client.conn.execute("DROP TABLE IF EXISTS invoices")
            console.print("[bold yellow]Database reset[/bold yellow]")
        else:
            console.print("[yellow]Database already initialized[/yellow]")
            return

    console.print("[bold green]Initializing database...[/bold green]")
    client.init_tables()
    console.print("[green]Database initialized successfully[/green]")

# Import invoices command
@click.command()
@click.option("db_path", "--db-path", default=sample_db_path, help="Database path")
@click.argument(
    "input-xml-path",
    default=sample_input_path
)
def import_invoice(db_path: Path, input_xml_path: Path):
    "Import invoices from a single XML to DuckDB"
    # TODO: rename to import_invoices, as it imports multiple invoices 
    input_xml_path = os.path.abspath(input_xml_path)

    console.print("[bold green]Starting import process...[/bold green]")
    console.print(f"[bold]Database path:[/bold] {db_path}")
    console.print(f"[bold]Input XML:[/bold] {input_xml_path}")

    xml_file = Path(input_xml_path)

    if not xml_file.exists():
        console.print("[bold red]No XML file found.[/bold red]")
        return

    client = InvoiceHandler(db_path)
    console.print(f"[blue]Processing {xml_file.name}...[/blue]")
    client.parse_invoices(xml_file)
    client.sync_invoices()
    console.print(f"[green]Processing is complete.[/green]")

    import ipdb; ipdb.set_trace()

# Search invoices command
@click.command()
@click.option("db_path", "--db-path", default=sample_db_path, help="Database path")
@click.option("--embed", is_flag=True, help="Embed IPython shell after search")
def search_invoices(db_path: str, embed: bool):
    "Search invoices in the DuckDB database"
    client = InvoiceHandler(db_path)
    invoices = client.load_invoices()
    
    if not invoices:
        console.print("[bold red]No invoices found.[/bold red]")
        return

    console.print("[bold green]Invoices found:[/bold green]")
    
    if embed:
        IPython.embed()
    else:
        for invoice in invoices:
            console.print(invoice.model_dump())

# Migrate invoices command
@click.command()
@click.option("db_path", "--db-path", default=sample_db_path, help="Database path")
@click.option("--embed", is_flag=True, help="Embed IPython shell after search")
def migrate_invoices(db_path: str, embed: bool):
    "Migrate invoices from to Pohoda format (XML)"
    client = InvoiceHandler(db_path)    
    client.migrate_invoices()
    if embed:
        IPython.embed()


cli.add_command(import_invoice)
cli.add_command(init_db)
cli.add_command(search_invoices)
cli.add_command(migrate_invoices)

if __name__ == "__main__":
    cli()
