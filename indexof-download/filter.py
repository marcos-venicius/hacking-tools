from tqdm import tqdm
import requests
from settings import HEADERS
import cache
import re

class Filter:
    def __init__(self, files: list[tuple[str, str, str]], filter: str | None=None) -> None:
        self.files = files
        self.grep = filter
        self.cache = cache.load(db='grep.json')

    def __load_content(self, url: str):
        if url in self.cache:
            return self.cache[url]

        response = requests.get(url, headers=HEADERS, timeout=5000)

        self.cache[url] = response.text

        return response.text

    def filter(self) -> list[tuple[str, str, str]]:
        if self.grep is None: return self.files

        print('FILTERING FILES\n')

        found: list[tuple[str, str, str]] = []

        for i in (t := tqdm(range(len(self.files)))):
            filename, _, url = self.files[i]

            t.set_description(filename)

            file_content = self.__load_content(url)

            if re.search(self.grep, file_content, re.IGNORECASE) is not None:
                found.append(self.files[i])

        print(f'\n{len(found)} FILES FOUND')

        cache.save(self.cache, db='grep.json')

        return found