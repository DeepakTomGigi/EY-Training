import os
import time
import pandas as pd
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import pika

# ---------------- Logging ----------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

# ---------------- FastAPI ----------------
app = FastAPI(title="Student Pipeline API")

CSV_FILE = "data/students.csv"

# ---------------- Student Model ----------------
class Student(BaseModel):
    StudentID: int
    Name: str = None
    Age: int = None
    Course: str = None

# ---------------- Helpers ----------------
def read_students():
    if not os.path.exists(CSV_FILE):
        return []
    df = pd.read_csv(CSV_FILE, dtype=str)
    return df.to_dict(orient="records")

def write_students(students):
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    df = pd.DataFrame(students)
    df.to_csv(CSV_FILE, index=False)

# ---------------- API Middleware ----------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"API call: {request.method} {request.url}")
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"API call completed in {duration:.4f} seconds")
    return response

# ---------------- CRUD Endpoints ----------------
@app.get("/students")
def get_students():
    return read_students()

@app.post("/students")
def add_student(student: Student):
    students = read_students()
    if any(s["StudentID"] == str(student.StudentID) for s in students):
        logger.warning(f"Duplicate StudentID {student.StudentID}")
        raise HTTPException(status_code=400, detail="StudentID already exists")
    students.append({
        "StudentID": str(student.StudentID),
        "Name": student.Name,
        "Age": str(student.Age),
        "Course": student.Course
    })
    write_students(students)
    logger.info(f"Added student {student.StudentID}")
    return {"message": "Student added successfully"}

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    students = read_students()
    updated = False
    for s in students:
        if s["StudentID"] == str(student_id):
            s["Name"] = student.Name
            s["Age"] = str(student.Age)
            s["Course"] = student.Course
            updated = True
    if not updated:
        logger.warning(f"StudentID {student_id} not found for update")
        raise HTTPException(status_code=404, detail="Student not found")
    write_students(students)
    logger.info(f"Updated student {student_id}")
    return {"message": f"Student {student_id} updated successfully"}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    students = read_students()
    new_students = [s for s in students if s["StudentID"] != str(student_id)]
    if len(new_students) == len(students):
        logger.warning(f"StudentID {student_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Student not found")
    write_students(new_students)
    logger.info(f"Deleted student {student_id}")
    return {"message": f"Student {student_id} deleted successfully"}

# ---------------- ETL Function ----------------
def run_etl(csv_file):
    start_time = time.time()
    try:
        df = pd.read_csv(csv_file)
        logger.info(f"ETL started for {csv_file} ({len(df)} rows)")
    except Exception as e:
        logger.error(f"ETL error reading file {csv_file}: {e}")
        return
    try:
        df['TotalMarks'] = df['Maths'] + df['Python'] + df['ML']
        df['Percentage'] = (df['TotalMarks'] / 300) * 100
        df['Result'] = df['Percentage'].apply(lambda x: 'Pass' if x >= 50 else 'Fail')
        # os.makedirs("processed", exist_ok=True)
        output_file = os.path.join("data/processed", f"results_{int(time.time())}.csv")
        df.to_csv(output_file, index=False)
        duration = time.time() - start_time
        logger.info(f"ETL completed for {csv_file} in {duration:.4f}s, saved to {output_file}")
    except Exception as e:
        logger.error(f"ETL processing error for {csv_file}: {e}")

