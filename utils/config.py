import json
from pathlib import Path


class Config:
    _instance = None
    _data = None

    def __init__(self, config_file="config.json"):
        self.config_file = Path(config_file)

        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(self.config_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    @classmethod
    def _ensure_loaded(cls):
        if cls._instance is None:
            cls._instance = Config()

    @classmethod
    def get(cls, key, default=None):
        cls._ensure_loaded()
        return cls._instance._get(key, default)

    def _get(self, key, default=None):
        keys = key.split(".")
        value = self.data

        for k in keys:
            if not isinstance(value, dict):
                return default

            value = value.get(k)

            if value is None:
                return default

        return value