#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
installer.py

This script automates the process of setting up a Python project from a GitHub repository.
It can create a virtual environment, install dependencies, and optionally build the project using Poetry.

Usage:
    python installer.py

The script will prompt for the following inputs:
    - GitHub repository URL
    - Installation path
    - Whether to create a new virtual environment
    - Whether to install with development dependencies
    - Whether to build the project with Poetry

Relative path/filename:
    /Users/cward/Repos/neven_cz/bin/installer.py
"""

import os
import subprocess
import venv


def run_command(command):
    result = subprocess.run(
        command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return result.stdout.decode("utf-8")


def create_virtualenv(path):
    venv.create(path, with_pip=True)
    activate_script = os.path.join(path, "bin", "activate")
    return activate_script


def install_uv(activate_script, dev=False):
    pip_command = f"source {activate_script} && pip install -e ."
    if dev:
        pip_command += "[dev]"
    run_command(pip_command)


def download_repo(github_url, path):
    run_command(f"git clone {github_url} {path}")


def build_poetry(path):
    run_command(f"cd {path} && poetry build")


def main():
    github_url = input("Enter the GitHub repository URL: ")
    install_path = input("Enter the installation path: ")
    create_venv = (
        input("Do you want to create a new virtual environment? (yes/no): ").lower()
        == "yes"
    )
    dev_install = (
        input("Do you want to install with dev dependencies? (yes/no): ").lower()
        == "yes"
    )
    build_poetry_option = (
        input("Do you want to build with poetry? (yes/no): ").lower() == "yes"
    )

    download_repo(github_url, install_path)

    if create_venv:
        venv_path = os.path.join(install_path, "venv")
        activate_script = create_virtualenv(venv_path)
    else:
        activate_script = os.path.join(install_path, "bin", "activate")

    install_uv(activate_script, dev=dev_install)

    if build_poetry_option:
        build_poetry(install_path)


if __name__ == "__main__":
    main()
