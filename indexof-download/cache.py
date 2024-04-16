
import os
import json


def load() -> dict:
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as file:
            string = file.read()
            return json.loads(string)
    else:
        return {}

def save(cache: dict) -> None:
    with open('cache.json', 'w') as file:
        file.write(json.dumps(cache));
        file.close()
