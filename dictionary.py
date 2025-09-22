student = {
    'name' : 'John',
    'age' : 22,
    'course': 'Python'
}

print(student['name'])
print(student.get('age'))

student["grade"] = "A" #add new key-value
student["age"] = "23" # update existing value

student.pop("grade")    #remove by key
# del student["course"]   # delete key

for key, value in student.items():
    print(key, ":", value)

print(student)

employee = {
    "id" : 1,
    "name" : "sonu",
    "dept" : "finance",
    "skills": ["python", "c++", "java"]
}
print(employee["skills"][1])    #access nested data