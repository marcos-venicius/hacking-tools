#!/usr/bin/env python3

import requests
import re
import os
import argparse


parser = argparse.ArgumentParser(
    prog='gfinder',
    description='Find files from a website over the internet and/or download them',
    epilog='./gfinder --domain example.com --filetype pdf'
)

parser.add_argument(
    '--domain',
    help='Domain to search from',
    required=True
)

parser.add_argument(
    '--filetype',
    help='Filetype you want to search for',
    required=True
)

args = parser.parse_args()


USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0"
BASE_URL = "https://www.google.com/search?q="
HEADERS = {
    'User-Agent': USER_AGENT
}


def mount_url(site: str, filetype: str) -> str:
    site = site.strip()

    if site.endswith('/'):
        return mount_url(site[:-1])

    return f"{BASE_URL}site:{site} filetype:{filetype}"


def make_request(url, get='text'):
    response = requests.get(url, headers=HEADERS)

    if get == 'text':
        return response.text
    elif get == 'content':
        return response.content


def get_file_paths(site: str, filetype: str, text: str) -> list[str]:
    regex = fr"((http)|(https):\/\/{site}).[\/|\w|\-|\.]*({filetype})"

    return list(sorted(set([x.group() for x in re.finditer(regex, text)])))


def ask(question: str) -> bool:
    answers = {'y': True, 'n': False}

    while True:
        response = input(
            f'\033[1;37m{question} \033[1;36m[y/n]\033[1;37m?\033[0m '
        )
        response = response.strip().lower()

        if response not in answers:
            continue

        return answers[response]


def get_file_name_from_url(url: str) -> str:
    return url.split('/')[-1]


def download_files(files: list[str]):
    print()

    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    for file in files:
        print(f'\033[1;36m[*]\033[1;37m {file}\033[0m')
        print('    \033[1;37mDOWNLOADING\033[0m')
        content = make_request(file, 'content')
        print('    \033[1;32mDOWNLOADED\033[0m')
        filename = get_file_name_from_url(file)
        file_path = os.path.join('downloads', filename)

        print('    \033[1;37mSAVING\033[0m')
        with open(file_path, 'wb') as file:
            file.write(content)
            file.close()
        print('    \033[1;32mSAVED\033[0m')

    print('\n\033[1;36m[*]\033[1;37m ALL FILES SAVED IN ./downloads folder\033[0m')


print('\033[1;36m[*]\033[1;37m PREPARING\033[0m')

url = mount_url(args.domain, args.filetype)

print('\033[1;36m[*]\033[1;37m SEARCHING FOR FILES\033[0m')

text = make_request(url)

file_paths = get_file_paths(args.domain, args.filetype, text)

if len(file_paths) == 0:
    print('\033[1;31m[!]\033[1;37m NO FILES FOUND\033[0m')
    exit(0)

print(f'\033[1;36m[*]\033[1;37m SHOWING {len(file_paths)} FILES\033[0m')

for index, path in enumerate(file_paths):
    print(f'    \033[1;36m{str(index + 1).rjust(2, "0")}  \033[1;37m{path}\033[0m')

print()

if ask('you want to download all files'):
    download_files(file_paths)

print('\n\033[1;37mGoodbye\033[0m')
