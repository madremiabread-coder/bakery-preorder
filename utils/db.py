import os
import sqlite3
from flask import g

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "app.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")


# --- Connection helpers ---
def get_db():
    """
    Returns a SQLite connection tied to the Flask 'g' context.
    """
    if "db" not in g:
        # Ensure directory exists
        os.makedirs(DB_DIR, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(exception=None):
    """
    Close the database connection when the Flask app context ends.
    """
    db = g.pop("db", None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    """
    Run a query and return results (dict-like rows).
    """
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows


def init_db(app=None):
    """
    Initialize the database:
    - Ensure the schema exists.
    - Optionally seed sample products if empty.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        # Run schema.sql to ensure tables exist
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        # Seed if products table is empty
        existing = conn.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"]
        if existing == 0:
            conn.executemany(
                """
                INSERT INTO products (name, price_cents, description, image_url, is_active)
                VALUES (?, ?, ?, ?, 1)
                """,
                [
                    (
                        "Sourdough Country Loaf",
                        1200,
                        "Naturally leavened, slow-fermented loaf with an open crumb and crackly crust.",
                        "https://images.unsplash.com/photo-1608198093002-ad4e005484ec?q=80&w=1200&auto=format&fit=crop",
                    ),
                    (
                        "Chocolate Chunk Cookie Pack (6)",
                        900,
                        "Crisp edges, gooey center, generous dark chocolate chunks. Baked fresh weekly.",
                        "https://images.unsplash.com/photo-1606313564200-e75d5e30476e?q=80&w=1200&auto=format&fit=crop",
                    ),
                ],
            )
        conn.commit()


# --- Orders helper ---
def create_order(customer_name, items):
    """
    Create a new order and insert related order_items.
    `items` = list of dicts like:
      { "product_id": 1, "option_id": None, "quantity": 2 }
    """
    conn = get_db()
    cur = conn.cursor()

    # --- Calculate total_cents before inserting order ---
    total_cents = 0
    for item in items:
        product = cur.execute(
            "SELECT price_cents FROM products WHERE id = ?",
            (item["product_id"],)
        ).fetchone()
        if not product:
            raise ValueError(f"Invalid product_id {item['product_id']}")

        subtotal = product["price_cents"] * item["quantity"]

        if item.get("option_id"):
            option = cur.execute(
                "SELECT extra_price_cents FROM options WHERE id = ?",
                (item["option_id"],)
            ).fetchone()
            if not option:
                raise ValueError(f"Invalid option_id {item['option_id']}")
            subtotal += option["extra_price_cents"] * item["quantity"]

        total_cents += subtotal

    # --- Insert order with total ---
    cur.execute(
        "INSERT INTO orders (customer_name, total_cents) VALUES (?, ?)",
        (customer_name, total_cents)
    )
    order_id = cur.lastrowid

    # --- Insert order items ---
    for item in items:
        cur.execute(
            """
            INSERT INTO order_items (order_id, product_id, option_id, quantity)
            VALUES (?, ?, ?, ?)
            """,
            (order_id, item["product_id"], item.get("option_id"), item["quantity"])
        )

    conn.commit()

    return {
        "order_id": order_id,
        "customer_name": customer_name,
        "total_cents": total_cents,
        "items": items,
    }


