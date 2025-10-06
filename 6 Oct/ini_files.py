import configparser

config = configparser.ConfigParser()

config["database"] = {
    "host": "localhost",
    "port": "3306",
    "user": "root",
    "password": "admin123",
}

# write to config file
with open("app.ini", "w") as configfile:
    config.write(configfile)

# Read from config
config.read("app.ini")
print(config["database"]["host"])
print(config["database"]["port"])