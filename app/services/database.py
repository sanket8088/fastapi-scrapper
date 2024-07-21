import json
from typing import List
import os

class Database:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def save_data(self, data: List[dict]):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)
