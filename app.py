import os
from flask import Flask, render_template, abort
from utils.db import init_db, get_db, query_db, close_db

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-not-secret")

# --- Database lifecycle ---
# Run once at startup
with app.app_context():
    init_db(app)

@app.teardown_appcontext
def _teardown_db(exception):
    close_db(exception)

# --- Jinja filters/util ---
def cents_to_dollars(cents):
    return f"${cents/100:.2f}"

app.jinja_env.filters["currency"] = cents_to_dollars

# --- Routes (Task 12) ---
@app.route("/")
def home():
    # Show a few featured products
    featured = query_db(
        "SELECT id, name, price_cents, description, image_url FROM products WHERE is_active=1 ORDER BY id LIMIT 2"
    )
    return render_template("home.html", featured=featured)

@app.route("/products")
def products():
    items = query_db(
        "SELECT id, name, price_cents, description, image_url FROM products WHERE is_active=1 ORDER BY id"
    )
    return render_template("products.html", products=items)

@app.route("/product/<int:product_id>")
def product_detail(product_id):
    product = query_db(
        "SELECT id, name, price_cents, description, image_url FROM products WHERE id=? AND is_active=1",
        (product_id,),
        one=True,
    )
    if not product:
        abort(404)
    return render_template("product_detail.html", product=product)

# --- Error pages (simple) ---
@app.errorhandler(404)
def not_found(e):
    return render_template("base.html", title="Not found", content="<p>Page not found.</p>"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    