from customer_service import (
    customer_exists,
    save_customer,
    get_customer
)

from menu import get_menu_text

# Temporary session storage
SESSIONS = {}


def main_menu(name, table):
    return f"""
🙏 Welcome {name} ❤️

📍 Table: {table}

Please choose an option:

1️⃣ View Menu
2️⃣ Current Order
3️⃣ Call Waiter
4️⃣ Request Bill
5️⃣ Restaurant Timings
"""


def process_message(phone, message):

    message = message.strip()

    # ------------------------------------
    # Detect table QR (Example: T5)
    # ------------------------------------
    if message.upper().startswith("T"):

        table = message.upper()

        SESSIONS[phone] = {
            "step": "ASK_NAME",
            "table": table
        }

        if customer_exists(phone):

            customer = get_customer(phone)

            SESSIONS[phone]["step"] = "MAIN_MENU"

            return main_menu(customer["name"], table)

        return (
            f"🙏 Welcome to Mandi House!\n\n"
            f"📍 Table: {table}\n\n"
            "May I know your name?"
        )

    # ------------------------------------
    # Session not found
    # ------------------------------------
    if phone not in SESSIONS:
        return (
            "Please scan the QR code on your table to start ordering."
        )

    session = SESSIONS[phone]

    # ------------------------------------
    # Ask Name
    # ------------------------------------
    if session["step"] == "ASK_NAME":

        save_customer(phone, message)

        session["step"] = "MAIN_MENU"

        return main_menu(message, session["table"])

    # ------------------------------------
    # Main Menu
    # ------------------------------------
    if session["step"] == "MAIN_MENU":

        if message == "1":
            session["step"] = "VIEW_MENU"
            return get_menu_text()

        elif message == "2":
            return "🛒 Current Order feature is coming next."

        elif message == "3":
            return "👨‍🍳 Waiter has been notified. (Coming soon)"

        elif message == "4":
            return "🧾 Request Bill feature coming next."

        elif message == "5":
            return (
                "🕒 Restaurant Timings\n"
                "11:00 AM - 11:00 PM"
            )

        else:
            return "Please choose a valid option (1-5)."

    # ------------------------------------
    # View Menu
    # ------------------------------------
    if session["step"] == "VIEW_MENU":

        return "🚧 Menu ordering is the next feature."

    return "Something went wrong."