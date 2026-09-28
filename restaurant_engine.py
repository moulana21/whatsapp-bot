from customer_service import (
    customer_exists,
    save_customer,
    get_customer
)

from menu import (
    get_menu_text,
    get_item
)


# =====================================
# TEMPORARY SESSION STORAGE
# =====================================

SESSIONS = {}


def process_message(phone, message):

    message = message.strip()

    # =====================================
    # DETECT TABLE QR
    # Example: T5
    # =====================================

    if message.upper().startswith("T"):

        table = message.upper()

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
            "order_status": "NEW"
        }

        # =================================
        # EXISTING CUSTOMER
        # =================================

        if customer_exists(phone):
         customer = get_customer(phone)
 
         print("========== CUSTOMER RECOGNITION ==========")
        print("PHONE:", phone)
        print("CUSTOMER EXISTS: True")
        print("CUSTOMER NAME:", customer["name"])
        print("==========================================")

    SESSIONS[phone]["customer_name"] = customer["name"]
    SESSIONS[phone]["step"] = "MAIN_MENU"

    return "SHOW_RETURNING_MENU_BUTTON"
    else:
    print("========== CUSTOMER RECOGNITION ==========")
    print("PHONE:", phone)
    print("CUSTOMER EXISTS: False")
    print("==========================================")
        # =================================
        # NEW CUSTOMER
        # =================================

    return (
         f"🙏 Welcome to Mandi House!\n\n"
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

        save_customer(phone, message)

        session["customer_name"] = message
        session["step"] = "MAIN_MENU"

        return "SHOW_MENU_BUTTON"

    # =====================================
       # MAIN MENU
       # =====================================
    if session["step"] == "MAIN_MENU":
   
       # Customer tapped View Menu
       if message == "VIEW_MENU":
   
           session["step"] = "CATEGORY"
   
           return "SHOW_CATEGORY_BUTTONS"
   
           # Keep typing 1 working temporarily
           if message == "1":
   
               session["step"] = "CATEGORY"
   
               return "SHOW_CATEGORY_BUTTONS"
   
           return "Please use the button above."

    # =====================================
    # CATEGORY SELECTION
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

        else:

            return "Please choose a category."

    # =====================================
    # MANDI MENU
    # =====================================

    if session["step"] == "MANDI_MENU":

        # Current menu numbering:
        # 1 = Chicken Mandi
        # 2 = Mutton Mandi
        # 3 = Fish Mandi

        item_numbers = ["1", "2", "3"]

        if message in item_numbers:

            item = get_item(message)

            if not item:

                return "❌ Menu item not found."

            session["selected_items"] = [item]
            session["current_item_index"] = 0
            session["step"] = "ASK_QUANTITY"

            return (
                f"✅ You selected:\n\n"
                f"{item['name']}\n\n"
                f"How many {item['name']}?"
            )

        return "Please choose a Mandi item."

    # =====================================
    # SHAWARMA MENU
    # =====================================

    if session["step"] == "SHAWARMA_MENU":

        # Current menu numbering:
        # 4 = Shawarma

        if message == "4":

            item = get_item("4")

            if not item:

                return "❌ Menu item not found."

            session["selected_items"] = [item]
            session["current_item_index"] = 0
            session["step"] = "ASK_QUANTITY"

            return (
                f"✅ You selected:\n\n"
                f"{item['name']}\n\n"
                f"How many {item['name']}?"
            )

        return "Please choose Shawarma."

    # =====================================
    # DRINKS MENU
    # =====================================

    if session["step"] == "DRINKS_MENU":

        # Current menu numbering:
        # 5 = Water
        # 6 = Coke
        # 7 = Pepsi

        if message in ["5", "6", "7"]:

            item = get_item(message)

            if not item:

                return "❌ Menu item not found."

            session["selected_items"] = [item]
            session["current_item_index"] = 0
            session["step"] = "ASK_QUANTITY"

            return (
                f"✅ You selected:\n\n"
                f"{item['name']}\n\n"
                f"How many {item['name']}?"
            )

        return "Please choose a drink."

    # =====================================
    # ASK QUANTITY
    # =====================================

    if session["step"] == "ASK_QUANTITY":

        if message.isdigit():

            quantity = int(message)

            if quantity <= 0:

                return "Please enter a valid quantity."

            item = session["selected_items"][0]

            session["cart"].append({
                "name": item["name"],
                "price": item["price"],
                "quantity": quantity
            })

            session["step"] = "AFTER_ADD"

            return (
                "✅ Added to your order!\n\n"
                f"{item['name']} × {quantity}"
            )

        return "Please enter a valid quantity."

    # =====================================
    # AFTER ADDING ITEM
    # =====================================

    if session["step"] == "AFTER_ADD":

        if message == "ADD_MORE":

            session["step"] = "CATEGORY"

            return "SHOW_CATEGORY_BUTTONS"

        elif message == "VIEW_CART":

            return "SHOW_CART"

        elif message == "REQUEST_BILL":

            return "SHOW_BILL"

        return "Please choose an option."

    # =====================================
    # FALLBACK
    # =====================================

    return "Something went wrong. Please try again."