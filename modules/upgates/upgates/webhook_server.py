#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Webhook Server for Upgates Integration

This module sets up a Flask server to handle webhooks from Upgates. It listens for
real-time updates and triggers appropriate synchronization tasks based on the event type.

Usage:
    Run this script to start the webhook server:
    $ python /Users/cward/Repos/neven_cz/modules/upgates/upgates/webhook_server.py

Routes:
    /webhook (POST): Endpoint to receive webhook events from Upgates.

Event Types:
    - product.updated: Triggers product synchronization.
    - customer.updated: Triggers customer synchronization.
    - order.updated: Triggers order synchronization.
"""

from flask import Flask, request, jsonify
import asyncio
from upgates.client import UpgatesClient

app = Flask(__name__)
client = UpgatesClient()


@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook for real-time Upgates updates."""
    data = request.json
    print(f"🔔 Webhook received: {data}")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
