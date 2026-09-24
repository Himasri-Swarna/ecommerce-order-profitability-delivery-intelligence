import pandas as pd
from pathlib import Path

# 1. File locations
raw = Path("01_data/01_raw")
processed = Path("01_data/02_processed")

# 2. Load datasets
items = pd.read_csv(raw / "olist_order_items_dataset.csv")
products = pd.read_csv(raw / "olist_products_dataset.csv")
sellers = pd.read_csv(raw / "olist_sellers_dataset.csv")
translation = pd.read_csv(raw / "product_category_name_translation.csv")

# 3. Add English category name
products = products.merge(
    translation,
    on="product_category_name",
    how="left"
)

# 4. Add product category to order items
items = items.merge(
    products[["product_id", "product_category_name_english"]],
    on="product_id",
    how="left"
)

# 5. Add seller location
items = items.merge(
    sellers[["seller_id", "seller_state"]],
    on="seller_id",
    how="left"
)

# 6. Calculate contribution proxy
items["contribution_proxy"] = (
    items["price"] - items["freight_value"]
)

# 7. Select useful columns
items_enriched = items[
    [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "product_category_name_english",
        "seller_state",
        "price",
        "freight_value",
        "contribution_proxy"
    ]
]

# 8. Save processed file
processed.mkdir(parents=True, exist_ok=True)

output = processed / "order_items_enriched.csv"
items_enriched.to_csv(output, index=False)

print("SUCCESS!")
print("Rows:", len(items_enriched))
print("Columns:", len(items_enriched.columns))
print("Saved to:", output)
print("\nFirst 5 rows:")
print(items_enriched.head())