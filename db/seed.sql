-- Products + Options Seed Data (with image URLs)

-- 1. Banana bread
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Organic Sourdough Banana Bread',
    900,
    'Moist, keto-friendly, sourdough banana bread, customizable with add-ons.',
    'https://placehold.co/600x400?text=Banana+Bread'
);
INSERT INTO options (product_id, name, extra_price_cents) VALUES
    ((SELECT id FROM products WHERE name='Organic Sourdough Banana Bread'), 'Dark Chocolate Chips', 100),
    ((SELECT id FROM products WHERE name='Organic Sourdough Banana Bread'), 'Pecans', 150),
    ((SELECT id FROM products WHERE name='Organic Sourdough Banana Bread'), 'Protein', 200);

-- 2. Chocolate Sourdough Birote (Guadalajara)
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Chocolate Sourdough Birote',
    600,
    'Rich, moist, and decadent chocolate sourdough bread made just like in Guadalajara, Mexico.',
    'https://placehold.co/600x400?text=Chocolate+Birote'
);

-- 3. Sourdough Birote (Guadalajara)
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Sourdough Birote',
    500,
    'Crunchy, darkly baked sourdough bread made just like in Guadalajara, Mexico.',
    'https://placehold.co/600x400?text=Sourdough+Birote'
);

-- 4. Sourdough Country Loaf
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Sourdough Country Loaf',
    1300,
    'A rustic, hearty sourdough loaf perfect for sandwiches and toast.',
    'https://placehold.co/600x400?text=Country+Loaf'
);

-- 5. Sourdough Focaccia (Plain)
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Sourdough Focaccia (Plain)',
    1000,
    'A crispy, airy sourdough focaccia perfect for dipping in sauces or spreading with cheese.',
    'https://placehold.co/600x400?text=Plain+Focaccia'
);

-- 6. Sourdough Focaccia (Savory)
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Sourdough Focaccia (Savory)',
    1000,
    'A crispy, airy sourdough focaccia customizable with add-ons.',
    'https://placehold.co/600x400?text=Savory+Focaccia'
);
INSERT INTO options (product_id, name, extra_price_cents) VALUES
    ((SELECT id FROM products WHERE name='Sourdough Focaccia (Savory)'), 'Salsa Macha and Cheese', 200),
    ((SELECT id FROM products WHERE name='Sourdough Focaccia (Savory)'), 'Cherry Tomatoes and Basil', 200),
    ((SELECT id FROM products WHERE name='Sourdough Focaccia (Savory)'), 'Herbs de Provence and Sea Salt', 150);

-- 7. Sourdough Focaccia (Sweet)
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Sourdough Focaccia (Sweet)',
    1000,
    'A crispy, airy sourdough focaccia customizable with add-ons.',
    'https://placehold.co/600x400?text=Sweet+Focaccia'
);
INSERT INTO options (product_id, name, extra_price_cents) VALUES
    ((SELECT id FROM products WHERE name='Sourdough Focaccia (Sweet)'), 'Mascarpone Cheese and Berry Compote', 250),
    ((SELECT id FROM products WHERE name='Sourdough Focaccia (Sweet)'), 'Tamarindo', 200),
    ((SELECT id FROM products WHERE name='Sourdough Focaccia (Sweet)'), 'Horchata', 200),
    ((SELECT id FROM products WHERE name='Sourdough Focaccia (Sweet)'), 'Guava and Cheese', 250);

-- 8. Homemade Salsa Macha
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Homemade Salsa Macha',
    500,
    'A spicy, tangy salsa made with fresh tomatillos, onions, and cilantro.',
    'https://placehold.co/600x400?text=Salsa+Macha'
);

-- 9. Starter Kit
INSERT INTO products (name, price_cents, description, image_url) 
VALUES (
    'Starter Kit',
    1500,
    'Everything you need to start your own sourdough journey. Includes flour, water, and a starter.',
    'https://placehold.co/600x400?text=Starter+Kit'
);

