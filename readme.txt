Workflow for adding and editing prodicts:
1. Want to change the schema? Edit db/schema.sql.
2. Want to add or update products/options? Edit db/seed.sql.
3. Reset your database by running in "python3 seed.py" - This wipes your products and options tables, re-creates them, and inserts your updated data.

Structure for SQL:
db/schema.sql → Defines tables (structure only, no rows).
db/seed.sql → Contains all your product + option data in plain SQL INSERT statements.
seed.py → A very small script that just reads both files and executes them.

That way:
If you want to add “Pumpkin Spice Sourdough,” you only touch seed.sql.
If you later add a new table like orders, you only touch schema.sql.
You never duplicate the schema logic across multiple places.


Git version control:
1. You’ll see a list of changed files.
2. In the Commit message box, write something meaningful like:
"Initial project setup"
"Added product_detail.js"
"Fix: basket totals not updating"

3. Click Commit.
4. Then click Push (this sends your commit to GitHub).