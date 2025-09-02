How to update product images (one-pager)

Goal: upload real product photos into static/images/, update the DB so product.image_url points to /static/images/<file>, and keep db/seed.sql consistent for future reseeds.

Quick overview (one line): Upload photos to static/images/ → 2. Run the updater script → 3. Verify in browser → 4. Update db/seed.sql (optional) → 5. Commit & push.

Preparation — file naming rules (very important):
-Use lowercase, no spaces, use hyphens: banana-bread.jpg
-Use .jpg or .png (prefer .jpg for photos)
-Suggested sizes: 1200×800 (or 600×400) — you can resize later; keep aspect ratio -consistent
-Optimize/compress images (short term): use an online compressor before uploading

Step A — Upload files in Replit:

1. Open your Replit project.

2. In left Files panel, open static/images/.

3. Drag & drop your photos into that folder or right-click → Upload file.

4. Rename files to match names you want (e.g. banana-bread.jpg).

Step B — Updater script (safe, idempotent)

1. (completed 9/2) Place this script at scripts/update_images.py (create scripts/ folder if needed). It updates products.image_url to /static/images/<filename>:

2.
<python>
Allready pasted into file (completed 9/2)
<python>

Step C — Run the updater (in Replit Shell)

1. Optional DB backup:
<bash>
cp db/app.db db/app.backup.$(date +%Y%m%d%H%M).db
<bash>
2. Run updater:
python3 update_images.py
3. Output will list updated products and warn if any files are missing.

Step D — Verify everything:

1. Open your Replit preview or public Repl URL.
2. Browse /products and click a product — the product detail page should show the new photo.
3. Quick API check (browser): /api/product/<id> — ensure image_url shows /static/images/<filename>.

If an image is broken:
1. Confirm filename in static/images/ exactly matches IMAGE_MAP.
2. Confirm image_url returned by /api/product/<id> is /static/images/filename.
3. Clear browser cache (Shift+reload) or open in a private window.

Step F — Commit & push to GitHub

In Replit Version Control: write a commit message like Add real product photos + update DB.

Commit & Push to GitHub so your repo and team have the changes.


****images can only be .jpg****