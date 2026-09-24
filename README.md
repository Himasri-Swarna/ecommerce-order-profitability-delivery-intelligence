E-Commerce Order-to-Profitability & Delivery Intelligence

📌 Project Overview
Analyzed the Brazilian E-Commerce Public Dataset (Olist) to understand
order performance, contribution proxy, delivery efficiency, customer
satisfaction, seller performance, and category performance.

🎯 Business Questions

- Which categories generate the highest contribution proxy?
- Which sellers and seller states contribute most?
- Which states experience higher delivery delays?
- How does delivery delay relate to customer review scores?
- How does item value and freight cost change over time?

🛠️ Tools & Technologies

- Python
- Pandas
- NumPy
- MySQL
- SQL
- Power BI
- DAX
- Excel/CSV

📊 Key Metrics

- Total Orders: 99,441
- Item Value: 13.59M
- Freight Cost: 2.25M
- Contribution Proxy: 11.34M
- Average Review Score: 4.09
- Late Delivery Rate: 6.8%

🔍 Key Findings

1. Delivery delays are strongly associated with lower review scores.
2. Categories differ significantly in contribution proxy and freight cost.
3. Delivery performance varies across customer states.
4. Seller performance varies substantially across seller states.
5. Monthly item value shows noticeable changes over the observed period.

⚠️ Important Business Assumption
The dataset does not contain actual product cost/COGS.
Therefore:

Contribution Proxy = Item Value − Freight Value

This should NOT be interpreted as true profit.

📁 Project Structure

- `01_data` — Raw and processed datasets
- `02_sql` — SQL analysis queries
- `03_python` — Data processing scripts
- `04_eda` — Exploratory data analysis
- `05_powerbi` — Power BI dashboard
- `06_docs` — Documentation
- `07_outputs` — Results and exports
- `08_README.md` — Project documentation
- `09_requirements.txt` — Python dependencies
