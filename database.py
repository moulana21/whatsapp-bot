import sqlite3
from config import DATABASE_NAME


def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # CUSTOMERS
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        phone TEXT UNIQUE NOT NULL,

        name TEXT NOT NULL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # =====================================
    # ORDERS
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        order_id TEXT UNIQUE,

        customer_id INTEGER,

        status TEXT DEFAULT 'ACTIVE',

        subtotal REAL DEFAULT 0,

        gst REAL DEFAULT 0,

        total REAL DEFAULT 0,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(customer_id)
        REFERENCES customers(id)

    )
    """)

    # =====================================
    # ORDER ITEMS
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        order_id INTEGER,

        item_name TEXT,

        quantity INTEGER,

        unit_price REAL,

        line_total REAL,

        FOREIGN KEY(order_id)
        REFERENCES orders(id)

    )
    """)

    conn.commit()
    conn.close()

    print("✅ Database initialized successfully.")