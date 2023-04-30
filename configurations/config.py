import json

class Config:
    def __init__(self, connection_string):
        self.connection_string = connection_string

def load_config(filename="config.json"):
    with open(filename) as f:
        loaded_config = json.load(f)
        config = Config(**loaded_config)
    return config
