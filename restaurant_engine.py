from customer_service import (
    customer_exists,
    save_customer,
    get_customer
)

from menu import (
    get_menu_text,
    get_item
)

from order_service import (
    create_order,
    add_order_item,
    calculate_bill,
    finish_order
)


# =====================================
# TEMPORARY SESSION STORAGE
# =====================================

SESSIONS = {}


# =====================================
# CART HELPERS
# =====================================

def add_to_cart(session, item, quantity):
    """
    Add an item to the cart.

    If the item already exists,
    increase its quantity.
    """

    for cart_item in session["cart"]:

        if cart_item["name"] == item["name"]:

            cart_item["quantity"] += quantity

            return

    session["cart"].append({
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity
    })


def get_cart_subtotal(session):
    """
    Calculate cart subtotal.
    """

    total = 0

    for item in session["cart"]:

        total += (
            item["price"] *
            item["quantity"]
        )

    return total


def get_cart_gst(session):
    """
    Calculate GST at 5%.
    """

    subtotal = get_cart_subtotal(session)

    return round(
        subtotal * 0.05,
        2
    )


def get_cart_total(session):
    """
    Calculate final total including GST.
    """

    subtotal = get_cart_subtotal(session)

    gst = get_cart_gst(session)

    return round(
        subtotal + gst,
        2
    )


# =====================================
# BUILD CART TEXT
# =====================================

def build_cart_text(session):

    if not session["cart"]:

        return (
            "🛒 YOUR CART\n\n"
            "Your cart is empty."
        )

    text = "🛒 YOUR CART\n\n"

    for item in session["cart"]:

        line_total = (
            item["price"] *
            item["quantity"]
        )

        text += (
            f"🍽 {item['name']} × "
            f"{item['quantity']} "
            f"— ₹{line_total}\n"
        )

    subtotal = get_cart_subtotal(session)

    gst = get_cart_gst(session)

    total = get_cart_total(session)

    text += "\n"
    text += "────────────────\n"
    text += f"Subtotal: ₹{subtotal}\n"
    text += f"GST (5%): ₹{gst}\n"
    text += f"Total: ₹{total}\n"

    return text


# =====================================
# BUILD CONFIRMATION TEXT
# =====================================

def build_confirmation_text(session):

    if not session["cart"]:

        return (
            "📋 ORDER CONFIRMATION\n\n"
            "Your cart is empty."
        )

    text = "📋 ORDER CONFIRMATION\n\n"

    for item in session["cart"]:

        line_total = (
            item["price"] *
            item["quantity"]
        )

        text += (
            f"🍽 {item['name']} × "
            f"{item['quantity']} "
            f"— ₹{line_total}\n"
        )

    subtotal = get_cart_subtotal(session)

    gst = get_cart_gst(session)

    total = get_cart_total(session)

    text += "\n"
    text += "────────────────\n"
    text += f"Subtotal: ₹{subtotal}\n"
    text += f"GST (5%): ₹{gst}\n"
    text += f"Total: ₹{total}\n\n"

    text += (
        f"📍 Table: {session['table']}\n"
        f"👤 Customer: {session['customer_name']}\n\n"
    )

    text += "Please confirm your order."

    return text


# =====================================
# SAVE CONFIRMED ORDER
# =====================================

def save_confirmed_order(phone, session):

    """
    Create the real database order.

    Steps:

    1. Find customer
    2. Create order
    3. Add every cart item
    4. Calculate bill
    5. Complete order
    """

    customer = get_customer(phone)

    if not customer:

        print("❌ CUSTOMER NOT FOUND")

        return None


    customer_id = customer["id"]


    print("======================================")
    print("🧾 CREATING REAL DATABASE ORDER")
    print("CUSTOMER ID:", customer_id)
    print("CUSTOMER NAME:", customer["name"])
    print("TABLE:", session["table"])
    print("======================================")


    # =====================================
    # CREATE ORDER
    # =====================================

    db_id, order_id = create_order(
        customer_id
    )

    print("✅ ORDER CREATED")
    print("DB ID:", db_id)
    print("ORDER ID:", order_id)


    # =====================================
    # ADD CART ITEMS
    # =====================================

    for item in session["cart"]:

        add_order_item(
            db_id,
            item["name"],
            item["quantity"],
            item["price"]
        )

        print(
            "✅ ITEM ADDED:",
            item["name"],
            "x",
            item["quantity"]
        )


    # =====================================
    # CALCULATE BILL FROM DATABASE
    # =====================================

    subtotal, gst, total = calculate_bill(
        db_id
    )

    print("======================================")
    print("💰 BILL CALCULATED")
    print("SUBTOTAL:", subtotal)
    print("GST:", gst)
    print("TOTAL:", total)
    print("======================================")


    # =====================================
    # FINISH ORDER
    # =====================================

    finish_order(
        db_id,
        subtotal,
        gst,
        total
    )

    print("✅ ORDER COMPLETED")
    print("ORDER ID:", order_id)


    # =====================================
    # SAVE ORDER INFORMATION IN SESSION
    # =====================================

    session["current_order_id"] = order_id

    session["order_db_id"] = db_id

    session["order_status"] = "COMPLETED"

    session["order_subtotal"] = subtotal

    session["order_gst"] = gst

    session["order_total"] = total


    return {
        "db_id": db_id,
        "order_id": order_id,
        "subtotal": subtotal,
        "gst": gst,
        "total": total
    }


