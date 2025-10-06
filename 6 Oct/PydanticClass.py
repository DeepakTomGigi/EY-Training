from pydantic import BaseModel

# Define a model (like a schema)
class Student(BaseModel):
    name: str
    age: int
    email: str
    is_active: bool = True  #default value

# valid data
data = {
    "name" : "sample",
    "age" : 23,
    "email" : "sample@example.com"
}
student = Student(**data)

print(student)
print(student.name)

# invalid_data =  {
#     "name" : "Paul",
#     "age" : "Twenty",
#     "email" : "hello@example.com"
# }
#
# student1 = Student(**invalid_data)