import json
from typing import Optional

class Config:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

def load_config(filename: Optional[str] = "config.json") -> Config:
    with open(filename) as f:
        loaded_config = json.load(f)
        config = Config(**loaded_config)
    return config
