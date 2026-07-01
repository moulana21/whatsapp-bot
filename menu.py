MENU = {
    "1": {"name": "Chicken Mandi", "price": 499},
    "2": {"name": "Mutton Mandi", "price": 699},
    "3": {"name": "Fish Mandi", "price": 599},
    "4": {"name": "Shawarma", "price": 120},
    "5": {"name": "Water Bottle", "price": 20},
    "6": {"name": "Coke", "price": 40},
    "7": {"name": "Pepsi", "price": 40}
}


def get_menu():
    return MENU


def get_item(item_no):
    return MENU.get(item_no)


def get_menu_text():

    text = "🍽 *MANDI HOUSE MENU*\n\n"

    for key, item in MENU.items():
        text += f"{key}. {item['name']} - ₹{item['price']}\n"

    text += "\nReply with menu number(s).\nExample: 1,3,6"

    return text