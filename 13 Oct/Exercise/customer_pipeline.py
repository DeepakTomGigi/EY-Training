import pandas as pd
from datetime import datetime

def run_pipeline():
    start = datetime.now()

    # 1. Extract data
    df = pd.read_csv("customers.csv")

    # 2. Transform the data
    df["AgeGroup"] = df["Age"].apply(
        lambda age: "Young" if age < 30 else ("Adult" if age < 50 else "Senior")
    )

    df = df[df["Age"] >= 20]

    # 3. Load
    df.to_csv("filtered_customers.csv", index=False)

    # 4. Print execution time
    end = datetime.now()
    print("Pipeline executed successfully!")
    print(f"Execution Time: {end}")
    print("Output file: filtered_customers.csv")


if __name__ == "__main__":
    run_pipeline()