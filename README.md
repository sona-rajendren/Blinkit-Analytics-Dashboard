Blinkit Analytics Dashboard
Interactive dashboard built from the Blinkit marketing and customer-analytics tables (orders, order items, products, customers, delivery, feedback, marketing, inventory).

Structure
blinkit-analytics-dashboard/
├── data/
│   ├── raw/                  original CSV/XLSX files (do not edit)
│   └── orders_enriched.csv   one row per order, all tables joined (made by src/analysis.py)
├── src/analysis.py           joins tables, KPIs, summary CSVs, PNG charts, dashboard/data.js
├── dashboard/
│   ├── index.html            dashboard: Overview, Delivery, Feedback, Marketing, Inventory
│   └── data.js               generated data for the dashboard
├── sql/queries.sql           9 queries (tested in SQLite)
├── outputs/                  summary tables and charts
└── requirements.txt
Run it
pip install pandas numpy matplotlib
python src/analysis.py        # rebuilds everything from data/raw
# then double-click dashboard/index.html (internet needed for Chart.js and fonts)
How the tables join
orders → order_items (order_id) → products (product_id); orders → customers (customer_id); orders → delivery_performance and customer_feedback (order_id). Every join was checked: all keys match and each order appears once. marketing_performance has no order or customer key, and inventory links to products only, so those two tabs stand alone.

Data notes (read before presenting findings)
Each order has exactly one item, and order_total does not equal quantity × unit_price. Revenue in the dashboard uses order_total.
Delivery reasons_if_delayed only ever contains "Traffic" (or blank, including for some on-time orders), so it is not charted.
In the inventory file, damaged stock is about half of stock received, which is unrealistically high. Treat the inventory tab as a demonstration, not a real finding.
blinkit_inventoryNew.csv is a monthly roll-up of the inventory table and is not used.
Category_Icons.xlsx and Rating_Icon.xlsx hold icon image links for Power BI and are not used here.
Several relationships look flat (for example delivery distance vs on-time rate, and rating vs delivery status), which suggests the data is partly synthetic. Report what the charts show, but do not over-interpret them.
