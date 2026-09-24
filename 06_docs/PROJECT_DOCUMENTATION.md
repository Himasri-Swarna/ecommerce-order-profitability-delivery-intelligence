E-Commerce Order-to-Profitability & Delivery Intelligence

1. Project Objective

Analyze e-commerce order data to understand:

- Order and item-value performance
- Freight cost and contribution proxy
- Delivery performance
- Customer review patterns
- Seller performance
- Product category performance

2. Dataset

Dataset: Brazilian E-Commerce Public Dataset by Olist.

The project uses 9 CSV files covering:

- Customers
- Orders
- Order items
- Payments
- Reviews
- Products
- Sellers
- Geolocation
- Product category translation

3. Data Processing

Python was used to:

1. Inspect the raw datasets.
2. Check missing values and duplicates.
3. Convert date columns to datetime.
4. Aggregate order items to order level.
5. Aggregate payment information.
6. Aggregate review scores.
7. Calculate delivery duration.
8. Calculate delivery delay.
9. Create a delivered-late flag.
10. Create contribution proxy metrics.
11. Generate processed datasets for SQL and Power BI.

12. SQL Analysis

MySQL was used to analyze:

- Monthly business performance
- Delivery performance by customer state
- Delivery delay vs review score
- Category performance
- Seller performance
- Month-over-month growth
- Order status distribution

5. Power BI Dashboard

The dashboard contains three pages:

### Page 1 — Executive Overview

Includes:

- Total Orders
- Item Value
- Freight Cost
- Contribution Proxy
- Average Review Score
- Late Delivery Rate
- Monthly Item Value Trend
- Top 10 Categories by Contribution Proxy
- Late Delivery Rate by State
- Delivery Delay vs Review Score
- Order Month, Customer State and Order Status filters

### Page 2 — Delivery Intelligence

Includes:

- Average Delivery Days
- Average Delivery Days by State
- Late Delivery Rate by State
- Delivery Delay vs Review Score
- Order Distribution by Delivery Days
- Order Status Distribution

### Page 3 — Seller & Category Intelligence

Includes:

- Top 10 Sellers by Contribution Proxy
- Top 10 Categories by Item Value
- Contribution Proxy by Seller State
- Top 10 Categories by Freight Cost
- Orders by Seller State

6. Key Metrics

- Total Orders: 99,441
- Item Value: 13.59M
- Freight Cost: 2.25M
- Contribution Proxy: 11.34M
- Average Review Score: 4.09
- Late Delivery Rate: 6.8%

7.  Key Findings

### Delivery and Customer Experience

Orders delivered later than the estimated delivery date show lower average review scores. The relationship becomes more pronounced as the delay increases.

This represents an observed association and should not be interpreted as proof that delivery delay directly causes lower ratings.

### Category Performance

Product categories vary substantially in item value, freight cost and contribution proxy.

### Seller Performance

Seller contribution and order volume vary across individual sellers and seller states.

### Delivery Performance

Delivery duration and late-delivery rates vary across customer states.

8. Contribution Proxy Definition

The dataset does not provide actual product cost or COGS.

Therefore:

Contribution Proxy = Item Value − Freight Value

This metric is a proxy and must not be interpreted as actual accounting profit.

9. Limitations

- Actual product COGS is unavailable.
- Marketing and advertising costs are unavailable.
- Returns and refunds are not modeled as a separate profitability adjustment.
- Seller IDs are anonymous.
- Delivery-delay analysis shows association rather than causation.
- Missing delivery dates limit some delivery analyses.

10. Tools Used

- Python
- Pandas
- NumPy
- Matplotlib
- MySQL
- SQL
- Power BI
- DAX
- Git/GitHub
