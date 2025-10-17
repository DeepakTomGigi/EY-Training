import pandas as pd

# Load data
students = pd.read_csv("data/students.csv")
marks = pd.read_csv("data/marks.csv")

# Merge by StudentID
merged = pd.merge(students, marks, on="StudentID")

# Derived columns
merged["TotalMarks"] = merged["Maths"] + merged["Python"] + merged["ML"]
merged["Percentage"] = (merged["TotalMarks"] / 300) * 100
merged["Result"] = merged["Percentage"].apply(lambda x: "Pass" if x >= 50 else "Fail")

# Analytics
course_stats = merged.groupby("Course")["Percentage"].agg(["mean", "max", "min"]).reset_index()
pass_rate = merged.groupby("Course")["Result"].apply(lambda x: (x == "Pass").mean() * 100).reset_index()
final = pd.merge(course_stats, pass_rate, on="Course")
final.rename(columns={"mean": "Avg%", "max": "Top%", "min": "Low%", "Result": "PassRate%"}, inplace=True)

# os.makedirs("processed", exist_ok=True)
final.to_csv("data/processed/final_analytics.csv", index=False)

print("Analytics generated: processed/final_analytics.csv")
print(final)
