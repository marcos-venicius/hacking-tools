from urllib.parse import urlparse, urljoin
import requests
import cache as cache_handler
from settings import HEADERS
import os
import re

class FilesLoader:
    def __init__(self, url: str, no_cache=False):
        self.url = self.__base_url(url)
        self.path = self.__path(url)
        self.files = []
        self.no_cache = no_cache

        if no_cache:
            self.cache = {}
        else:
            self.cache = cache_handler.load()

    def __base_url(self, url: str) -> str:
        parse = urlparse(url)

        return f'{parse.scheme}://{parse.netloc}'

    def __path(self, url: str) -> list[str]:
        parse = urlparse(url)
        path = parse.path[1:]

        return [chunk for chunk in path.split('/') if chunk]

    def __extract_file_links_from_index_of_html_code(self, html: str) -> list[str]:
        regex = r'(\[.+?\]).+(href=".+?")'

        files_list = []
        matches = re.findall(regex, html)

        for match in matches:
            is_ico = match[0] == '[ICO]'
            is_dir = match[0] == '[DIR]'

            if is_ico: continue

            url = re.findall(r'".+?"', match[1])[0][1:-1]
            kind = 'dir' if is_dir else 'file'

            if kind == 'dir' and url.startswith('/'):
                continue

            files_list.append((kind, url))

        return files_list

    def reset(self):
        self.files = []

    def save(self):
        if not self.no_cache:
            cache_handler.save(self.cache)

    def get_max_filename_size(self):
        m = 0

        for file in self.files:
            filename_size = len(file[0])

            if filename_size > m:
                m = filename_size

        return m

    def get(self, path=None):
        if path is None:
            path = self.path

        url = os.path.join(self.url, *path)

        if url not in self.cache:
            response = requests.get(url, headers=HEADERS)

            if 'Index of /' not in response.text:
                return []

            self.cache[url] = response.text

        html = self.cache[url]

        file_links = self.__extract_file_links_from_index_of_html_code(html)

        for file_link in file_links:
            item_type = file_link[0]
            item_name = file_link[1].replace('/', '')
            item_url = urljoin(self.url, '/'.join([*path, item_name]))

            if item_type == 'file':
                self.files.append((item_name, path, item_url))
            elif item_type == 'dir':
                self.get([*path, item_name])

        return self.files

