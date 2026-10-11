import os
import sqlite3
from datetime import datetime

# Database file is created in the project root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "restaurant.db")

# Tax rate applied on every bill (5%)
TAX_RATE = 0.05


class DuplicateItemError(Exception):
    """Raised when a menu item with the same name already exists."""


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create all tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS menu_items (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bills (
            bill_id TEXT PRIMARY KEY,
            bill_date TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax REAL NOT NULL,
            total REAL NOT NULL
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bill_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bill_id TEXT NOT NULL,
            item_name TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            line_total REAL NOT NULL,
            FOREIGN KEY (bill_id) REFERENCES bills (bill_id)
        )
        """
    )

    enforce_unique_menu_names(cur)

    conn.commit()
    conn.close()


def enforce_unique_menu_names(cur):
    """Q06 - Unique constraint: no two menu items may share the same name
    (ignoring capital letters and extra spaces)."""
    # Remove any old duplicates first (the oldest item is kept)
    cur.execute(
        """
        DELETE FROM menu_items
        WHERE item_id NOT IN (
            SELECT MIN(item_id) FROM menu_items GROUP BY LOWER(TRIM(name))
        )
        """
    )
    cur.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_menu_unique_name
        ON menu_items (LOWER(TRIM(name)))
        """
    )


# ---------- Menu item operations (CRUD) ----------

def add_item(name, category, price):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
            (name, category, price),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise DuplicateItemError(name)
    finally:
        conn.close()


def get_all_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT item_id, name, category, price FROM menu_items ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def update_item(item_id, name, category, price):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE menu_items SET name = ?, category = ?, price = ? WHERE item_id = ?",
            (name, category, price, item_id),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        raise DuplicateItemError(name)
    finally:
        conn.close()


def delete_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM menu_items WHERE item_id = ?", (item_id,))
    conn.commit()
    conn.close()


# ---------- Billing operations ----------

def calculate_totals(cart_items):
    """cart_items: list of (name, price, quantity). Returns (subtotal, tax, total)."""
    subtotal = sum(price * qty for _, price, qty in cart_items)
    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax, 2)
    return round(subtotal, 2), tax, total


def create_bill(cart_items):
    """Save a bill with all its items. Returns (bill_id, subtotal, tax, total)."""
    subtotal, tax, total = calculate_totals(cart_items)

    conn = get_connection()
    cur = conn.cursor()

    # Q06 - Unique bill ID: always one more than the highest existing number
    cur.execute("SELECT COALESCE(MAX(CAST(SUBSTR(bill_id, 6) AS INTEGER)), 0) FROM bills")
    bill_id = f"BILL-{cur.fetchone()[0] + 1:04d}"
    bill_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute(
        "INSERT INTO bills (bill_id, bill_date, subtotal, tax, total) VALUES (?, ?, ?, ?, ?)",
        (bill_id, bill_date, subtotal, tax, total),
    )
    for name, price, qty in cart_items:
        cur.execute(
            """
            INSERT INTO bill_items (bill_id, item_name, price, quantity, line_total)
            VALUES (?, ?, ?, ?, ?)
            """,
            (bill_id, name, price, qty, round(price * qty, 2)),
        )

    conn.commit()
    conn.close()
    return bill_id, subtotal, tax, total


def get_all_bills():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT bill_id, bill_date, subtotal, tax, total FROM bills ORDER BY bill_date DESC, bill_id DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_bill_items(bill_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT item_name, price, quantity, line_total FROM bill_items WHERE bill_id = ?",
        (bill_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    init_db()
    print("Database ready:", DB_PATH)