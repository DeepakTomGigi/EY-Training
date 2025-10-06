import logging
import json

# Configure logging
logging.basicConfig(
    filename='task.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Read and print all students
with open("students.json", "r") as f:
    students = json.load(f)
    logging.info(f"Loaded {len(students)} students")

for student in students:
    print(student["name"])

# Add a new student
new_student = {
    "name": "Arjun",
    "age": 20,
    "course": "Data Science",
    "marks": 78
}
students.append(new_student)

# save it back to the original file
with open("students.json", "w") as f:
    json.dump(students, f, indent=4)
    logging.info(f"Added new student {new_student['name']}")