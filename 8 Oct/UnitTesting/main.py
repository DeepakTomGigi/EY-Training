from math import degrees

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float

employees = [
    {"id": 1, "name": "Amit Sharma", "department": "HR", "salary": 50000},
]

@app.get("/employees")
def get_all():
    return employees

@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    employees.append(employee.dict())
    return employee

@app.get("/employees/{emp_id}")
def get_employee(emp_id: int):
    for emp in employees:
        if emp["id"] == emp_id:
            return emp
    raise HTTPException(status_code=404, detail="Employee not found")


@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, employee: Employee):
    for i, emp in enumerate(employees):
        if emp["id"] == emp_id:
            employees[i] = employee.model_dump()  # update in-place
            return {"message": "Employee updated successfully", "employee": employees[i]}
    raise HTTPException(status_code=404, detail="Employee not found")

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int):
    for i, emp in enumerate(employees):
        if emp["id"] == emp_id:
            del employees[i]
            return {"message": "Employee deleted successfully"}
    raise HTTPException(status_code=404, detail="Employee not found")

