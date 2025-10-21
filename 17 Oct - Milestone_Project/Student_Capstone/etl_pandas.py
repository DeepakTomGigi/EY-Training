import pandas as pd
import os

# ---------------- File Paths ----------------
INPUT_CSV = "data/marks.csv"
OUTPUT_CSV = "data/processed/student_results.csv"

# Ensure output folder exists
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

# ---------------- Step 1: Read CSV ----------------
try:
    df = pd.read_csv(INPUT_CSV)
except FileNotFoundError:
    print(f"Input file '{INPUT_CSV}' not found.")
    exit(1)

# ---------------- Step 2: Transform Data ----------------
# TotalMarks = sum of all subjects
df['TotalMarks'] = df['Maths'] + df['Python'] + df['ML']

# Percentage = (TotalMarks / MaximumMarks) * 100

df['Percentage'] = (df['TotalMarks'] / 300) * 100

# Result = Pass if Percentage >= 50
df['Result'] = df['Percentage'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')

# ---------------- Step 3: Save final CSV ----------------
df.to_csv(OUTPUT_CSV, index=False)

print(f"ETL Complete! Processed file saved at '{OUTPUT_CSV}'\n")
print(df)
