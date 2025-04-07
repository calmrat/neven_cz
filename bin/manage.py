#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manage.py v0.1.0
File: manage.py

This script provides CLI for managing the Neven.cz Project.
- creating a ZIP archive of the current Git repository.
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List

import click
import dotenv


def expand_home(path) -> Path:
    """
    Expand the ~ symbol to the full path of the user's home directory.

    :param path: A string path that may contain a ~ symbol.
    :return: A string path with the ~ symbol expanded to the user's home directory.
    """
    return Path(os.path.expanduser(Path(path)))


def make_dirs(paths: List[Path]) -> int:
    """
    Create directories for each path in the list of paths.

    :param paths: A list of Path objects.
    """
    click.echo(f"Creating directories: {paths}")
    for path in paths:
        if path.exists():
            click.echo(f"Directory already exists: {path}")
            continue
        try:
            path.mkdir(parents=True, exist_ok=True)
            click.echo(f"Directory created: {path}")
            return 0
        except Exception as e:
            click.echo(f"Failed to create directory {path}: {e}", err=True)
            return 1


# Load environment variables from .env file
env_path = Path(os.path.join(os.path.dirname(__file__), "../.env"))
dotenv.load_dotenv(dotenv_path=env_path)

# Get the value of NEVEN_PATH from the environment
neven_path = expand_home(os.getenv("NEVEN_PATH"))

data_path = neven_path / Path("data")
output_path = data_path / Path("output")
repo_archive_path = output_path / Path("repo_archive")

sys_paths = [neven_path, data_path, repo_archive_path, output_path]

# Create directories if they do not exist
make_dirs(sys_paths)


# import abra
# import upgates
@click.group()
def cli():
    pass


@click.command()
@click.option(
    "--output-path", default=repo_archive_path, help="Output path for the ZIP file."
)
@click.option(
    "--output-filename",
    default=f"neven_cz-{datetime.now().strftime('%d%m%y%H%M%S')}.zip",
    help="Output ZIP file name.",
)
def zip_repo(output_path, output_filename):
    """
    Create a ZIP archive of the current Git repository.

    This command uses "git archive" to package all tracked files from the current HEAD into a ZIP file.
    Files listed in .gitignore or untracked files are excluded.
    """
    path = Path(output_path) / output_filename
    try:
        subprocess.run(
            ["git", "archive", "--format=zip", "--output", path, "HEAD"], check=True
        )
        click.echo(f"Repository archived successfully to {path}")
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to archive repository: {e}", err=True)


cli.add_command(zip_repo)

if __name__ == "__main__":
    cli()
