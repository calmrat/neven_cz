#!/usr/bin/env python3
"""
config.py

Loads configuration settings from a TOML file or sets default values.
"""

import os
import toml

CONFIG_PATH = os.getenv("CONFIG_PATH", ".config/upgates/config.toml")
CONFIG_PATH_2 = os.getenv("CONFIG_PATH", "./.config/config.toml")

if os.path.exists(CONFIG_PATH):
    config = toml.load(CONFIG_PATH)
elif os.path.exists(CONFIG_PATH_2):
    config = toml.load(CONFIG_PATH_2)
else:
    # Default configuration if no config file exists.
    config = {
        "database": {
            "cache_path": ".data/cache",
            "data_path": ".data"
        },
        "upgates": {
            "api_url": "https://api.upgates.cz",
            "login": "your_login",
            "api_key": "your_api_key"
        },
        "api": {
            "verify_ssl": True,
            "retry_attempts": 3,
            "parallel_batches": 1
        },
        "logging": {
            "log_level": "info"
        }
    }