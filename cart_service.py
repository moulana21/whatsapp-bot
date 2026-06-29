from database import get_connection


def add_item(order_id, item_name, quantity, unit_price):

    conn = get_connection()
    cursor = conn.cursor()

    line_total = quantity * unit_price

    cursor.execute(
        """
        INSERT INTO order_items(
            order_id,
            item_name,
            quantity,
            unit_price,
            line_total
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            order_id,
            item_name,
            quantity,
            unit_price,
            line_total
        )
    )

    conn.commit()
    conn.close()


def get_cart(order_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM order_items
        WHERE order_id = ?
        """,
        (order_id,)
    )

    items = cursor.fetchall()

    conn.close()

    return items


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