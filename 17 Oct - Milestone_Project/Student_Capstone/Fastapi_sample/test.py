# FastAPI Task
from fastapi import FastAPI
from pydantic import BaseModel
import csv

app = FastAPI()

CSV_FILE = "data\students.csv"

# ---------------- Student Model ----------------
class Student(BaseModel):
    StudentID: int
    Name: str = None
    Age: int = None
    Course: str = None

# ---------------- Helper Functions ----------------
def read_students():
    with open(CSV_FILE, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_students(students):
    with open(CSV_FILE, mode="w", newline="") as file:
        fieldnames = ["StudentID", "Name", "Age", "Course"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

# ---------------- CRUD Operations ----------------
@app.get("/students")
def get_students():
    return read_students()

@app.post("/students")
def add_student(student: Student):
    students = read_students()
    if any(s["StudentID"] == str(student.StudentID) for s in students):
        return {"error": "StudentID already exists"}
    students.append({
        "StudentID": str(student.StudentID),
        "Name": student.Name or "",
        "Age": str(student.Age) if student.Age else "",
        "Course": student.Course or ""
    })
    write_students(students)
    return {"message": "Student added successfully"}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    students = read_students()
    updated = False
    for s in students:
        if s["StudentID"] == str(student_id):
            if student.Name is not None: s["Name"] = student.Name
            if student.Age is not None: s["Age"] = str(student.Age)
            if student.Course is not None: s["Course"] = student.Course
            updated = True
    if updated:
        write_students(students)
        return {"message": f"Student {student_id} updated successfully"}
    return {"error": "Student not found"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = read_students()
    new_students = [s for s in students if s["StudentID"] != str(student_id)]
    if len(new_students) == len(students):
        return {"error": "Student not found"}
    write_students(new_students)
    return {"message": f"Student {student_id} deleted successfully"}
