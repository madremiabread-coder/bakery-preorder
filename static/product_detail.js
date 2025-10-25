// ===============================
// ✅ Add selected product to basket
// ===============================
function addToCart(product) {
  // Load existing basket (or start empty)
  let cart = JSON.parse(localStorage.getItem("cart")) || [];

  // --- Get selected option (radio button), if any ---
  const selectedRadio = document.querySelector('input[name="option"]:checked');
  let option = null;

  if (selectedRadio) {
    option = {
      id: parseInt(selectedRadio.value),
      name: selectedRadio.dataset.name,
      extra_price_cents: parseInt(selectedRadio.dataset.price),
    };
  }

  // --- Build new basket item ---
  let item = {
    id: product.id,
    name: product.name,
    base_price_cents: product.price_cents,
    option: option,
    quantity: 1,
    total_price_cents:
      product.price_cents + (option ? option.extra_price_cents : 0),
  };

  // --- Check if same product+option already exists ---
  const existingIndex = cart.findIndex(
    (i) =>
      i.id === item.id &&
      JSON.stringify(i.option) === JSON.stringify(item.option)
  );

  if (existingIndex >= 0) {
    // If found → increment quantity + total
    cart[existingIndex].quantity += 1;
    cart[existingIndex].total_price_cents += item.total_price_cents;
  } else {
    // Otherwise → add new entry
    cart.push(item);
  }

  // Save updated basket back to localStorage
  localStorage.setItem("cart", JSON.stringify(cart));

  // Simple confirmation (later we could do a toast UI)
  alert("✅ Added to Basket!");
}

// ===============================
// ✅ Fetch product details + render on page
// ===============================
async function loadProduct(productId) {
  try {
    // --- Request product data from backend ---
    const res = await fetch(`/api/product/${productId}`);
    if (!res.ok) {
      document.getElementById("product-detail").innerHTML =
        "<p class='text-red-600'>Failed to load product.</p>";
      return;
    }

    const product = await res.json();

    // --- Fill in left column: product image ---
    const mediaContainer = document.querySelector("#product-detail .media");
    mediaContainer.innerHTML = product.image_url
      ? `<img src="${product.image_url}" alt="${product.name}" />`
      : "<p>No image available</p>";

    // --- Fill in right column: title, desc, price ---
    const infoContainer = document.querySelector("#product-detail .info");
    infoContainer.querySelector("h1").textContent = product.name;
    infoContainer.querySelector(".desc").textContent =
      product.description || "No description available.";
    infoContainer.querySelector(".price").textContent =
      `$${(product.price_cents / 100).toFixed(2)}`;

    // --- Build options (radio buttons if available) ---
    let optionsHtml = "";
    if (product.options && product.options.length > 0) {
      optionsHtml = `<div class="mt-4"><p><strong>Choose an option:</strong></p>`;
      product.options.forEach((opt) => {
        optionsHtml += `
          <label>
            <input type="radio" name="option" value="${opt.id}"
                   data-name="${opt.name}"
                   data-price="${opt.extra_price_cents}">
            ${opt.name} (+$${(opt.extra_price_cents / 100).toFixed(2)})
          </label><br>`;
      });
      optionsHtml += `</div>`;
    }
    document.getElementById("product-options").innerHTML = optionsHtml;

    // --- Hook up the Add to Basket button ---
    const addButton = document.getElementById("add-to-cart");
    addButton.disabled = false; // Enable it now that data is loaded
    addButton.onclick = () => addToCart(product);
  } catch (err) {
    console.error("Error loading product:", err);
    document.getElementById("product-detail").innerHTML =
      "<p class='text-red-600'>Error loading product.</p>";
  }
}

// ===============================
// ✅ Auto-run on page load
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  // Get productId from URL (last segment after /product/)
  const productId = window.location.pathname.split("/").pop();
  loadProduct(productId);
});


