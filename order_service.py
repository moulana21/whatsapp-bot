import random
from database import get_connection


# =====================================
# GENERATE ORDER ID
# =====================================

def generate_order_id():

    return f"MH{random.randint(1000,9999)}"


# =====================================
# CREATE ORDER
# =====================================

def create_order(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    order_id = generate_order_id()

    cursor.execute(
        """
        INSERT INTO orders(
            order_id,
            customer_id
        )
        VALUES(?, ?)
        """,
        (
            order_id,
            customer_id
        )
    )

    conn.commit()

    db_id = cursor.lastrowid

    conn.close()

    return db_id, order_id


# =====================================
# GET ORDER
# =====================================

def get_order(db_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (db_id,)
    )

    order = cursor.fetchone()

    conn.close()

    return order


# =====================================
# GET ACTIVE ORDER
# =====================================

def active_order(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE customer_id = ?
        AND status = 'ACTIVE'
        """,
        (customer_id,)
    )

    order = cursor.fetchone()

    conn.close()

    return order


# =====================================
# ADD ITEM TO ORDER
# =====================================

def add_order_item(order_id, item_name, quantity, unit_price):

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


# =====================================
# GET ORDER ITEMS
# =====================================

def get_order_items(order_id):

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


# =====================================
# REMOVE ITEM
# =====================================

def remove_order_item(item_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM order_items
        WHERE id = ?
        """,
        (item_id,)
    )

    conn.commit()
    conn.close()


# =====================================
# CLEAR ORDER
# =====================================

def clear_order(order_id):

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


# =====================================
# CALCULATE BILL
# =====================================

def calculate_bill(order_id):

    items = get_order_items(order_id)

    subtotal = sum(item["line_total"] for item in items)

    gst = round(subtotal * 0.05, 2)

    total = subtotal + gst

    return subtotal, gst, total


# =====================================
# FINISH ORDER
# =====================================

def finish_order(db_id, subtotal, gst, total):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET

            subtotal = ?,
            gst = ?,
            total = ?,
            status = 'COMPLETED'

        WHERE id = ?
        """,
        (
            subtotal,
            gst,
            total,
            db_id
        )
    )

    conn.commit()
    conn.close()


# =====================================
# CANCEL ORDER
# =====================================

def cancel_order(db_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status = 'CANCELLED'
        WHERE id = ?
        """,
        (db_id,)
    )

    conn.commit()
    conn.close()