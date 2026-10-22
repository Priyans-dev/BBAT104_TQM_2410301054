"""Automatic version of the 19 checks in docs/defect_log.md.

Run from the project folder:  python tests/test_q06_checks.py
A temporary database is used, so your real restaurant.db is never touched.
TC-18 and TC-19 (confirmation dialogs) need the screen and must be checked by hand.
"""
import os
import sys
import tempfile

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src import database, validators  # noqa: E402

# Same list as CATEGORIES in src/menu_page.py
CATEGORIES = ["Starters", "Main Course", "Breads", "Rice", "Desserts", "Beverages", "Snacks"]

# Use a temporary database for the tests
database.DB_PATH = os.path.join(tempfile.mkdtemp(), "test_restaurant.db")
database.init_db()


def validate_form(name, category, price_text):
    """Same checks as the Add/Edit form. Returns (clean_name, price) or None if invalid."""
    name = validators.clean_name(name)
    if validators.validate_name(name):
        return None
    if validators.validate_category(category, CATEGORIES):
        return None
    price, error = validators.validate_price(price_text)
    if error:
        return None
    return name, price


def try_add(name, category, price_text):
    """Returns 'invalid', 'duplicate' or 'accepted'."""
    checked = validate_form(name, category, price_text)
    if checked is None:
        return "invalid"
    try:
        database.add_item(checked[0], category, checked[1])
    except database.DuplicateItemError:
        return "duplicate"
    return "accepted"


def try_rename(item_id, new_name, category, price_text):
    checked = validate_form(new_name, category, price_text)
    if checked is None:
        return "invalid"
    try:
        database.update_item(item_id, checked[0], category, checked[1])
    except database.DuplicateItemError:
        return "duplicate"
    return "accepted"


# Setup: the menu already has Paneer Tikka and Veg Pulao
database.add_item("Paneer Tikka", "Starters", 250)
database.add_item("Veg Pulao", "Rice", 180)
veg_pulao_id = [row[0] for row in database.get_all_items() if row[1] == "Veg Pulao"][0]

results = []


def check(tc, description, actual, expected):
    passed = actual == expected
    results.append(passed)
    status = "PASS" if passed else "FAIL"
    print(f"{tc}  {status}  {description}  (expected {expected}, got {actual})")


check("TC-01", "Add 'Paneer Tikka' again", try_add("Paneer Tikka", "Starters", "250"), "duplicate")
check("TC-02", "Add 'paneer tikka'", try_add("paneer tikka", "Starters", "250"), "duplicate")
check("TC-03", "Add 'Paneer Tikka ' (space at end)", try_add("Paneer Tikka ", "Starters", "250"), "duplicate")
check("TC-04", "Add 'Paneer   Tikka' (spaces inside)", try_add("Paneer   Tikka", "Starters", "250"), "duplicate")
check("TC-05", "Rename 'Veg Pulao' to 'Paneer Tikka'", try_rename(veg_pulao_id, "Paneer Tikka", "Rice", "180"), "duplicate")
check("TC-06", "Name '@@@'", try_add("@@@", "Starters", "100"), "invalid")
check("TC-07", "Name '123'", try_add("123", "Starters", "100"), "invalid")
check("TC-08", "Name 'A'", try_add("A", "Starters", "100"), "invalid")
check("TC-09", "Name of 60 characters", try_add("Abcdefghij" * 6, "Starters", "100"), "invalid")
check("TC-10", "Price 250.999", try_add("Veg Biryani", "Rice", "250.999"), "invalid")
check("TC-11", "Price 99999", try_add("Veg Biryani", "Rice", "99999"), "invalid")
check("TC-12", "Price nan", try_add("Veg Biryani", "Rice", "nan"), "invalid")
check("TC-13", "Price 1e5", try_add("Veg Biryani", "Rice", "1e5"), "invalid")
check("TC-14", "Price abc", try_add("Veg Biryani", "Rice", "abc"), "invalid")
check("TC-15", "Price -50", try_add("Veg Biryani", "Rice", "-50"), "invalid")
check("TC-16", "Price 0", try_add("Veg Biryani", "Rice", "0"), "invalid")
check("TC-17", "Empty name", try_add("", "Rice", "100"), "invalid")

# Extra checks
check("EX-01", "A new valid item is accepted", try_add("Veg Biryani", "Rice", "220"), "accepted")
bill_a = database.create_bill([("Paneer Tikka", 250.0, 2)])[0]
bill_b = database.create_bill([("Veg Pulao", 180.0, 1)])[0]
check("EX-02", "Two bills get different Bill IDs", bill_a != bill_b, True)
check("EX-03", "Bill total = subtotal + 5% tax", database.calculate_totals([("A", 100.0, 2)]), (200.0, 10.0, 210.0))

print()
print("TC-18 and TC-19 (confirmation dialogs): check by hand in the app.")
passed = sum(results)
print(f"Result: {passed} of {len(results)} automatic checks passed.")
sys.exit(0 if passed == len(results) else 1)