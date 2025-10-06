import pandas as pd
import numpy as np
data = {
    "Name": ["Rahul", "Priya", "Arjun", "Neha", "Vikram"],
    "Age": [21, 22, 20, 23, 21],
    "Course": ["AI", "ML", "Data Science", "AI", "ML"],
    "Marks": [85, 90, 78, 88, 95]
}

df = pd.DataFrame(data)
# print(df)

# Selecting Data

# print(df[["Name"]])
# print(df[["Name","Marks"]])
#
# print(df.iloc[[0]])
# print(df.loc[2, "Marks"])

#Filter Data
# Students with marks > 85
high_scores = df[df["Marks"] > 85]
print(high_scores)

# Adding & Updating Columns

# Add Pass/Fail Column
df["Result"] = np.where(df["Marks"] >= 80,"Pass","Fail")

# Update Neha's marks
df.loc[df["Name"] == "Neha", "Marks"] = 92

print(df)
