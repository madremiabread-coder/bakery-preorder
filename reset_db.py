import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "db", "app.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "db", "schema.sql")
SEED_PATH = os.path.join(BASE_DIR, "db", "seed.sql")

def reset_database():
    # Remove existing DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Deleted old database.")

    # Create new DB and apply schema
    conn = sqlite3.connect(DB_PATH)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    print("Applied schema.sql")

    # Apply seed data
    with open(SEED_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    print("Applied seed.sql")

    conn.commit()
    conn.close()
    print("Database reset complete.")

if __name__ == "__main__":
    reset_database()
