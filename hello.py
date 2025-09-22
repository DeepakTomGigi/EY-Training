def greet(user):
    return f"Hello, {user}"

name = input("What is your name? ")
message = greet(name)
print(message)
