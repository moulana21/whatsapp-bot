import random
from database import get_connection


def generate_order_id():

    return f"MH{random.randint(1000,9999)}"


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


def finish_order(db_id, subtotal, gst, total):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET
            subtotal=?,
            gst=?,
            total=?,
            status='COMPLETED'
        WHERE id=?
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


def active_order(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM orders
        WHERE customer_id=?
        AND status='ACTIVE'
        """,
        (customer_id,)
    )

    order = cursor.fetchone()

    conn.close()

    return order

def cancel_order(db_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE orders
        SET status='CANCELLED'
        WHERE id=?
        """,
        (db_id,)
    )

    conn.commit()
    conn.close()