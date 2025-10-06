import yaml
import logging

logging.basicConfig(
    filename='task2.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


config = {
    "app": {
        "name": "Student Portal",
        "version": "1.0"
    },

    "database": {
        "host": "localhost",
        "port": "3306",
        "user": "root"
    }
}

with open("config.yaml", "w") as f:
    yaml.dump(config, f)

filename = 'config.yaml'

try:
    # read config using yaml
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
        logging.info("Config loaded successfully.")

    # print the database connection
    db = config['database']
    connection_string = f"Connecting to {db['host']}:{db['port']} as {db['user']}"
    print(connection_string)

except FileNotFoundError:
    logging.error(f"{filename} not found.")
    print(f"Error: {filename} not found.")

