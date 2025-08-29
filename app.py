import os
import sqlite3
from flask import Flask, render_template, jsonify
from utils.db import init_db, query_db, close_db

# --- App setup ---
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-not-secret")

# --- Database connection helper ---
def get_db_connection():
    """
    Create a direct SQLite connection (used for custom queries in API routes).
    Using sqlite3.Row allows accessing rows like dictionaries.
    """
    conn = sqlite3.connect("db/app.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Database lifecycle ---
with app.app_context():
    # Initialize database if needed (schema + seed data)
    init_db(app)

@app.teardown_appcontext
def _teardown_db(exception):
    # Close database connection at the end of each request
    close_db(exception)

# --- Jinja filters (used inside HTML templates) ---
def cents_to_dollars(cents):
    """Convert price from integer cents to formatted dollars string."""
    return f"${cents/100:.2f}"

app.jinja_env.filters["currency"] = cents_to_dollars


# ================================
# HTML PAGE ROUTES (render templates)
# ================================

@app.route("/")
def home():
    """Homepage: show featured products (first 2 active)."""
    featured = query_db(
        "SELECT id, name, price_cents, description, image_url "
        "FROM products WHERE is_active=1 ORDER BY id LIMIT 2"
    )
    return render_template("home.html", featured=featured)

@app.route("/products")
def products():
    """All products page."""
    items = query_db(
        "SELECT id, name, price_cents, description, image_url "
        "FROM products WHERE is_active=1 ORDER BY id"
    )
    return render_template("products.html", products=items)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    """
    Product detail page.
    NOTE: Product data is loaded dynamically via JavaScript
    from the /api/product/<id> endpoint.
    """
    return render_template("product_detail.html")

@app.route("/cart")
def cart():
    """Shopping cart page (basket)."""
    return render_template("cart.html")


# ================================
# API ROUTES (return JSON for frontend)
# ================================

@app.route("/api/products")
def api_products():
    """Return all active products (no options)."""
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products WHERE is_active=1").fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route("/api/products_with_options")
def api_products_with_options():
    """Return all active products with their available options."""
    conn = get_db_connection()
    products = conn.execute(
        "SELECT * FROM products WHERE is_active=1 ORDER BY id"
    ).fetchall()

    product_dicts = []
    for p in products:
        product_data = dict(p)
        options = conn.execute(
            "SELECT id, name, extra_price_cents FROM options WHERE product_id=?",
            (p["id"],)
        ).fetchall()
        product_data["options"] = [dict(o) for o in options]
        product_dicts.append(product_data)

    conn.close()
    return jsonify(product_dicts)

@app.route("/api/featured")
def api_featured():
    """Return the first 2 featured products (active only)."""
    conn = get_db_connection()
    products = conn.execute(
        "SELECT * FROM products WHERE is_active=1 ORDER BY id LIMIT 2"
    ).fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route("/api/product/<int:product_id>")
def api_product(product_id):
    """Return a single product (with options) by product_id."""
    conn = get_db_connection()
    product = conn.execute(
        "SELECT * FROM products WHERE id=? AND is_active=1", (product_id,)
    ).fetchone()

    if not product:
        conn.close()
        return jsonify({"error": "Product not found"}), 404

    options = conn.execute(
        "SELECT id, name, extra_price_cents FROM options WHERE product_id=?",
        (product_id,)
    ).fetchall()
    conn.close()

    product_dict = dict(product)
    product_dict["options"] = [dict(opt) for opt in options]
    return jsonify(product_dict)


# ================================
# ERROR HANDLERS
# ================================

@app.errorhandler(404)
def not_found(e):
    """Custom 404 page."""
    return render_template(
        "base.html", title="Not found", content="<p>Page not found.</p>"
    ), 404

# ================================
# DEBUGGING HELPERS: Print all routes
# ================================

def print_routes(app):
    print("\n=== Registered Routes ===")
    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        print(f"{rule.endpoint:25s} {methods:10s} {rule}")
    print("=========================\n")


# ================================
# RUN SERVER
# ================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Print all routes for debugging
    print_routes(app)
    # host=0.0.0.0 allows external access (needed for Replit, etc.)
    app.run(host="0.0.0.0", port=port, debug=True)
