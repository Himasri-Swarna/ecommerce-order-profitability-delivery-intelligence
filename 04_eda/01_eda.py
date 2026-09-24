import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# E-COMMERCE ORDER-TO-PROFITABILITY & DELIVERY INTELLIGENCE
# PYTHON EDA
# ============================================================

print("=" * 60)
print("EDA STARTED")
print("=" * 60)


# ============================================================
# 1. LOAD PROCESSED DATA
# ============================================================

file_path = "01_data/02_processed/orders_master.csv"

df = pd.read_csv(file_path)

print("\nSUCCESSFULLY LOADED DATA")


# ============================================================
# 2. BASIC DATA INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("BASIC DATA INFORMATION")
print("=" * 60)

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())


# ============================================================
# 3. FIRST 5 ROWS
# ============================================================

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# 4. DATA TYPES
# ============================================================

print("\nData types:")
print(df.dtypes)


# ============================================================
# 5. MISSING VALUES
# ============================================================

print("\nMissing values:")
print(df.isnull().sum())


# ============================================================
# 6. DUPLICATES
# ============================================================

print("\nDuplicate rows:", df.duplicated().sum())


# ============================================================
# 7. BASIC STATISTICS
# ============================================================

print("\nNumerical summary:")
print(df.describe())


# ============================================================
# 8. DELIVERY PERFORMANCE
# ============================================================

print("\n" + "=" * 60)
print("DELIVERY PERFORMANCE")
print("=" * 60)

if "delivered_late" in df.columns:

    print("\nDelivered late values:")
    print(df["delivered_late"].value_counts())

    late_rate = df["delivered_late"].mean() * 100

    print(
        "\nOverall late delivery rate:",
        round(late_rate, 2),
        "%"
    )


# ============================================================
# 9. REVIEW SCORE ANALYSIS
# ============================================================

if "avg_review_score" in df.columns:

    print("\nAverage review score:")
    print(round(df["avg_review_score"].mean(), 2))


# ============================================================
# 10. DELIVERY DAYS ANALYSIS
# ============================================================

if "delivery_days" in df.columns:

    print("\nDelivery days:")
    print(
        df["delivery_days"]
        .describe()
    )


# ============================================================
# 11. CONTRIBUTION PROXY ANALYSIS
# ============================================================

if "contribution_proxy" in df.columns:

    print("\nTotal contribution proxy:")

    print(
        round(
            df["contribution_proxy"].sum(),
            2
        )
    )


# ============================================================
# 12. MONTHLY PERFORMANCE
# ============================================================

if "order_month" in df.columns and "item_value" in df.columns:

    monthly = (
        df.groupby("order_month")
        .agg(
            orders=("order_id", "count"),
            item_value=("item_value", "sum"),
            freight=("freight_value", "sum"),
            contribution_proxy=(
                "contribution_proxy",
                "sum"
            )
        )
        .reset_index()
    )

    print("\nMonthly performance:")
    print(monthly)


# ============================================================
# 13. DELIVERY VS CUSTOMER SATISFACTION
# ============================================================

if (
    "delivery_delta_days" in df.columns
    and "avg_review_score" in df.columns
):

    def delivery_bucket(days):

        if pd.isna(days):
            return "Unknown"

        elif days <= 0:
            return "On or before estimate"

        elif days <= 3:
            return "1-3 days late"

        elif days <= 7:
            return "4-7 days late"

        else:
            return "8+ days late"


    df["delivery_bucket"] = (
        df["delivery_delta_days"]
        .apply(delivery_bucket)
    )


    review_analysis = (
        df.groupby("delivery_bucket")
        .agg(
            orders=("order_id", "count"),
            avg_review_score=(
                "avg_review_score",
                "mean"
            )
        )
        .reset_index()
    )


    print("\nDelivery vs review score:")
    print(review_analysis)


# ============================================================
# 14. STATE DELIVERY ANALYSIS
# ============================================================

if (
    "customer_state" in df.columns
    and "delivery_days" in df.columns
):

    state_delivery = (
        df.dropna(subset=["delivery_days"])
        .groupby("customer_state")
        .agg(
            delivered_orders=("order_id", "count"),
            avg_delivery_days=(
                "delivery_days",
                "mean"
            )
        )
        .reset_index()
        .sort_values(
            "avg_delivery_days",
            ascending=False
        )
    )

    print("\nState delivery performance:")
    print(state_delivery.head(15))


# ============================================================
# 15. VISUALIZATION 1 — MONTHLY ITEM VALUE
# ============================================================

if "order_month" in df.columns and "item_value" in df.columns:

    monthly_plot = (
        df.groupby("order_month")["item_value"]
        .sum()
    )

    plt.figure(figsize=(10, 5))

    monthly_plot.plot()

    plt.title("Monthly Item Value")

    plt.xlabel("Month")

    plt.ylabel("Item Value")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()


# ============================================================
# 16. VISUALIZATION 2 — DELIVERY BUCKET VS REVIEW
# ============================================================

if "delivery_bucket" in df.columns:

    review_plot = (
        df.groupby("delivery_bucket")[
            "avg_review_score"
        ]
        .mean()
    )

    plt.figure(figsize=(9, 5))

    review_plot.plot(
        kind="bar"
    )

    plt.title(
        "Delivery Delay vs Customer Review Score"
    )

    plt.xlabel("Delivery Bucket")

    plt.ylabel("Average Review Score")

    plt.xticks(rotation=20)

    plt.tight_layout()

    plt.show()


# ============================================================
# 17. VISUALIZATION 3 — DELIVERY DAYS DISTRIBUTION
# ============================================================

if "delivery_days" in df.columns:

    plt.figure(figsize=(9, 5))

    df["delivery_days"].dropna().plot(
        kind="hist",
        bins=30
    )

    plt.title(
        "Delivery Days Distribution"
    )

    plt.xlabel("Delivery Days")

    plt.ylabel("Number of Orders")

    plt.tight_layout()

    plt.show()


# ============================================================
# 18. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nNext phase:")
print("Power BI Dashboard")

