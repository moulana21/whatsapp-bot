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
    "1": {"name": "Chicken Mandi", "price": 499},
    "2": {"name": "Mutton Mandi", "price": 699},
    "3": {"name": "Fish Mandi", "price": 599},
    "4": {"name": "Shawarma", "price": 120}
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

        if "text" not in message:
            return "ok", 200

        sender = message["from"]
        text = message["text"]["body"].strip()

        handle_message(sender, text)

    except Exception as e:
        print("ERROR:", e)

    return "ok", 200


def handle_message(sender, text):

    text_lower = text.lower()

    if sender not in users:

        users[sender] = {
            "step": "name"
        }

        send_message(
            sender,
            "🙏 Namaste!\n\nWelcome to Mandi House ❤️\n\nMay I know your name?"
        )
        return

    user = users[sender]

    if user["step"] == "name":

        user["name"] = text
        user["step"] = "menu"

        send_menu(sender, user["name"])
        return

    if text_lower in ["hi", "hello", "menu"]:

        user["step"] = "menu"
        send_menu(sender, user["name"])
        return

    if user["step"] == "menu":

    items = [x.strip() for x in text.split(",")]

    valid = True
    selected_items = []

    for item_no in items:
        if item_no not in MENU:
            valid = False
            break

        selected_items.append(MENU[item_no])

    if not valid:
        send_message(
            sender,
            "😄 Please select a valid menu number (1-4)."
        )
        return

    user["selected_items"] = selected_items
    user["step"] = "quantity"

    item_names = "\n".join(
        [f"• {item['name']}" for item in selected_items]
    )

    send_message(
        sender,
        f"""🍽 Selected Items:

{item_names}

How many plates of each item would you like?

Example:
2"""
    )
    return
            return

        send_message(
            sender,
            "😄 Please select a valid menu number (1-4)."
        )
        return

    if user["step"] == "quantity":

        if text.isdigit():

            qty = int(text)

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
                f"""✅ ORDER SUMMARY

🍽 Item: {user['item']}
📦 Quantity: {qty}

💰 Subtotal: ₹{subtotal}
🧾 GST (5%): ₹{gst}
💵 Total: ₹{total}

Reply:
CONFIRM
or
CANCEL"""
            )
            return

        send_message(sender, "Please enter a valid quantity.")
        return

    if user["step"] == "confirm":

        if text_lower == "confirm":

            order_id = f"MH{random.randint(1000,9999)}"

            send_message(
                sender,
                f"""🎉 ORDER CONFIRMED

🆔 Order ID: {order_id}

👤 Customer: {user['name']}
🍽 Item: {user['item']}
📦 Quantity: {user['qty']}

💵 Total: ₹{user['total']}

Thank you for ordering ❤️"""
            )

            user["step"] = "menu"
            return

        if text_lower == "cancel":

            user["step"] = "menu"

            send_message(
                sender,
                "❌ Order cancelled.\n\nType MENU to order again."
            )
            return

    send_message(sender, "Type MENU to view menu.")


send_menu(sender, user["name"])

    send_message(
        sender,
        f"""🙏 Welcome {name}

🍽 MANDI HOUSE MENU

1️⃣ Chicken Mandi - ₹499
2️⃣ Mutton Mandi - ₹699
3️⃣ Fish Mandi - ₹599
4️⃣ Shawarma - ₹120

Reply with menu number."""
    )


def send_message(to, message):

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
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
        json=payload
    )

    print(response.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)