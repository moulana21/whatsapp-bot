from flask import Flask, request
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Store customer orders
orders = {}

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
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]

        sender = message["from"]
        text = message["text"]["body"].strip().lower()

        handle_message(sender, text)

    except Exception as e:
        print("Error:", e)

    return "ok", 200


def handle_message(sender, text):

    if text == "hi":
        send_message(
            sender,
            """🍽 Welcome to Royal Grand Restaurant

1. Chicken Biryani - ₹250
2. Mutton Biryani - ₹350
3. Shawarma - ₹120

Reply with item number."""
        )

    elif text in MENU:

        orders[sender] = {
            "item": MENU[text]["name"],
            "price": MENU[text]["price"]
        }

        send_message(sender, "How many plates?")

    elif sender in orders and text.isdigit():

        qty = int(text)

        item = orders[sender]["item"]
        price = orders[sender]["price"]

        total = qty * price

        orders[sender]["qty"] = qty
        orders[sender]["total"] = total

        send_message(
            sender,
            f"""✅ Order Summary

{item} x {qty}

Total: ₹{total}

Reply CONFIRM to place order."""
        )

    elif text == "confirm":

        order = orders.get(sender)

        if order:
            send_message(
                sender,
                f"""🎉 Order Confirmed

Item: {order['item']}
Quantity: {order['qty']}
Total: ₹{order['total']}

Order ID: RG1001

Thank you for ordering."""
            )

    else:
        send_message(sender, "Send HI to see menu.")


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