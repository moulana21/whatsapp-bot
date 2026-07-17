from customer_service import (
    customer_exists,
    save_customer,
    get_customer
)

from menu import get_menu_text, get_item

# Stores temporary conversation state
SESSIONS = {}


def process_message(phone, message):

    message = message.strip()

    # -------------------------------
    # New Customer
    # -------------------------------
    if not customer_exists(phone):

        if phone not in SESSIONS:

            SESSIONS[phone] = {
    "step": "ASK_NAME",
    "cart": [],
    "selected_items": [],
    "current_index": 0
}
            return (
                "🙏 Welcome to Mandi House!\n\n"
                "May I know your name?"
            )

        if SESSIONS[phone]["step"] == "ASK_NAME":

            save_customer(phone, message)

            del SESSIONS[phone]

            return (
                f"Welcome {message}! ❤️\n\n"
                + get_menu_text()
            )

    # -------------------------------
    # Existing Customer
    # -------------------------------
    customer = get_customer(phone)

    if message.lower() in ["hi", "hello", "menu"]:

        return (
            f"🙏 Welcome back {customer['name']} ❤️\n\n"
            + get_menu_text()
        )

    return (
        "Type MENU to see our delicious menu 😄"
    )