from database import get_connection


def get_customer(phone):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM customers WHERE phone = ?",
        (phone,)
    )

    customer = cursor.fetchone()

    conn.close()

    return customer


def create_customer(phone, name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO customers(
            phone,
            name
        )
        VALUES (?, ?)
        """,
        (phone, name)
    )

    conn.commit()

    customer_id = cursor.lastrowid

    conn.close()

    return customer_id


def save_customer(phone, name):

    customer = get_customer(phone)

    if customer:
        return customer

    create_customer(phone, name)

    return get_customer(phone)


def customer_exists(phone):

    return get_customer(phone) is not None


def update_customer_name(phone, name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET name = ?
        WHERE phone = ?
        """,
        (name, phone)
    )

    conn.commit()
    conn.close()


def get_all_customers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM customers
        ORDER BY id DESC
        """
    )

    customers = cursor.fetchall()

    conn.close()

    return customers