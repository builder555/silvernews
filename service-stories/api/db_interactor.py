import json
import os

class DB:
    def __init__(self):
        self._file = 'db.json'
        if not os.path.exists(self._file):
            with open(self._file, 'w') as f:
                json.dump([], f)

    def get_stories(self):
        with open(self._file, 'r') as f:
            return json.load(f)