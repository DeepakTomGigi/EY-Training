students = {"Rahul", "Priya", "Krish", "Rahul"} # does not allow duplicate elements
print(students)

fruits = {"apple", "banana", "cherry"}
print("apple" in fruits)
print("orange" in fruits)


set_a = {"Rahul", "Priya", "Krish"}
set_b = {"Amit", "Sneha", "Priya"}
print(set_a & set_b)        #Union
print(set_a - set_b)        #Difference
print(set_a | set_b)        #Intersection

#Set Function
name = ["Rahul", "Priya", "Krish","Rahul"]
unique_names= set(name)
print(unique_names)

