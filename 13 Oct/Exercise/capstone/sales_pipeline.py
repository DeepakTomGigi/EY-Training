import pandas as pd
from datetime import datetime

def run_pipeline():
    start = datetime.now()

    # 1. Extract the data
    products = pd.read_csv("products.csv")
    customers = pd.read_csv("customers.csv")
    orders = pd.read_csv("orders.csv")

    # 2. Transform the data
    # merge the data
    merged_df = pd.merge(orders, customers, on="CustomerID", how="inner")
    merged_df = pd.merge(merged_df, products, on="ProductID", how="inner")

    merged_df["TotalAmount"] = merged_df["Quantity"] * merged_df["Price"]
    
    merged_df["OrderDate"] = pd.to_datetime(merged_df["OrderDate"])
    merged_df["OrderMonth"] = merged_df["OrderDate"].dt.month_name()

    merged_df = merged_df[merged_df["Quantity"] >= 2]
    merged_df = merged_df[merged_df["Country"].isin(["India", "UAE"])]


    # grouping and aggregating
    category_summary = (
        merged_df.groupby("Category")["TotalAmount"]
        .sum()
        .reset_index()
        .rename(columns={"TotalAmount": "TotalRevenue"})
    )

    segment_summary = (
        merged_df.groupby("Segment")["TotalAmount"]
        .sum()
        .reset_index()
        .rename(columns={"TotalAmount": "TotalRevenue"})
    )

    customer_revenue = (
        merged_df.groupby(["CustomerID", "Name"])["TotalAmount"]
        .sum()
        .reset_index()
        .sort_values(by="TotalAmount", ascending=False)
    )

    customer_revenue["Rank"] = customer_revenue["TotalAmount"].rank(
        method="dense", ascending=False
    ).astype(int)

    merged_df.to_csv("processed_orders.csv", index=False)
    category_summary.to_csv("category_summary.csv", index=False)
    segment_summary.to_csv("segment_summary.csv", index=False)
    customer_revenue.to_csv("customer_ranking.csv", index=False)

    end_time = datetime.now()
    print(f"🕒 Completed at: {end_time}")
    print("Output files generated:")
    print(" - processed_orders.csv")
    print(" - category_summary.csv")
    print(" - segment_summary.csv")
    print(" - customer_ranking.csv")


if __name__ == "__main__":
    run_pipeline()


