import csv
from database.db_config import get_connection


# 1. Insert data from CSV
def insert_students_from_csv():
    conn = get_connection()
    cursor = conn.cursor()
    with open("../data/students.csv", "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            cursor.execute("""
                INSERT INTO students (StudentID, Name, Age, Course)
                VALUES (%s, %s, %s, %s)
            """, (row["StudentID"], row["Name"], row["Age"], row["Course"]))

    conn.commit()
    conn.close()
    print("Students inserted successfully!")


# 2. Update a course
def update_course(student_id, new_course):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students SET Course = %s WHERE StudentID = %s
    """, (new_course, student_id))
    conn.commit()
    conn.close()
    print(f"Student {student_id}'s course updated to {new_course}")


# 3. Delete a student
def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE StudentID = %s", (student_id,))
    conn.commit()
    conn.close()
    print(f"Student {student_id} deleted successfully.")


# 4. Fetch students enrolled in “AI”
def fetch_ai_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE Course = 'AI'")
    for row in cursor.fetchall():
        print(row)
    conn.close()




# --- Run the pipeline ---
if __name__ == "__main__":
    # Uncomment one at a time to test
    # insert_students_from_csv()
    # update_course(102, "Deep Learning")
    delete_student(105)
    # fetch_ai_students()
