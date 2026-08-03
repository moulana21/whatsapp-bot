from flask import Flask, request
from whatsapp_api import (
    send_message,
    send_reply_buttons
)
import os

from config import HOST, PORT, DEBUG, RESTAURANT_NAME
from database import init_database
from menu import get_menu_text
from restaurant_engine import process_message

# -----------------------------
# Create Flask App
# -----------------------------
app = Flask(__name__)

# -----------------------------
# Initialize Database
# -----------------------------
init_database()

# -----------------------------
# Verify Token
# -----------------------------
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "12345")

# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return {
        "status": "running",
        "project": f"{RESTAURANT_NAME} Restaurant Bot V3",
        "database": "Connected"
    }

# -----------------------------
# Menu Route
# -----------------------------
@app.route("/menu")
def menu():
    return {
        "menu": get_menu_text()
    }

# -----------------------------
# Chat Test Route
# -----------------------------
@app.route("/chat")
def chat():

    phone = request.args.get("phone")
    message = request.args.get("message")

    if not phone or not message:
        return {
            "error": "phone and message required"
        }, 400

    reply = process_message(phone, message)

    return {
        "reply": reply
    }

# -----------------------------
# WhatsApp Webhook Verification
# -----------------------------
@app.route("/webhook", methods=["GET"])
def verify():

    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook Verified")
        return challenge, 200

    return "Verification failed", 403

# -----------------------------
# WhatsApp Incoming Messages
# -----------------------------
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    print("\n==========================")
    print("FULL WEBHOOK PAYLOAD")
    print(data)
    print("==========================")

    try:
        value = data["entry"][0]["changes"][0]["value"]

        # Incoming User Message
        if "messages" in value:

            msg = value["messages"][0]

            sender = msg["from"]
            text = msg["text"]["body"]

            print("✅ USER MESSAGE RECEIVED")
            print("From :", sender)
            print("Text :", text)
           # Process message
            reply = process_message(sender, text)

           # Send WhatsApp reply

        if reply == "SHOW_MENU_BUTTON":
           send_reply_buttons(sender)
        else:
          send_message(sender, reply)

        # Status Updates
        if "statuses" in value:

            print("ℹ️ STATUS UPDATE")
            print(value["statuses"][0]["status"])

    except Exception as e:
        print("❌ ERROR:", e)

    return "OK", 200

# -----------------------------
# Print Routes
# -----------------------------
print("\n========== REGISTERED ROUTES ==========")

for rule in app.url_map.iter_rules():
    print(rule)

print("=======================================\n")

# -----------------------------
# Start Server
# -----------------------------
if __name__ == "__main__":

    print("🚀 Starting Restaurant Bot V3...")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )