-- Minimal schema for Task 12 (products only)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  price_cents INTEGER NOT NULL CHECK (price_cents >= 0),
  description TEXT,
  image_url TEXT,
  is_active INTEGER NOT NULL DEFAULT 1,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Additional tables (orders, weekly_batches, waitlist, etc.) will be added in the next steps.
-- Options (add-ons or variants tied to a product)
CREATE TABLE IF NOT EXISTS options (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id INTEGER NOT NULL,
  name TEXT NOT NULL,
  extra_price_cents INTEGER NOT NULL DEFAULT 0 CHECK (extra_price_cents >= 0),
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);