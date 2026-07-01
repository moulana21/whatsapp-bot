import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WhatsApp Cloud API
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Database
DATABASE_NAME = "restaurant.db"

# GST
GST_PERCENTAGE = 5

# Restaurant Details
RESTAURANT_NAME = "Mandi House"

# Currency
CURRENCY = "₹"

# Flask
HOST = "0.0.0.0"
PORT = 5000
DEBUG = False