import pandas as pd
from pathlib import Path

# ============================================================
# 1. FILE LOCATIONS
# ============================================================

raw = Path("01_data/01_raw")
processed = Path("01_data/02_processed")

processed.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. LOAD DATASETS
# ============================================================

orders = pd.read_csv(raw / "olist_orders_dataset.csv")
customers = pd.read_csv(raw / "olist_customers_dataset.csv")
items = pd.read_csv(raw / "olist_order_items_dataset.csv")
payments = pd.read_csv(raw / "olist_order_payments_dataset.csv")
reviews = pd.read_csv(raw / "olist_order_reviews_dataset.csv")
products = pd.read_csv(raw / "olist_products_dataset.csv")
sellers = pd.read_csv(raw / "olist_sellers_dataset.csv")
translation = pd.read_csv(raw / "product_category_name_translation.csv")


# ============================================================
# 3. CONVERT ORDER DATES
# ============================================================

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")


# ============================================================
# 4. AGGREGATE ORDER ITEMS
#    One order can contain multiple items.
# ============================================================

items_order = (
    items.groupby("order_id")
    .agg(
        item_count=("order_item_id", "count"),
        item_value=("price", "sum"),
        freight_value=("freight_value", "sum")
    )
    .reset_index()
)


# ============================================================
# 5. AGGREGATE PAYMENTS
#    One order can have multiple payment records.
# ============================================================

payments_order = (
    payments.groupby("order_id")
    .agg(
        payment_value=("payment_value", "sum")
    )
    .reset_index()
)


# ============================================================
# 6. AGGREGATE REVIEWS
#    One order can have multiple review records.
# ============================================================

reviews_order = (
    reviews.groupby("order_id")
    .agg(
        avg_review_score=("review_score", "mean")
    )
    .reset_index()
)


# ============================================================
# 7. ADD CUSTOMER INFORMATION
# ============================================================

customer_info = customers[
    [
        "customer_id",
        "customer_unique_id",
        "customer_city",
        "customer_state"
    ]
].copy()


# ============================================================
# 8. MERGE EVERYTHING AT ORDER LEVEL
# ============================================================

orders_master = orders.merge(
    customer_info,
    on="customer_id",
    how="left"
)

orders_master = orders_master.merge(
    items_order,
    on="order_id",
    how="left"
)

orders_master = orders_master.merge(
    payments_order,
    on="order_id",
    how="left"
)

orders_master = orders_master.merge(
    reviews_order,
    on="order_id",
    how="left"
)


# ============================================================
# 9. FILL VALUES FOR ORDERS WITHOUT ITEMS/PAYMENTS/REVIEWS
# ============================================================

orders_master["item_count"] = orders_master["item_count"].fillna(0)
orders_master["item_value"] = orders_master["item_value"].fillna(0)
orders_master["freight_value"] = orders_master["freight_value"].fillna(0)
orders_master["payment_value"] = orders_master["payment_value"].fillna(0)


# ============================================================
# 10. CONTRIBUTION PROXY
#
# NOTE:
# This is NOT true profit because the dataset does not contain
# product cost/COGS.
#
# Contribution Proxy = Item Value - Freight
# ============================================================

orders_master["contribution_proxy"] = (
    orders_master["item_value"]
    - orders_master["freight_value"]
)


# ============================================================
# 11. DELIVERY DAYS
# ============================================================

orders_master["delivery_days"] = (
    orders_master["order_delivered_customer_date"]
    - orders_master["order_purchase_timestamp"]
).dt.days


# ============================================================
# 12. DELIVERY DELTA
#
# Positive = delivered late
# Zero/negative = delivered on/before estimate
# ============================================================

orders_master["delivery_delta_days"] = (
    orders_master["order_delivered_customer_date"]
    - orders_master["order_estimated_delivery_date"]
).dt.days


# ============================================================
# 13. LATE DELIVERY FLAG
#
# 1 = Late
# 0 = Not late
#
# IMPORTANT:
# .astype(int) converts True/False into 1/0
# ============================================================

orders_master["delivered_late"] = (
    orders_master["delivery_delta_days"] > 0
).astype(int)


# ============================================================
# 14. ORDER MONTH
# ============================================================

orders_master["order_month"] = (
    orders_master["order_purchase_timestamp"]
    .dt.to_period("M")
    .astype(str)
)


# ============================================================
# 15. PURCHASE HOUR
# ============================================================

orders_master["purchase_hour"] = (
    orders_master["order_purchase_timestamp"]
    .dt.hour
)


# ============================================================
# 16. PURCHASE DAY OF WEEK
# ============================================================

orders_master["purchase_day"] = (
    orders_master["order_purchase_timestamp"]
    .dt.day_name()
)


# ============================================================
# 17. REORDER COLUMNS
# ============================================================

orders_master = orders_master[
    [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",

        "customer_unique_id",
        "customer_city",
        "customer_state",

        "item_count",
        "item_value",
        "freight_value",
        "contribution_proxy",
        "payment_value",
        "avg_review_score",

        "delivery_days",
        "delivery_delta_days",
        "delivered_late",

        "order_month",
        "purchase_hour",
        "purchase_day"
    ]
]


# ============================================================
# 18. SAVE PROCESSED DATA
# ============================================================

output_file = processed / "orders_master.csv"

orders_master.to_csv(
    output_file,
    index=False
)


# ============================================================
# 19. FINAL VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("SUCCESS!")
print("=" * 60)

print("Orders master rows:", len(orders_master))
print("Orders master columns:", len(orders_master.columns))

print("\nOutput file:")
print(output_file)

print("\nDelivered late values:")
print(orders_master["delivered_late"].value_counts(dropna=False))

print("\nFirst 5 rows:")
print(orders_master.head())