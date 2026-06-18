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

customers = {}
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
        text = message["text"]["body"].strip()

        handle_message(sender, text)

    except Exception as e:
        print("Error:", e)

    return "ok", 200


def show_menu(sender, customer_name):
    send_message(
        sender,
        f"""🍽 Welcome {customer_name}

1. Chicken Biryani - ₹250
2. Mutton Biryani - ₹350
3. Shawarma - ₹120

Reply with item number."""
    )


def handle_message(sender, text):

    lower_text = text.lower()

    if sender not in customers:

        if lower_text == "hi":
            customers[sender] = {"waiting_name": True}

            send_message(
                sender,
                "👋 Welcome to Royal Grand Restaurant\n\nMay I know your name?"
            )

            return

        elif customers.get(sender, {}).get("waiting_name"):

            pass

    if sender in customers and customers[sender].get("waiting_name"):

        customers[sender]["name"] = text
        customers[sender]["waiting_name"] = False

        show_menu(sender, text)
        return

    if lower_text == "hi":

        if sender in customers:

            customer_name = customers[sender]["name"]

            if sender in orders:

                last_order = orders[sender].get("item", "No previous order")

                send_message(
                    sender,
                    f"""👋 Welcome back {customer_name}

Last Order:
{last_order}

Would you like to order again?

1. Chicken Biryani - ₹250
2. Mutton Biryani - ₹350
3. Shawarma - ₹120"""
                )

            else:
                show_menu(sender, customer_name)

        return

    elif text in MENU:

        orders[sender] = {
            "item": MENU[text]["name"],
            "price": MENU[text]["price"]
        }

        send_message(sender, "How many plates?")
        return

    elif sender in orders and text.isdigit():

        qty = int(text)

        item = orders[sender]["item"]
        price = orders[sender]["price"]

        subtotal = qty * price
        gst = round(subtotal * 0.05, 2)
        total = round(subtotal + gst, 2)

        orders[sender]["qty"] = qty
        orders[sender]["subtotal"] = subtotal
        orders[sender]["gst"] = gst
        orders[sender]["total"] = total

        send_message(
            sender,
            f"""✅ Order Summary

{item} x {qty}

Subtotal: ₹{subtotal}
GST (5%): ₹{gst}
Total Bill: ₹{total}

Reply CONFIRM to place order."""
        )

        return

    elif lower_text == "confirm":

        if sender in orders:

            order = orders[sender]

            order_id = f"RG{random.randint(1000,9999)}"

            send_message(
                sender,
                f"""🎉 Order Confirmed

Order ID: {order_id}

Item: {order['item']}
Quantity: {order['qty']}

Subtotal: ₹{order['subtotal']}
GST: ₹{order['gst']}
Total: ₹{order['total']}

Thank you for ordering ❤️"""
            )

        return

    send_message(sender, "Send HI to start ordering.")


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