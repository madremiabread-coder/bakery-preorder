import os
import sqlite3
from flask import g

# DB path: /db/app.db (relative to project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "db")
DB_PATH = os.path.join(DB_DIR, "app.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")

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
    db = g.pop("db", None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return (rows[0] if rows else None) if one else rows

def init_db(app=None):
    """
    Creates tables (if not exist) and seeds sample products if table is empty.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        # Run schema
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())

        # Seed only if products table is empty
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
                        # You can replace with /static/images/your-image.jpg later
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
