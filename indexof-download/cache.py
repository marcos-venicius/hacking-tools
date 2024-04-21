import os
import json
import base64


def load(db='cache.json') -> dict:
    if os.path.exists(db):
        with open(db, 'rb') as file:
            string = file.read()
            decoded = base64.b64decode(string.decode('utf-8'))
            return json.loads(decoded)

    else:
        return {}

def save(cache: dict, db='cache.json') -> None:
    with open(db, 'wb') as file:
        dump = json.dumps(cache)
        b64 = base64.b64encode(dump.encode('utf-8'))
        file.write(b64)
        file.close()
