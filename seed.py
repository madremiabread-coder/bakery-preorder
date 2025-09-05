# seed.py
import sqlite3
import os

DB_PATH = os.path.join("db", "app.db")

def run_sql_file(cursor, filepath):
    with open(filepath, "r") as f:
        sql = f.read()
    cursor.executescript(sql)

def main():
    # Connect to DB
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Load schema (ensures tables exist: products, options, orders, order_items, etc.)
    run_sql_file(cur, os.path.join("db", "schema.sql"))

    # 2. Clear existing product + options data
    cur.execute("DELETE FROM options;")
    cur.execute("DELETE FROM products;")

    # 3. Insert products + options from seed.sql
    run_sql_file(cur, os.path.join("db", "seed.sql"))

    conn.commit()
    conn.close()
    print("✅ Database reset: schema applied, products + options seeded (orders empty).")

if __name__ == "__main__":
    main()
