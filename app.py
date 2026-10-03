from flask import Flask, request
import os

from flow_crypto import decrypt_request, encrypt_response

from whatsapp_api import (
    send_message,
    send_reply_buttons,
    send_category_buttons,
    send_mandi_buttons
)

from config import (
    HOST,
    PORT,
    DEBUG,
    RESTAURANT_NAME
)

from database import init_database
from menu import get_menu_text

from restaurant_engine import (
    process_message,
    SESSIONS
)


# =====================================
# CREATE FLASK APP
# =====================================

app = Flask(__name__)


# =====================================
# INITIALIZE DATABASE
# =====================================

init_database()


# =====================================
# VERIFY TOKEN
# =====================================

VERIFY_TOKEN = os.getenv(
    "VERIFY_TOKEN",
    "12345"
)


# =====================================
# HOME ROUTE
# =====================================

@app.route("/")
def home():

    return {
        "status": "running",
        "project": f"{RESTAURANT_NAME} Restaurant Bot V3",
        "database": "Connected"
    }


# =====================================
# MENU ROUTE
# =====================================

@app.route("/menu")
def menu():

    return {
        "menu": get_menu_text()
    }


# =====================================
# CHAT TEST ROUTE
# =====================================

@app.route("/chat")
def chat():

    phone = request.args.get("phone")
    message = request.args.get("message")

    if not phone or not message:

        return {
            "error": "phone and message required"
        }, 400

    reply = process_message(
        phone,
        message
    )

    return {
        "reply": reply
    }


# =====================================
# WHATSAPP WEBHOOK VERIFICATION
# =====================================

@app.route(
    "/webhook",
    methods=["GET"]
)
def verify():

    mode = request.args.get(
        "hub.mode"
    )

    token = request.args.get(
        "hub.verify_token"
    )

    challenge = request.args.get(
        "hub.challenge"
    )

    if (
        mode == "subscribe"
        and token == VERIFY_TOKEN
    ):

        print("✅ Webhook Verified")

        return challenge, 200

    return "Verification failed", 403


# =====================================
# WHATSAPP INCOMING MESSAGES
# =====================================

@app.route(
    "/webhook",
    methods=["POST"]
)
def webhook():

    data = request.get_json()

    print("\n==========================")
    print("FULL WEBHOOK PAYLOAD")
    print(data)
    print("==========================")

    try:

        value = data[
            "entry"
        ][0][
            "changes"
        ][0][
            "value"
        ]

        # =================================
        # INCOMING MESSAGE
        # =================================

        if "messages" in value:

            msg = value[
                "messages"
            ][0]

            sender = msg["from"]

            # -----------------------------
            # NORMAL TEXT MESSAGE
            # -----------------------------

            if "text" in msg:

                text = msg[
                    "text"
                ]["body"]

            # -----------------------------
            # INTERACTIVE BUTTON
            # -----------------------------

            elif "interactive" in msg:

                interactive = msg[
                    "interactive"
                ]

                if (
                    interactive.get("type")
                    == "button_reply"
                ):

                    text = interactive[
                        "button_reply"
                    ]["id"]

                else:

                    return "OK", 200

            # -----------------------------
            # UNSUPPORTED MESSAGE
            # -----------------------------

            else:

                return "OK", 200

            print(
                "✅ USER MESSAGE RECEIVED"
            )

            print(
                "From :",
                sender
            )

            print(
                "Text :",
                text
            )

            # =================================
            # PROCESS MESSAGE
            # =================================

            reply = process_message(
                sender,
                text
            )

            print(
                "🤖 BOT REPLY :",
                reply
            )

            # =================================
            # GET CUSTOMER SESSION
            # =================================

            session = SESSIONS.get(
                sender
            )

            # =================================
            # SHOW CUSTOMER WELCOME BUTTON
            # =================================

            if reply in ["SHOW_MENU_BUTTON", "SHOW_RETURNING_MENU_BUTTON"]:

                if not session:

                    send_message(
                        sender,
                        "Please scan the QR code again."
                    )

                    return "OK", 200

                customer_name = session.get(
                    "customer_name",
                    "Guest"
                )

                table = session.get(
                    "table",
                    "Unknown"
                )

                send_reply_buttons(
                  sender,
                  customer_name,
                   table,
                  returning=(reply == "SHOW_RETURNING_MENU_BUTTON")
)

            # =================================
            # SHOW CATEGORY BUTTONS
            # =================================

            elif reply == "SHOW_CATEGORY_BUTTONS":

                send_category_buttons(
                    sender
                )
            elif reply == "SHOW_MANDI_MENU":

                 send_mandi_buttons(
                    sender
                ) 
            # =================================
            # NORMAL TEXT REPLY
            # =================================

            else:

                send_message(
                    sender,
                    reply
                )

        # =================================
        # STATUS UPDATE
        # =================================

        if "statuses" in value:

            print(
                "ℹ️ STATUS UPDATE"
            )

            print(
                value[
                    "statuses"
                ][0]["status"]
            )

    except Exception as e:

        print(
            "❌ ERROR:",
            e
        )

    return "OK", 200


# =====================================
# PRINT REGISTERED ROUTES
# =====================================

print(
    "\n========== REGISTERED ROUTES =========="
)

for rule in app.url_map.iter_rules():

    print(rule)

print(
    "=======================================\n"
)


# =====================================
# WHATSAPP FLOW ENDPOINT
# =====================================

@app.route("/flow-key-check")
def flow_key_check():
    private_key = os.getenv("FLOW_PRIVATE_KEY")
    passphrase = os.getenv("FLOW_PASSPHRASE")

    return {
        "FLOW_PRIVATE_KEY_EXISTS": bool(private_key),
        "FLOW_PRIVATE_KEY_LENGTH": len(private_key) if private_key else 0,
        "FLOW_PRIVATE_KEY_START": private_key[:30] if private_key else "",
        "FLOW_PRIVATE_KEY_END": private_key[-30:] if private_key else "",
        "FLOW_PASSPHRASE_EXISTS": bool(passphrase)
    }, 200


@app.route(
    "/flow",
    methods=["POST"]
)
def flow():
    try:

        data = request.get_json()

        print("\n==========================")
        print("WHATSAPP FLOW REQUEST")
        print(data)
        print("==========================")

        decrypted_body, aes_key, iv = decrypt_request(
            data["encrypted_aes_key"],
            data["encrypted_flow_data"],
            data["initial_vector"]
        )

        print("DECRYPTED FLOW DATA:")
        print(decrypted_body)

        response_data = {
            "data": {
                "status": "active"
            }
        }

        encrypted_response = encrypt_response(
            response_data,
            aes_key,
            iv
        )

        return encrypted_response, 200, {
            "Content-Type": "text/plain"
        }

    except Exception as e:

        print("❌ FLOW ERROR:", e)

        return "Flow processing error", 500