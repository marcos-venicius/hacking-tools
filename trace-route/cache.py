import os
import json
import base64


class Cache:
    def __init__(self, filename: str):
        self.filename = filename
        self.cache = None

    def has_cache(self, key: str) -> bool:
        cache = self.load()

        return key in cache

    def load(self):
        if self.cache: return self.cache
        
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as file:
                content = file.read()
                content = base64.b64decode(content)
                content = content.decode('utf-8')
                content = content.strip()
                content = content or '{}'
                content = json.loads(content)

                self.cache = content

                file.close()
        else:
            self.cache = {}

        return self.cache

    def write(self, cache: dict):
        self.cache = cache

        with open(self.filename, 'wb') as file:
            content = json.dumps(cache)
            content = content.encode('utf-8')
            content = base64.b64encode(content)

            file.write(content)

            file.close()

