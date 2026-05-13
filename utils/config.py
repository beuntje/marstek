import json
from pathlib import Path

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)

        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(self.config_file, "r", encoding="utf-8") as file:
            self.data = json.load(file)

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.data

        for k in keys:
            if not isinstance(value, dict):
                return default

            value = value.get(k)

            if value is None:
                return default

        return value