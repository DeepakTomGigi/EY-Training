import json

# Python dictionary

student = {
    "name": "Rahul",
    "age": 22,
    "course": ["AI", "ML"],
    "marks": {"AI": 85, "ML": 90}
}

# Write to json file
with open("student.json", "w") as f:
    json.dump(student, f, indent=4)

# Read from json file
with open("student.json", "r") as f:
    data = json.load(f)

print(data["name"])
print(data["marks"]["AI"])