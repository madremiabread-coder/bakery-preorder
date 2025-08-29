// --- Render the basket on page load ---
function renderCart() {
  let cart = JSON.parse(localStorage.getItem("cart")) || []; // --- Load basket from localStorage ---
  const container = document.getElementById("cart-container");

  // --- Show empty basket message if no items ---
  if (cart.length === 0) {
    container.innerHTML = `<p class="text-gray-600">Basket is empty :( </p>`;
    return;
  }

  let totalCents = 0;

  // --- Start building basket table ---
  let html = `<table class="w-full border-collapse">
                <thead>
                  <tr class="border-b text-left">
                    <th class="py-2">Item</th>
                    <th class="py-2">Qty</th>
                    <th class="py-2">Price</th>
                    <th class="py-2">Total</th>
                  </tr>
                </thead>
                <tbody>`;

  // --- Loop through items in basket ---
  cart.forEach((item, index) => {
    const optionText = item.option
      ? ` <span class="text-sm text-gray-500">(${item.option.name})</span>`
      : "";

    const itemTotal = item.total_price_cents;
    totalCents += itemTotal;

    html += `
      <tr class="border-b">
        <td class="py-2">${item.name}${optionText}</td>
        <td class="py-2">${item.quantity}</td>
        <td class="py-2">$${(
          (item.base_price_cents + (item.option?.extra_price_cents || 0)) /
          100
        ).toFixed(2)}</td>
        <td class="py-2">$${(itemTotal / 100).toFixed(2)}</td>
        <td class="py-2">
          <button onclick="removeFromCart(${index})" class="text-red-600 hover:underline">Remove</button>
        </td>
      </tr>
    `;
  });

  // --- Close table body ---
  html += `</tbody></table>`;

  // --- Add totals + action buttons (Clear / Checkout) ---
  html += `
    <div class="mt-6 text-right">
      <p class="text-xl font-semibold">Grand Total: $${(
        totalCents / 100
      ).toFixed(2)}</p>
      <div class="mt-4 flex justify-end gap-4">
        <button onclick="clearCart()" class="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600">Clear Basket</button>
        <button onclick="checkout()" class="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700">Checkout</button>
      </div>
    </div>
  `;

  // --- Render all content into container ---
  container.innerHTML = html;
}

// --- Remove a single item by index ---
function removeFromCart(index) {
  let cart = JSON.parse(localStorage.getItem("cart")) || [];
  cart.splice(index, 1); // --- Remove item from array ---
  localStorage.setItem("cart", JSON.stringify(cart)); // --- Save updated basket ---
  renderCart(); // --- Re-render basket ---
}

// --- Clear the entire basket ---
function clearCart() {
  localStorage.removeItem("cart"); // --- Delete storage key completely ---
  renderCart();
}

// --- Placeholder for checkout flow ---
function checkout() {
  alert("Checkout flow coming soon!");
}

// --- Initial render when page loads ---
renderCart();

