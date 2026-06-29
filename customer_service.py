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
        INSERT INTO customers(phone, name)
        VALUES(?, ?)
        """,
        (phone, name)
    )

    conn.commit()
    conn.close()


def save_customer(phone, name):

    customer = get_customer(phone)

    if customer:
        return customer

    create_customer(phone, name)

    return get_customer(phone)


def customer_exists(phone):

    customer = get_customer(phone)

    return customer is not None