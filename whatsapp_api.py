import os
import requests


WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

GRAPH_URL = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"


def send_message(to, message):
    """
    Send a normal text message through WhatsApp Cloud API.
    """

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
        GRAPH_URL,
        headers=headers,
        json=payload
    )

    print("📤 SEND MESSAGE RESPONSE")
    print(response.status_code)
    print(response.text)

    return response.status_code == 200


# =====================================
# FIRST BUTTON
# =====================================

def send_reply_buttons(to, customer_name, table, returning=False):

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    if returning:
        body_text = (
            f"👋 Welcome back, {customer_name}!\n\n"
            f"📍 Table: {table}\n\n"
            "Ready to order?"
        )
    else:
        body_text = (
            f"👋 Welcome, {customer_name}!\n\n"
            f"📍 Table: {table}\n\n"
            "Ready to order?"
        )

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",

            "body": {
                "text": body_text
            },

            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "VIEW_MENU",
                            "title": "🍽 View Menu"
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(
        GRAPH_URL,
        headers=headers,
        json=payload
    )

    print("📤 SEND VIEW MENU BUTTON RESPONSE")
    print(response.status_code)
    print(response.text)

    return response.status_code == 200

def send_category_buttons(to):

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",

            "body": {
                "text": "🍽 Please choose a category:"
            },

            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "CATEGORY_MANDI",
                            "title": "🍗 Mandi"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "CATEGORY_SHAWARMA",
                            "title": "🌯 Shawarma"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "CATEGORY_DRINKS",
                            "title": "🥤 Drinks"
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(
        GRAPH_URL,
        headers=headers,
        json=payload
    )

    print("📤 SEND CATEGORY BUTTONS RESPONSE")
    print(response.status_code)
    print(response.text)

    return response.status_code == 200
    print("📤 SEND CATEGORY BUTTONS RESPONSE")
    print(response.status_code)
    print(response.text)

    return response.status_code == 200


def send_mandi_buttons(to):

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "interactive",
        "interactive": {
            "type": "button",
            "body": {
                "text": "🍗 Please choose your Mandi:"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "1",
                            "title": "🍗 Chicken Mandi ₹499"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "2",
                            "title": "🍖 Mutton Mandi ₹699"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "3",
                            "title": "🐟 Fish Mandi ₹599"
                        }
                    }
                ]
            }
        }
    }

    response = requests.post(
        GRAPH_URL,
        headers=headers,
        json=payload
    )

    print("📤 SEND MANDI BUTTONS RESPONSE")
    print(response.status_code)
    print(response.text)

    return response.status_code == 200