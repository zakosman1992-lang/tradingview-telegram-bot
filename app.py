from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN environment variable is missing")


@app.route("/", methods=["GET"])
def home():
    return "Bot is running", 200


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if WEBHOOK_SECRET and data.get("secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    chat_id = data.get("chat_id")
    text = data.get("text")

    if not chat_id or not text:
        return jsonify({"error": "chat_id and text are required"}), 400

    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    response = requests.post(
        telegram_url,
        json={"chat_id": chat_id, "text": text},
        timeout=10,
    )

    return jsonify({
        "status": "ok",
        "telegram_status": response.status_code
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
