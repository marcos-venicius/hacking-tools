#!/usr/bin/env python3

import os
import json
import requests
import re
import argparse

parser = argparse.ArgumentParser(prog='Index Of Download', description='Download index of files recursively', epilog='./main.py http://example.com/index/of/path')

parser.add_argument('url', help='Index of path. Example: http://example.com/index/of/path')

args = parser.parse_args()

url = args.url

HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'
}

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
        response = requests.get(url, headers=HEADERS)

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

def download_all(files):
    print('\n\033[1;36mDownloading\033[0m\n')

    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    for file in files:
        response = requests.get(file, headers=HEADERS)
        filename = file.split('/')[-1]

        with open(f'./downloads/{filename}', 'wb') as file:
            file.write(response.content)
            file.close()
        print(f'\033[1;32m+ \033[0m{filename}')

    print(f'\n\033[1;32m{len(files)} files downloaded to ./downloads folder\033[0m\n')

get_files_structure(url)

save_cache(cache)

print('\033[1;37mFILES FOUND:\033[0m\n')

max_file_size = get_max_file_name_size()

download_items = {}

for index, file in enumerate(files):
    key = str(index + 1).ljust(3)

    print('    \033[1;36m', key, '    \033[1;37m', file[0].ljust(max_file_size + 5), '\033[0m', file[1])

    download_items[key.strip()] = file[1]

download_options = {
    '1': 'Download all',
    '2': 'Select to download',
    '3': 'Exit'
}

print()
print('\033[1;37mOPTIONS\033[0m')
print()

for key in download_options:
    print('    \033[1;36m', key.ljust(3, ' '), '    \033[0m', download_options[key])

print()

while True:
    option = input('\033[1;37m> \033[0m')

    if option not in download_options:
        continue

    if option == '1': download_all(list(download_items.values()))

    if option == '2':
        print('\n\033[1;37mSELECT ALL ITEMS YOU WANT TO DOWNLOAD LIKE: 1 2 3 4...\033[0m\n')

        while True:
            options = list(set(input('\033[1;37m> \033[0m').split(' ')))

            if sum([int(opt not in download_items) for opt in options]) != 0:
                print('Invalid options')
                continue

            download_all([download_items[file] for file in options])

            break
    break
