// ======================================================
// Madre Mia! Bread - Cart Logic
// Handles rendering, removing, clearing, and checkout
// ======================================================

// 🔹 Render the basket on page load
function renderCart() {
  // Load basket from localStorage (or start empty)
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  const container = document.getElementById("cart-container");

  // If no items → show empty basket message
  if (cart.length === 0) {
    container.innerHTML = `<p class="muted">Your basket is empty 🧺</p>`;
    return;
  }

  let totalCents = 0;

  // Start building basket table
  let html = `
    <table class="cart-table">
      <thead>
        <tr>
          <th>Item</th>
          <th>Qty</th>
          <th>Price</th>
          <th>Total</th>
          <th></th> <!-- column for remove button -->
        </tr>
      </thead>
      <tbody>
  `;

  // Loop through basket items
  cart.forEach((item, index) => {
    const optionText = item.option
      ? ` <span class="small muted">(${item.option.name})</span>`
      : "";

    const itemTotal = item.total_price_cents;
    totalCents += itemTotal;

    html += `
      <tr>
        <td>${item.name}${optionText}</td>
        <td>${item.quantity}</td>
        <td>$${(
          (item.base_price_cents + (item.option?.extra_price_cents || 0)) / 100
        ).toFixed(2)}</td>
        <td>$${(itemTotal / 100).toFixed(2)}</td>
        <td>
          <button onclick="removeFromCart(${index})" class="btn btn-remove">
            Remove
          </button>
        </td>
      </tr>
    `;
  });

  // Close table
  html += `</tbody></table>`;

  // Add totals + actions
  html += `
    <div class="cart-summary">
      <p class="cart-total">Grand Total: $${(totalCents / 100).toFixed(2)}</p>
      <div class="cart-actions">
        <button onclick="clearCart()" class="btn">Clear Basket</button>
        <button onclick="checkout()" class="btn btn-primary">Checkout</button>
      </div>
    </div>
  `;

  // Render all into container
  container.innerHTML = html;
}

// 🔹 Remove a single item by index
function removeFromCart(index) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.splice(index, 1); // remove item
  localStorage.setItem("cart", JSON.stringify(cart)); // save updated basket
  renderCart(); // re-render
}

// 🔹 Clear the entire basket
function clearCart() {
  localStorage.removeItem("cart");
  renderCart();
}

// 🔹 Placeholder for checkout flow
function checkout() {
  alert("Checkout flow coming soon!");
}

// 🔹 Initial render when page loads
renderCart();


