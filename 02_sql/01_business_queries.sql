-- ============================================================
-- E-Commerce Order-to-Profitability & Delivery Intelligence
-- SQL Business Analysis
-- Database: ecommerce_intelligence
-- Author: Y. Himasri Swarna
-- ============================================================


-- ============================================================
-- 1. MONTHLY BUSINESS PERFORMANCE
-- ============================================================
-- Purpose: Analyze monthly orders, item value, freight cost, and contribution proxy.

SELECT
    order_month,
    COUNT(*) AS orders,
    ROUND(SUM(item_value), 2) AS item_value,
    ROUND(SUM(freight_value), 2) AS freight,
    ROUND(SUM(contribution_proxy), 2) AS contribution_proxy
FROM orders_master
GROUP BY order_month
ORDER BY order_month;


-- ============================================================
-- 2. DELIVERY PERFORMANCE BY CUSTOMER STATE
-- ============================================================
-- Purpose: Compare average delivery time and late delivery rate across customer states.
-- Only states with at least 100 delivered orders are included.

SELECT
    customer_state,
    COUNT(*) AS delivered_orders,
    ROUND(AVG(delivery_days), 2) AS avg_delivery_days,
    ROUND(100 * AVG(delivered_late), 2) AS late_rate_pct
FROM orders_master
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY customer_state
HAVING COUNT(*) >= 100
ORDER BY late_rate_pct DESC;


-- ============================================================
-- 3. DELIVERY DELAY VS CUSTOMER REVIEW SCORE
-- ============================================================
-- Purpose: Examine the association between delivery delay and average customer review score.
-- Delay buckets:
--   On or before estimate
--   1-3 days late
--   4-7 days late
--   8+ days late

SELECT
    CASE
        WHEN DATEDIFF(
            order_delivered_customer_date,
            order_estimated_delivery_date
        ) <= 0 THEN 'On or before estimate'

        WHEN DATEDIFF(
            order_delivered_customer_date,
            order_estimated_delivery_date
        ) <= 3 THEN '1-3 days late'

        WHEN DATEDIFF(
            order_delivered_customer_date,
            order_estimated_delivery_date
        ) <= 7 THEN '4-7 days late'

        ELSE '8+ days late'
    END AS delivery_bucket,

    COUNT(*) AS orders,

    ROUND(AVG(avg_review_score), 2) AS avg_review_score

FROM orders_master

WHERE avg_review_score IS NOT NULL
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL

GROUP BY delivery_bucket

ORDER BY
    CASE
        WHEN delivery_bucket = 'On or before estimate' THEN 1
        WHEN delivery_bucket = '1-3 days late' THEN 2
        WHEN delivery_bucket = '4-7 days late' THEN 3
        ELSE 4
    END;


-- ============================================================
-- 4. CATEGORY PERFORMANCE
-- ============================================================
-- Purpose: Identify product categories generating the highest contribution proxy.
-- Contribution Proxy = Item Value - Freight Value

SELECT
    product_category_name_english AS category,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(price), 2) AS item_value,
    ROUND(SUM(freight_value), 2) AS freight,
    ROUND(SUM(contribution_proxy), 2) AS contribution_proxy
FROM order_items_enriched
WHERE product_category_name_english IS NOT NULL
GROUP BY product_category_name_english
ORDER BY contribution_proxy DESC
LIMIT 15;


-- ============================================================
-- 5. SELLER PERFORMANCE
-- ============================================================
-- Purpose: Identify sellers with strong contribution proxy while requiring a minimum order volume of 20 orders.

SELECT
    seller_id,
    seller_state,
    COUNT(DISTINCT order_id) AS orders,
    ROUND(SUM(price), 2) AS item_value,
    ROUND(SUM(freight_value), 2) AS freight,
    ROUND(SUM(contribution_proxy), 2) AS contribution_proxy
FROM order_items_enriched
GROUP BY seller_id, seller_state
HAVING COUNT(DISTINCT order_id) >= 20
ORDER BY contribution_proxy DESC
LIMIT 20;


-- ============================================================
-- 6. MONTH-OVER-MONTH ITEM VALUE GROWTH
-- ============================================================
-- Purpose: Calculate monthly item value and its percentage change compared with the previous month.

WITH monthly AS (
    SELECT
        order_month AS month,
        SUM(item_value) AS item_value
    FROM orders_master
    GROUP BY order_month
),

previous_month AS (
    SELECT
        month,
        item_value,
        LAG(item_value) OVER (
            ORDER BY month
        ) AS previous_value
    FROM monthly
)

SELECT
    month,
    ROUND(item_value, 2) AS item_value,
    ROUND(previous_value, 2) AS previous_value,

    ROUND(
        100 * (item_value - previous_value)
        / NULLIF(previous_value, 0),
        2
    ) AS mom_growth_pct

FROM previous_month

ORDER BY month;


-- ============================================================
-- 7. ORDER STATUS DISTRIBUTION
-- ============================================================
-- Purpose: Understand the distribution of orders across different order statuses.

SELECT
    order_status,
    COUNT(*) AS orders,

    ROUND(
        100 * COUNT(*)
        / SUM(COUNT(*)) OVER (),
        2
    ) AS order_pct

FROM orders_master

GROUP BY order_status

ORDER BY orders DESC;


-- ============================================================
-- END OF SQL BUSINESS ANALYSIS
-- ============================================================

-- Important business assumption:

-- The Olist dataset does not contain actual product COGS.
-- Therefore, true profit cannot be calculated.

-- Contribution Proxy =
-- Item Value - Freight Value

-- This metric should NOT be interpreted as actual profit.