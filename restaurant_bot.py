def handle_message(sender, text):

    lower_text = text.lower()

    # New customer
    if sender not in customers:

        if lower_text == "hi":
            customers[sender] = {
                "waiting_name": True
            }

            send_message(
                sender,
                "👋 Welcome to MANDI HOUSE\n\nMay I know your name?"
            )
            return

        send_message(sender, "Send HI to start.")
        return

    # Save customer name
    if customers[sender].get("waiting_name"):

        customers[sender]["name"] = text
        customers[sender]["waiting_name"] = False

        send_message(
            sender,
            f"""🍽 Welcome {text}

🏠 MANDI HOUSE

1. Chicken Mandi - ₹499
2. Mutton Mandi - ₹699
3. Fish Mandi - ₹599
4. Shawarma - ₹120

Reply with item number."""
        )
        return

    # Returning customer
    if lower_text == "hi":

        name = customers[sender]["name"]

        send_message(
            sender,
            f"""👋 Welcome back {name}

🏠 MANDI HOUSE

1. Chicken Mandi - ₹499
2. Mutton Mandi - ₹699
3. Fish Mandi - ₹599
4. Shawarma - ₹120

Reply with item number."""
        )
        return

    # Select menu item
    if text in MENU and (
        sender not in orders or
        not orders[sender].get("awaiting_quantity")
    ):

        orders[sender] = {
            "item": MENU[text]["name"],
            "price": MENU[text]["price"],
            "awaiting_quantity": True
        }

        send_message(sender, "How many plates?")
        return

    # Quantity input
    if sender in orders and orders[sender].get("awaiting_quantity"):

        if text.isdigit():

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
            orders[sender]["awaiting_quantity"] = False

            send_message(
                sender,
                f"""✅ Order Summary

Item: {item}
Quantity: {qty}

Subtotal: ₹{subtotal}
GST (5%): ₹{gst}
Total Bill: ₹{total}

Reply CONFIRM to place order."""
            )

        return

    # Confirm order
    if lower_text == "confirm":

        if sender in orders:

            order = orders[sender]

            order_id = f"MH{random.randint(1000,9999)}"

            send_message(
                sender,
                f"""🎉 Order Confirmed

🏠 MANDI HOUSE

Order ID: {order_id}

Item: {order['item']}
Quantity: {order['qty']}

Subtotal: ₹{order['subtotal']}
GST: ₹{order['gst']}
Total: ₹{order['total']}

Thank you for ordering ❤️"""
            )

            del orders[sender]

        return

    send_message(sender, "Send HI to start ordering.")