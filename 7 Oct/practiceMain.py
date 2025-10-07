from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Pydantic model
class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float

# In-memory list of employees (just a regular Python list)
employees = [
    Employee(id=1, name="Alice Smith", department="HR", salary=60000.0),
    Employee(id=2, name="Bob Johnson", department="IT", salary=80000.0),
    Employee(id=3, name="Carol Williams", department="Finance", salary=75000.0),
]

# GET all employees
@app.get("/employees")
def get_employees():
    return employees

# GET employee by ID
@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    for emp in employees:
        if emp.id == emp_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")

# POST add new employee
@app.post("/employees")
def add_employee(employee: Employee):
    for emp in employees:
        if emp.id == employee.id:
            raise HTTPException(status_code=400, detail="Employee ID already exists")
    employees.append(employee)
    return employee

# PUT update employee by ID
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, updated_emp: Employee):
    for index, emp in enumerate(employees):
        if emp.id == emp_id:
            employees[index] = updated_emp
            return updated_emp
    raise HTTPException(status_code=404, detail="Employee not found")

# DELETE employee by ID
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    for index, emp in enumerate(employees):
        if emp.id == emp_id:
            del employees[index]
            return {"message": "Employee deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")


