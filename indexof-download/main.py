#!/usr/bin/env python3

import os
import json
import requests
import re

def load_cache() -> dict:
    if os.path.exists('cache.json'):
        with open('cache.json', 'r') as file:
            string = file.read()
            return json.loads(string)
    else:
        return {}


def save_cache(cache: dict) -> None:
    with open('cache.json', 'w') as file:
        file.write(json.dumps(cache));
        file.close()

cache = load_cache()
files = []

def get_files_structure(url: str, first=True, path_history=[]):
    text = ''

    url = os.path.join(url, *path_history)

    if url in cache:
        text = cache[url]
    else:
        response = requests.get(url, headers={
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
        })

        if 'Index of /' not in response.text:
            if first: raise Exception('This url is no Index Of')
            return None

        cache[url] = response.text
        text = response.text

    results = extract_files_from_text(text)

    for result in results:
        if result[0] == 'file':
            files.append((result[1], os.path.join(url, *path_history, result[1])))
        elif result[0] == 'dir' and result[1] != '':
            get_files_structure(url, False, [result[1]])

def extract_files_from_text(text: str) -> list[str]:
    regex = r'(\[TXT\]|\[DIR\]).+(href=".+?")'

    files_list = []
    matches = re.findall(regex, text)

    for match in matches:
        kind_opts = {
            '[DIR]': 'dir',
            '[TXT]': 'file'
        }

        url = re.findall(r'".+?"', match[1])[0][1:-1]
        kind = kind_opts[match[0]]

        if kind == 'dir' and url.startswith('/'):
            continue

        files_list.append((kind, url))

    return files_list

def get_max_file_name_size():
    m = 0

    for file in files:
        if len(file[0]) > m:
            m = len(file[0])

    return m

get_files_structure('http://businesscorp.com.br/css/')

save_cache(cache)

print('Files found:\n')

max_file_size = get_max_file_name_size()

for index, file in enumerate(files):
    key = str(index + 1).ljust(3)

    print('    \033[1;36m', key, '    \033[1;37m', file[0].ljust(max_file_size + 5), '\033[0m', file[1])

print()


