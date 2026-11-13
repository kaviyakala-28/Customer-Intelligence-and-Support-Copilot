
-- Q1: Customers with high-value completed orders
SELECT customer_id, SUM(order_amount) AS total_spend
FROM orders
WHERE status = 'completed' AND order_amount > 500
GROUP BY customer_id
HAVING SUM(order_amount) > 8000;


-- Q2: Revenue by city and product category
SELECT c.city, p.category,
       ROUND(SUM(o.order_amount), 2) AS total_revenue
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p ON o.product_id = p.product_id
WHERE o.status = 'completed'
GROUP BY c.city, p.category
ORDER BY c.city, p.category;


-- Q3: Products priced above the average catalogue price
SELECT product_id, product_name, price_inr
FROM products
WHERE price_inr > (SELECT AVG(price_inr) FROM products)
ORDER BY price_inr DESC;


-- Q4: Customers without completed orders
SELECT c.customer_id, c.city
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
    AND o.status = 'completed'
WHERE o.order_id IS NULL;


-- Q5: Customers spending above the average
WITH customer_spend AS (
    SELECT customer_id, SUM(order_amount) AS total_spend
    FROM orders
    WHERE status = 'completed'
    GROUP BY customer_id
)
SELECT customer_id, ROUND(total_spend, 2) AS total_spend
FROM customer_spend
WHERE total_spend > (SELECT AVG(total_spend) FROM customer_spend)
ORDER BY total_spend DESC;


-- Q6: Customer spending rankings within each city
WITH customer_spend AS (
    SELECT c.city, o.customer_id,
           SUM(o.order_amount) AS total_spend
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.status = 'completed'
    GROUP BY c.city, o.customer_id
),
ranked_customers AS (
    SELECT *,
           RANK() OVER (
               PARTITION BY city ORDER BY total_spend DESC
           ) AS spend_rank,
           DENSE_RANK() OVER (
               PARTITION BY city ORDER BY total_spend DESC
           ) AS dense_rank,
           ROW_NUMBER() OVER (
               PARTITION BY city ORDER BY total_spend DESC
           ) AS row_num
    FROM customer_spend
)
SELECT city, customer_id, ROUND(total_spend, 2) AS total_spend,
       spend_rank, dense_rank, row_num
FROM ranked_customers
ORDER BY city, row_num;


-- Q7: Daily revenue and running cumulative revenue
WITH daily_revenue AS (
    SELECT DATE(order_ts) AS order_date,
           SUM(order_amount) AS daily_revenue
    FROM orders
    WHERE status = 'completed'
    GROUP BY DATE(order_ts)
)
SELECT order_date,
       ROUND(daily_revenue, 2) AS daily_revenue,
       ROUND(
           SUM(daily_revenue) OVER (ORDER BY order_date), 2
       ) AS cumulative_revenue
FROM daily_revenue
ORDER BY order_date;
