-- Blinkit analytics queries (SQLite syntax; works in MySQL/PostgreSQL with minor date-function changes).
-- Load each CSV in data/raw/ into a table with the same name without ".csv"
-- (blinkit_orders, blinkit_order_items, blinkit_products, blinkit_customers,
--  blinkit_delivery_performance, blinkit_customer_feedback, blinkit_marketing_performance, blinkit_inventory).

-- 1. Headline KPIs
SELECT COUNT(*) AS orders, ROUND(SUM(order_total),2) AS revenue, ROUND(AVG(order_total),2) AS avg_order_value,
       ROUND(100.0*SUM(delivery_status='On Time')/COUNT(*),1) AS on_time_pct
FROM blinkit_orders;

-- 2. Revenue and orders by month
SELECT SUBSTR(order_date,1,7) AS month, COUNT(*) AS orders, ROUND(SUM(order_total),2) AS revenue
FROM blinkit_orders GROUP BY 1 ORDER BY 1;

-- 3. Revenue by product category
SELECT p.category, COUNT(*) AS orders, ROUND(SUM(o.order_total),2) AS revenue
FROM blinkit_orders o
JOIN blinkit_order_items oi ON oi.order_id = o.order_id
JOIN blinkit_products p ON p.product_id = oi.product_id
GROUP BY p.category ORDER BY revenue DESC;

-- 4. Top 10 products by revenue
SELECT p.product_name, ROUND(SUM(o.order_total),2) AS revenue
FROM blinkit_orders o
JOIN blinkit_order_items oi ON oi.order_id = o.order_id
JOIN blinkit_products p ON p.product_id = oi.product_id
GROUP BY p.product_name ORDER BY revenue DESC LIMIT 10;

-- 5. Revenue by customer segment
SELECT c.customer_segment, COUNT(*) AS orders, ROUND(SUM(o.order_total),2) AS revenue
FROM blinkit_orders o JOIN blinkit_customers c ON c.customer_id = o.customer_id
GROUP BY 1 ORDER BY revenue DESC;

-- 6. Delivery status with average delay and rating
SELECT o.delivery_status, COUNT(*) AS orders, ROUND(AVG(d.delivery_time_minutes),2) AS avg_delay_min,
       ROUND(AVG(f.rating),2) AS avg_rating
FROM blinkit_orders o
JOIN blinkit_delivery_performance d ON d.order_id = o.order_id
JOIN blinkit_customer_feedback f ON f.order_id = o.order_id
GROUP BY 1;

-- 7. Feedback topics by sentiment
SELECT feedback_category, sentiment, COUNT(*) AS responses
FROM blinkit_customer_feedback GROUP BY 1,2 ORDER BY 1,2;

-- 8. Marketing: ROAS by campaign
SELECT campaign_name, ROUND(SUM(spend),2) AS spend, ROUND(SUM(revenue_generated),2) AS revenue,
       ROUND(SUM(revenue_generated)/SUM(spend),2) AS roas,
       ROUND(100.0*SUM(conversions)/SUM(clicks),2) AS conv_rate_pct
FROM blinkit_marketing_performance GROUP BY 1 ORDER BY roas DESC;

-- 9. Inventory: damage rate by category (dates in blinkit_inventory are dd-mm-yyyy text)
SELECT p.category, SUM(i.stock_received) AS received, SUM(i.damaged_stock) AS damaged,
       ROUND(100.0*SUM(i.damaged_stock)/SUM(i.stock_received),2) AS damage_rate_pct
FROM blinkit_inventory i JOIN blinkit_products p ON p.product_id = i.product_id
GROUP BY 1 ORDER BY damage_rate_pct DESC;
