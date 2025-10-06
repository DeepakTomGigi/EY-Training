import yaml

config = {
    "model": "RandomForest",
    "params": {
        "n_estimators": 100,
        "max_depth": 5
    },
    "dataset": "student.csv"
}

# write to YAML file
with open("config.yaml", "w") as f:
    yaml.dump(config, f)

# Read YAML
with open("config.yaml", "r") as f:
    data = yaml.safe_load(f)

print(data["params"]["n_estimators"])