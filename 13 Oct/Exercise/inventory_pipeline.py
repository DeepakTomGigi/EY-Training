import pandas as pd
from datetime import datetime

def run_pipeline():
    print("Starting Inventory Restock Alert Pipeline...\n")
    start_time = datetime.now()

    # 1. Extract
    df = pd.read_csv("inventory.csv")

    # 2. Transform
    # Add RestockNeeded column
    df["RestockNeeded"] = df.apply(
        lambda row: "Yes" if row["Quantity"] < row["ReorderLevel"] else "No",
        axis=1
    )

    # Add TotalValue column
    df["TotalValue"] = df["Quantity"] * df["PricePerUnit"]

    # 3. Load
    df.to_csv("restock_report.csv", index=False)

    # 4. Print completion message
    end_time = datetime.now()
    print(f"Inventory pipeline completed at {end_time}")
    print("Output file: restock_report.csv")

if __name__ == "__main__":
    run_pipeline()
