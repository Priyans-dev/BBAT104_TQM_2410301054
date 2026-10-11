import os
import sqlite3

# Database file is created in the project root folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "restaurant.db")


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

    conn.commit()
    conn.close()


# ---------- Menu item operations (CRUD) ----------

def add_item(name, category, price):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
        (name, category, price),
    )
    conn.commit()
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
    cur.execute(
        "UPDATE menu_items SET name = ?, category = ?, price = ? WHERE item_id = ?",
        (name, category, price, item_id),
    )
    conn.commit()
    conn.close()


def delete_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM menu_items WHERE item_id = ?", (item_id,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database ready:", DB_PATH)