# =====================================
# MAIN MESSAGE PROCESSOR
# =====================================

def process_message(phone, message):

    message = message.strip()

    print("🔎 DEBUG PHONE:", phone)

    customer = get_customer(phone)

    print(
        "🔎 DEBUG CUSTOMER:",
        dict(customer)
        if customer
        else None
    )


    # =====================================
    # DETECT TABLE QR
    # =====================================

    if message.upper().startswith("T"):

        table = message.upper()


        # Create fresh session

        SESSIONS[phone] = {

            "step": "ASK_NAME",

            # Customer
            "table": table,
            "customer_name": None,

            # Ordering
            "selected_items": [],
            "current_item_index": 0,
            "cart": [],

            # Order
            "current_order_id": None,
            "order_db_id": None,
            "order_status": "NEW",

            "order_subtotal": 0,
            "order_gst": 0,
            "order_total": 0
        }


        # =====================================
        # EXISTING CUSTOMER
        # =====================================

        if customer_exists(phone):

            customer = get_customer(phone)

            print(
                "========== CUSTOMER RECOGNITION =========="
            )

            print(
                "PHONE:",
                phone
            )

            print(
                "CUSTOMER EXISTS: True"
            )

            print(
                "CUSTOMER NAME:",
                customer["name"]
            )

            print(
                "=========================================="
            )


            SESSIONS[phone][
                "customer_name"
            ] = customer["name"]


            SESSIONS[phone][
                "step"
            ] = "MAIN_MENU"


            return "SHOW_RETURNING_MENU_BUTTON"


        # =====================================
        # NEW CUSTOMER
        # =====================================

        print(
            "========== CUSTOMER RECOGNITION =========="
        )

        print(
            "PHONE:",
            phone
        )

        print(
            "CUSTOMER EXISTS: False"
        )

        print(
            "=========================================="
        )


        return (
            "🙏 Welcome to Mandi House!\n\n"
            f"📍 Table: {table}\n\n"
            "May I know your name?"
        )


    # =====================================
    # SESSION NOT FOUND
    # =====================================

    if phone not in SESSIONS:

        return (
            "Please scan the QR code on your table "
            "to start ordering."
        )


    session = SESSIONS[phone]


    # =====================================
    # ASK CUSTOMER NAME
    # =====================================

    if session["step"] == "ASK_NAME":

        save_customer(
            phone,
            message
        )


        session["customer_name"] = message

        session["step"] = "MAIN_MENU"


        print(
            "========== NEW CUSTOMER SAVED =========="
        )

        print(
            "PHONE:",
            phone
        )

        print(
            "CUSTOMER NAME:",
            message
        )

        print(
            "========================================"
        )


        return "SHOW_MENU_BUTTON"


    # =====================================
    # MAIN MENU
    # =====================================

    if session["step"] == "MAIN_MENU":

        if message == "VIEW_MENU":

            session["step"] = "CATEGORY"

            return "SHOW_CATEGORY_BUTTONS"


        # Temporary typing support

        if message == "1":

            session["step"] = "CATEGORY"

            return "SHOW_CATEGORY_BUTTONS"


        return "Please use the button above."


    # =====================================
    # CATEGORY
    # =====================================

    if session["step"] == "CATEGORY":

        if message == "CATEGORY_MANDI":

            session["step"] = "MANDI_MENU"

            return "SHOW_MANDI_MENU"


        elif message == "CATEGORY_SHAWARMA":

            session["step"] = "SHAWARMA_MENU"

            return "SHOW_SHAWARMA_MENU"


        elif message == "CATEGORY_DRINKS":

            session["step"] = "DRINKS_MENU"

            return "SHOW_DRINKS_MENU"


        return "Please choose a category."


    # =====================================
    # MANDI MENU
    # =====================================

    if session["step"] == "MANDI_MENU":

        item_numbers = [
            "1",
            "2",
            "3"
        ]


        if message in item_numbers:

            item = get_item(message)


            if not item:

                return "❌ Menu item not found."


            session["selected_items"] = [
                item
            ]

            session["current_item_index"] = 0

            session["step"] = "ASK_QUANTITY"


            return (
                "✅ You selected:\n\n"
                f"{item['name']}\n\n"
                f"How many {item['name']}?"
            )


        return "Please choose a Mandi item."


    # =====================================
    # SHAWARMA MENU
    # =====================================

    if session["step"] == "SHAWARMA_MENU":

        if message == "4":

            item = get_item("4")


            if not item:

                return "❌ Menu item not found."


            session["selected_items"] = [
                item
            ]

            session["current_item_index"] = 0

            session["step"] = "ASK_QUANTITY"


            return (
                "✅ You selected:\n\n"
                f"{item['name']}\n\n"
                f"How many {item['name']}?"
            )


        return "Please choose Shawarma."


    # =====================================
    # DRINKS MENU
    # =====================================

    if session["step"] == "DRINKS_MENU":

        if message in [
            "5",
            "6",
            "7"
        ]:

            item = get_item(message)


            if not item:

                return "❌ Menu item not found."


            session["selected_items"] = [
                item
            ]

            session["current_item_index"] = 0

            session["step"] = "ASK_QUANTITY"


            return (
                "✅ You selected:\n\n"
                f"{item['name']}\n\n"
                f"How many {item['name']}?"
            )


        return "Please choose a drink."


    # =====================================
    # ASK QUANTITY
    #
    # TEMPORARY TYPED QUANTITY
    #
    # Later WhatsApp Flow will provide
    # the + / - quantity interface.
    # =====================================

    if session["step"] == "ASK_QUANTITY":

        if message.isdigit():

            quantity = int(message)


            if quantity <= 0:

                return (
                    "Please enter a valid quantity."
                )


            item = session[
                "selected_items"
            ][0]


            add_to_cart(
                session,
                item,
                quantity
            )


            session["step"] = "AFTER_ADD"


            return (
                "✅ Added to your order!\n\n"
                f"{item['name']} × {quantity}\n\n"
                "What would you like to do next?"
            )


        return "Please enter a valid quantity."


    # =====================================
    # AFTER ADDING ITEM
    # =====================================

    if session["step"] == "AFTER_ADD":

        # Add another item

        if message == "ADD_MORE":

            session["step"] = "CATEGORY"

            return "SHOW_CATEGORY_BUTTONS"


        # View cart

        elif message == "VIEW_CART":

            session["step"] = "CART"

            return "SHOW_CART"


        # Go directly to confirmation

        elif message == "REQUEST_BILL":

            if not session["cart"]:

                return "🛒 Your cart is empty."


            session["step"] = "CONFIRMATION"

            return build_confirmation_text(
                session
            )


        return "Please choose an option."


    # =====================================
    # CART
    # =====================================

    if session["step"] == "CART":

        # Add more

        if message == "ADD_MORE":

            session["step"] = "CATEGORY"

            return "SHOW_CATEGORY_BUTTONS"


        # Continue to confirmation

        elif message in [
            "CONFIRM_CART",
            "CHECKOUT",
            "PROCEED_CONFIRMATION"
        ]:

            if not session["cart"]:

                return "🛒 Your cart is empty."


            session["step"] = "CONFIRMATION"

            return build_confirmation_text(
                session
            )


        # Edit order

        elif message == "EDIT_ORDER":

            session["step"] = "CATEGORY"

            return "SHOW_CATEGORY_BUTTONS"


        return build_cart_text(session)


    # =====================================
    # ORDER CONFIRMATION
    # =====================================

    if session["step"] == "CONFIRMATION":

        # =====================================
        # CONFIRM ORDER
        # =====================================

        if message == "CONFIRM_ORDER":

            if not session["cart"]:

                return "❌ Your cart is empty."


            # Prevent duplicate confirmation

            if session["order_status"] == "COMPLETED":

                return (
                    "⚠️ This order has already "
                    "been confirmed."
                )


            # =================================
            # SAVE REAL ORDER
            # =================================

            order = save_confirmed_order(
                phone,
                session
            )


            if not order:

                return (
                    "❌ We could not create your "
                    "order. Please try again."
                )


            session["step"] = "ORDER_CONFIRMED"


            return (
                "🎉 ORDER CONFIRMED!\n\n"

                f"🧾 Order ID: "
                f"{order['order_id']}\n\n"

                f"📍 Table: "
                f"{session['table']}\n"

                f"👤 Customer: "
                f"{session['customer_name']}\n\n"

                f"💰 Subtotal: "
                f"₹{order['subtotal']}\n"

                f"GST (5%): "
                f"₹{order['gst']}\n"

                f"Total: "
                f"₹{order['total']}\n\n"

                "👨‍🍳 Your order has been "
                "sent to the restaurant."
            )


        # =====================================
        # EDIT ORDER
        # =====================================

        elif message == "EDIT_ORDER":

            session["step"] = "CATEGORY"

            return "SHOW_CATEGORY_BUTTONS"


        # =====================================
        # VIEW CART AGAIN
        # =====================================

        elif message == "VIEW_CART":

            session["step"] = "CART"

            return "SHOW_CART"


        return (
            "Please confirm or edit "
            "your order."
        )


    # =====================================
    # ORDER ALREADY CONFIRMED
    # =====================================

    if session["step"] == "ORDER_CONFIRMED":

        return (
            "✅ Your order is already confirmed.\n\n"
            f"🧾 Order ID: "
            f"{session['current_order_id']}\n"
            f"📍 Table: "
            f"{session['table']}\n"
            f"💰 Total: "
            f"₹{session['order_total']}"
        )


    # =====================================
    # FALLBACK
    # =====================================

    return "Something went wrong. Please try again."