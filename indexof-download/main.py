#!/usr/bin/env python3

import os
import cache as cache_handler
from settings import HEADERS
from download import download_files
import requests
import re
import argparse

parser = argparse.ArgumentParser(prog='Index Of Download', description='Download index of files recursively', epilog='./main.py http://example.com/index/of/path')

parser.add_argument('url', help='Index of path. Example: http://example.com/index/of/path')
parser.add_argument('-o', '--output', help='Folder to download files inside', default='./downloads')

args = parser.parse_args()

url = args.url

cache = cache_handler.load()
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
    regex = r'(\[TXT\]|\[DIR\]|\[   \]).+(href=".+?")'

    files_list = []
    matches = re.findall(regex, text)

    for match in matches:
        kind_opts = {
            '[DIR]': 'dir',
            '[TXT]': 'file',
            '[   ]': 'file'
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

get_files_structure(url)

cache_handler.save(cache)

print('FILES FOUND\n')

max_file_size = get_max_file_name_size()

download_items = {}

for index, file in enumerate(files):
    key = str(index + 1).ljust(3)

    print('    ', key, '    ', file[0].ljust(max_file_size + 5), file[1])

    download_items[key.strip()] = file[1]

download_options = {
    '1': 'Download all',
    '2': 'Select to download',
    '3': 'Exit'
}

print('\nOPTIONS\n')

for key in download_options:
    print('    ', key.ljust(3, ' '), '    ', download_options[key])

print()

while True:
    option = input('> ')

    if option not in download_options:
        continue

    if option == '1': download_files(list(download_items.values()), args.output)

    if option == '2':
        print('\nSELECT ALL ITEMS YOU WANT TO DOWNLOAD LIKE: 1 2 3 4...\n')

        while True:
            options = list(set(input('> ').split(' ')))

            if sum([int(opt not in download_items) for opt in options]) != 0:
                print('Invalid options')
                continue

            download_files([download_items[file] for file in options], args.output)

            break
    break
