# update_images.py
import os
import sqlite3

DB_PATH = os.path.join("db", "app.db")
SEED_PATH = os.path.join("db", "seed.sql")
IMAGES_DIR = os.path.join("static", "images")

PLACEHOLDER_URL = "https://placehold.co/600x400?text={}"

def normalize_filename(filename: str) -> str:
    """
    Convert filenames like 'sourdough_birote.jpg' into 'Sourdough Birote'
    """
    name, _ = os.path.splitext(filename)
    return name.replace("_", " ").title()

def main():
    if not os.path.exists(IMAGES_DIR):
        print(f"❌ Images folder not found: {IMAGES_DIR}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Get all products from DB
    cur.execute("SELECT id, name FROM products")
    products = cur.fetchall()

    updated = []
    for pid, product_name in products:
        # Check if there is a matching file in static/images/
        expected_filename = product_name.lower().replace(" ", "_") + ".jpg"
        expected_path = os.path.join(IMAGES_DIR, expected_filename)

        if os.path.exists(expected_path):
            image_url = f"static/images/{expected_filename}"
        else:
            # fallback to placeholder
            safe_name = product_name.replace(" ", "+")
            image_url = PLACEHOLDER_URL.format(safe_name)

        cur.execute("UPDATE products SET image_url = ? WHERE id = ?", (image_url, pid))
        updated.append((product_name, image_url))

    conn.commit()
    conn.close()

    # --- Update seed.sql with the new image_url values ---
    if os.path.exists(SEED_PATH):
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            sql_content = f.read()

        for product_name, image_url in updated:
            # Replace or add the image_url field in the seed.sql
            if "INSERT INTO products" in sql_content:
                sql_content = sql_content.replace(
                    f"INSERT INTO products (name, price_cents, description) VALUES ('{product_name}',",
                    f"INSERT INTO products (name, price_cents, description, image_url) VALUES ('{product_name}',"
                )
                sql_content = sql_content.replace(
                    f"'{product_name}', ",
                    f"'{product_name}', '{image_url}', "
                )

        with open(SEED_PATH, "w", encoding="utf-8") as f:
            f.write(sql_content)

    print(f"✅ Updated {len(updated)} product(s) with images:")
    for name, path in updated:
        print(f"   {name} → {path}")

if __name__ == "__main__":
    main()

