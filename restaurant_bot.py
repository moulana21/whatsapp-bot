from flask import Flask, request
from dotenv import load_dotenv
import requests
import os
import random

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

users = {}

MENU = {
    "1": {"name": "Chicken Biryani", "price": 250},
    "2": {"name": "Mutton Biryani", "price": 350},
    "3": {"name": "Shawarma", "price": 120}
}


@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return "ok", 200

        message = value["messages"][0]

        sender = message["from"]

        if "text" not in message:
            return "ok", 200

        text = message["text"]["body"].strip()

        handle_message(sender, text)

    except Exception as e:
        print("ERROR:", str(e))

    return "ok", 200


def handle_message(sender, text):

    text_lower = text.lower()

    if sender not in users:
        users[sender] = {
            "step": "name"
        }

        send_message(
            sender,
            "👋 Welcome to Mandi House\n\nMay I know your name?"
        )
        return

    user = users[sender]

    if user["step"] == "name":

        user["name"] = text
        user["step"] = "menu"

        send_message(
            sender,
            f"""🍽 Welcome {text}

Mandi House Menu

1. Chicken Biryani - ₹250
2. Mutton Biryani - ₹350
3. Shawarma - ₹120

Reply with item number or item name."""
        )
        return

    if text_lower in ["hi", "hello", "menu"]:

        user["step"] = "menu"

        send_message(
            sender,
            f"""🍽 Welcome back {user['name']}

1. Chicken Biryani - ₹250
2. Mutton Biryani - ₹350
3. Shawarma - ₹120

Reply with item number or item name."""
        )
        return

    if user["step"] == "quantity":

        selected = None

        if text in MENU:
            selected = MENU[text]

        elif text_lower == "chicken biryani":
            selected = MENU["1"]

        elif text_lower == "mutton biryani":
            selected = MENU["2"]

        elif text_lower == "shawarma":
            selected = MENU["3"]

        if selected:

            user["item"] = selected["name"]
            user["price"] = selected["price"]
            user["step"] = "quantity"

            send_message(sender, "🍽 How many plates?")
            return

    if user["step"] == "quantity":

        if text.isdigit():

            qty = int(text)

            if qty <= 0:
                send_message(sender, "Please enter a valid quantity.")
                return

            subtotal = qty * user["price"]
            gst = round(subtotal * 0.05, 2)
            total = subtotal + gst

            user["qty"] = qty
            user["subtotal"] = subtotal
            user["gst"] = gst
            user["total"] = total
            user["step"] = "confirm"

            send_message(
                sender,
                f"""✅ Order Summary

{user['item']} x {qty}

Subtotal: ₹{subtotal}
GST (5%): ₹{gst}
Total Bill: ₹{total}

Reply CONFIRM to place order."""
            )
            return

    if user["step"] == "confirm":

        if text_lower == "confirm":

            order_id = f"MH{random.randint(1000,9999)}"

            send_message(
                sender,
                f"""🎉 Order Confirmed

Order ID: {order_id}

Customer: {user['name']}
Item: {user['item']}
Quantity: {user['qty']}

Subtotal: ₹{user['subtotal']}
GST: ₹{user['gst']}
Total: ₹{user['total']}

Thank you for ordering ❤️"""
            )

            user["step"] = "menu"
            return

    send_message(
        sender,
        "Send HI to start ordering."
    )


def send_message(to, message):

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print(response.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)