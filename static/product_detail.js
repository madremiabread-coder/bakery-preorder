// --- Add selected product (and option) to basket ---
function addToCart(product) {
  let cart = JSON.parse(localStorage.getItem("cart")) || []; // --- Load basket from localStorage ---

  // --- Get selected option (radio button), if any ---
  const selectedRadio = document.querySelector('input[name="option"]:checked');
  let option = null;

  if (selectedRadio) {
    option = {
      id: parseInt(selectedRadio.value),
      name: selectedRadio.dataset.name, // --- Safer: pulled from dataset, not DOM text ---
      extra_price_cents: parseInt(selectedRadio.dataset.price),
    };
  }

  // --- Build basket item ---
  let item = {
    id: product.id,
    name: product.name,
    base_price_cents: product.price_cents,
    option: option,
    quantity: 1,
    total_price_cents: product.price_cents + (option ? option.extra_price_cents : 0),
  };

  // --- Check if same item already exists in basket (same product + option) ---
  const existingIndex = cart.findIndex(
    (i) => i.id === item.id && JSON.stringify(i.option) === JSON.stringify(item.option)
  );

  if (existingIndex >= 0) {
    // --- If item already in basket → increase quantity ---
    cart[existingIndex].quantity += 1;
    cart[existingIndex].total_price_cents += item.total_price_cents;
  } else {
    // --- Otherwise → add new item ---
    cart.push(item);
  }

  // --- Save updated basket ---
  localStorage.setItem("cart", JSON.stringify(cart));

  // --- Show confirmation message ---
  alert("Added to Basket!");
}

// --- Fetch product details dynamically ---
async function loadProduct(productId) {
  try {
    const res = await fetch(`/api/product/${productId}`); // --- Get product + options from backend ---
    if (!res.ok) {
      document.getElementById("product-detail").innerHTML =
        "<p class='text-red-600'>Failed to load product.</p>";
      return;
    }

    const product = await res.json();

    // --- Build options list (radio buttons so only one can be selected) ---
    let optionsHtml = "";
    if (product.options && product.options.length > 0) {
      optionsHtml = `<div class="mt-4"><p class="font-semibold mb-2">Choose an option:</p>`;
      product.options.forEach((opt) => {
        optionsHtml += `
          <label class="block">
            <input type="radio" name="option" value="${opt.id}" 
                   data-name="${opt.name}" 
                   data-price="${opt.extra_price_cents}">
            ${opt.name} (+$${(opt.extra_price_cents / 100).toFixed(2)})
          </label>`;
      });
      optionsHtml += `</div>`;
    }

    // --- Render product details on page ---
    document.getElementById("product-detail").innerHTML = `
      <h1 class="text-3xl font-bold mb-4">${product.name}</h1>
      <img src="${product.image_url}" alt="${product.name}" 
           class="w-64 h-64 object-cover rounded mb-4">
      <p class="mb-2">$${(product.price_cents / 100).toFixed(2)}</p>
      ${optionsHtml}
      <button onclick='addToCart(${JSON.stringify(product)})' 
              class="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Add to Basket
      </button>
    `;

  } catch (err) {
    document.getElementById("product-detail").innerHTML =
      "<p class='text-red-600'>Error loading product.</p>";
  }
}

// --- Auto-load product when page loads ---
document.addEventListener("DOMContentLoaded", () => {
  const productId = window.location.pathname.split("/").pop(); // --- Get productId from URL ---
  loadProduct(productId);
});

