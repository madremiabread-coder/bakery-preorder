import sqlite3

DB_PATH = "db/app.db"
SCHEMA_PATH = "db/schema.sql"
SEED_PATH = "db/seed.sql"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Always start fresh
c.executescript("DROP TABLE IF EXISTS options; DROP TABLE IF EXISTS products;")

# Load schema + seed SQL
with open(SCHEMA_PATH, "r") as f:
    schema_sql = f.read()
with open(SEED_PATH, "r") as f:
    seed_sql = f.read()

# Apply schema first, then data
c.executescript(schema_sql)
c.executescript(seed_sql)

conn.commit()
conn.close()

print("✅ Database reset, schema applied, and products seeded!")
