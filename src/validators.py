import re

MAX_NAME_LENGTH = 40
MAX_PRICE = 10000

NAME_PATTERN = re.compile(r"^[A-Za-z0-9 \-'&().,]+$")
PRICE_PATTERN = re.compile(r"^\d+(\.\d{1,2})?$")


def clean_name(name):
    """Remove extra spaces: '  Paneer   Tikka ' becomes 'Paneer Tikka'."""
    return " ".join(name.split())


def validate_name(name):
    """Return an error message, or None if the name is valid."""
    name = clean_name(name)
    if not name:
        return "Item name is required."
    if len(name) < 2:
        return "Item name must be at least 2 characters."
    if len(name) > MAX_NAME_LENGTH:
        return f"Item name must be at most {MAX_NAME_LENGTH} characters."
    if not NAME_PATTERN.match(name):
        return "Item name can only have letters, numbers, spaces and - ' & ( ) . ,"
    if not re.search(r"[A-Za-z]", name):
        return "Item name must contain at least one letter."
    return None


def validate_category(category, allowed):
    """Return an error message, or None if the category is valid."""
    if not category:
        return "Category is required."
    if category not in allowed:
        return "Please choose a category from the list."
    return None


def validate_price(text):
    """Return (price, error). price is None when there is an error."""
    text = text.strip()
    if not text:
        return None, "Price is required."
    if not PRICE_PATTERN.match(text):
        return None, "Price must be a valid amount like 250 or 99.50 (max 2 decimals)."
    price = float(text)
    if price <= 0:
        return None, "Price must be greater than 0."
    if price > MAX_PRICE:
        return None, f"Price cannot be more than Rs. {MAX_PRICE}."
    return price, None