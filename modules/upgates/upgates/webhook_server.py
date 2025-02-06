
from flask import Flask, request, jsonify
import asyncio
from upgates.upgates_client import UpgatesClient

app = Flask(__name__)
client = UpgatesClient()

@app.route('/webhook', methods=['POST'])
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

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
