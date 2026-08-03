import os
import requests

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")


def send_message(to, message):
    """
    Send a text message through WhatsApp Cloud API
    """

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

    print("📤 SEND MESSAGE RESPONSE")
    print(response.status_code)
    print(response.text)

    return response.status_code == 200
    # =====================================
# SEND REPLY BUTTONS
# =====================================

def send_reply_buttons(to):

    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"

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
                "text": "🙏 Welcome to Mandi House ❤️\n\nTap below to view our menu."
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
        url,
        headers=headers,
        json=payload
    )

    print("📤 SEND BUTTON RESPONSE")
    print(response.status_code)
    print(response.text)

    return response.status_code == 200