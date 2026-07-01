def remove_item(order_id, item_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM order_items
        WHERE order_id = ?
        AND item_name = ?
        """,
        (
            order_id,
            item_name
        )
    )

    conn.commit()
    conn.close()


# 👇 Add this here
def clear_cart(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM order_items
        WHERE order_id = ?
        """,
        (order_id,)
    )

    conn.commit()
    conn.close()


def calculate_bill(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT SUM(line_total)
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,)
    )

    subtotal = cursor.fetchone()[0]

    if subtotal is None:
        subtotal = 0

    gst = round(subtotal * 0.05, 2)

    total = subtotal + gst

    conn.close()

    return subtotal, gst, total


# 👇 Add this at the end of the file
def cart_count(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,)
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count