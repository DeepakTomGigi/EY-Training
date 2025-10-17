import pandas as pd
import os
import logging
from datetime import datetime

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/pipeline.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

def run_daily_etl():
    try:
        df = pd.read_csv("data/marks.csv")
        df["TotalMarks"] = df["Maths"] + df["Python"] + df["ML"]
        df["Percentage"] = (df["TotalMarks"] / 300) * 100
        df["Result"] = df["Percentage"].apply(lambda x: "Pass" if x >= 50 else "Fail")

        os.makedirs("data/processed/daily_reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d")
        output_file = f"data/processed/daily_reports/daily_report_{timestamp}.csv"
        df.to_csv(output_file, index=False)

        logger.info(f"Daily ETL completed. Report saved as {output_file}")
        print(f"Daily ETL done: {output_file}")
    except Exception as e:
        logger.error(f"Daily ETL failed: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    run_daily_etl()
