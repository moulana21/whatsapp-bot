from database import get_connection


# =====================================
# GET CUSTOMER BY PHONE
# =====================================
def get_customer(phone):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM customers
        WHERE phone = ?
        """,
        (phone,)
    )

    customer = cursor.fetchone()

    conn.close()

    return customer


# =====================================
# CREATE NEW CUSTOMER
# =====================================
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


# =====================================
# SAVE CUSTOMER
# =====================================
def save_customer(phone, name):

    customer = get_customer(phone)

    if customer:
        return customer

    create_customer(phone, name)

    return get_customer(phone)


# =====================================
# CHECK CUSTOMER EXISTS
# =====================================
def customer_exists(phone):

    return get_customer(phone) is not None


# =====================================
# UPDATE CUSTOMER NAME
# =====================================
def update_customer_name(phone, name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET
            name = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
        """,
        (name, phone)
    )

    conn.commit()
    conn.close()


# =====================================
# UPDATE LAST VISIT
# =====================================
def update_last_visit(phone):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET
            last_visit = CURRENT_TIMESTAMP,
            updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
        """,
        (phone,)
    )

    conn.commit()
    conn.close()


# =====================================
# INCREMENT TOTAL ORDERS
# =====================================
def increment_total_orders(phone):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET
            total_orders = total_orders + 1,
            updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
        """,
        (phone,)
    )

    conn.commit()
    conn.close()


# =====================================
# UPDATE TOTAL SPENT
# =====================================
def update_total_spent(phone, amount):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET
            total_spent = total_spent + ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
        """,
        (amount, phone)
    )

    conn.commit()
    conn.close()


# =====================================
# UPDATE FAVORITE ITEM
# =====================================
def update_favorite_item(phone, item_name):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET
            favorite_item = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE phone = ?
        """,
        (item_name, phone)
    )

    conn.commit()
    conn.close()


# =====================================
# GET CUSTOMER STATS
# =====================================
def get_customer_stats(phone):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            total_orders,
            total_spent,
            favorite_item,
            first_visit,
            last_visit
        FROM customers
        WHERE phone = ?
        """,
        (phone,)
    )

    stats = cursor.fetchone()

    conn.close()

    return stats


# =====================================
# GET ALL CUSTOMERS
# =====================================
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