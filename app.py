from flask import Flask

from config import HOST, PORT, DEBUG, RESTAURANT_NAME
from database import init_database
from customer_service import (
    get_customer,
    save_customer,
    customer_exists
)
from menu import get_menu_text

# Create Flask App
app = Flask(__name__)

# Initialize Database
init_database()


@app.route("/")
def home():
    return {
        "status": "running",
        "project": f"{RESTAURANT_NAME} Restaurant Bot V3",
        "database": "Connected"
    }


@app.route("/test_customer")
def test_customer():

    phone = "9999999999"

    if customer_exists(phone):

        customer = get_customer(phone)

        return {
            "message": "Customer Found",
            "name": customer["name"]
        }

    save_customer(phone, "Moulana")

    return {
        "message": "New Customer Saved"
    }


@app.route("/menu")
def menu():

    return {
        "menu": get_menu_text()
    }


if __name__ == "__main__":

    print("🚀 Starting Restaurant Bot V3...")

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )