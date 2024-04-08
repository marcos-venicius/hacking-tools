#!/usr/bin/env python3

import mimetypes
import requests
import re
import os
import argparse


def dorks_type(*arg):
    allowed_dorks = set(['inurl', 'ext', 'intitle', 'intext'])

    dork = arg[0]

    if ':' not in dork:
        return dork

    dork_name, value = arg[0].split(':')

    if dork_name not in allowed_dorks:
        raise argparse.ArgumentError(f'invalid dork "{dork_name}"')

    return f'{dork_name}:{value}'


parser = argparse.ArgumentParser(
    prog='gfinder',
    description='Find files from a website over the internet and/or download them',
    epilog='./gfinder --domain example.com --filetype pdf'
)

parser.add_argument(
    'url',
    help='URL to search from (example.com, .com.br, *, ...)'
)

parser.add_argument(
    'dorks',
    nargs='*',
    type=dorks_type,
    help='inurl:"text", intext:"text", intitle:"title", "specifc term", ext:pdf'
)

parser.add_argument(
    '-a',
    '--user-agent',
    help='Custom user agent'
)

args = parser.parse_args()

print("""\033[1;32m
 ██████╗ ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗ 
██╔════╝ ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗
██║  ███╗█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝
██║   ██║██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗
╚██████╔╝██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝

\033[1;37m by https://github.com/marcos-venicius
\033[0m""")


USER_AGENT = args.user_agent or "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 OPR/108.0.0.0"
BASE_URL = "https://www.google.com/search?q="
HEADERS = {
    'User-Agent': USER_AGENT
}


def mount_url() -> str:
    return f'{BASE_URL}site:"{args.url}" {" ".join(args.dorks)}'


def make_request(url, get='text'):
    response = requests.get(url, headers=HEADERS)

    if get == 'text':
        return response.text
    elif get == 'content':
        return response.content


def get_file_paths(site: str, text: str) -> list[str]:
    regex = fr'href="((http)|(https):\/\/{site}).[\/|\w|\-|\.]*(\w)'

    return list(sorted(set([x.group().replace('href="', '') for x in re.finditer(regex, text)])))


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
    print(f'\n\033[1;36m[*]\033[1;37m DOWNLOADING {len(files)} FILES\033[0m\n')

    if not os.path.exists('downloads'):
        os.mkdir('downloads')

    for index, file in enumerate(files):
        print(f'    \033[1;36m[{str(index + 1).rjust(2, "0")}]\033[1;37m {file}\033[0m', end='')
        content = make_request(file, 'content')
        filename = get_file_name_from_url(file)

        if not mimetypes.MimeTypes().guess_type(filename)[0]:
            filename = f'{filename.strip()}.html'

        file_path = os.path.join('downloads', filename)

        with open(file_path, 'wb') as file:
            file.write(content)
            file.close()

        print('\033[1;32m success')

    print('\n\033[1;32m[+]\033[1;37m ALL FILES SAVED IN ./downloads folder\033[0m')


url = mount_url()

print('\033[1;36m[*]\033[1;37m SEARCHING...\033[0m')

text = make_request(url)

file_paths = get_file_paths(args.url, text)

if len(file_paths) == 0:
    print('\033[1;31m[!]\033[1;37m NO RESULTS FOUND\033[0m')
    exit(0)

print(f'\033[1;36m[*]\033[1;37m SHOWING {len(file_paths)} RESULTS\033[0m\n')

for index, path in enumerate(file_paths):
    ext = mimetypes.MimeTypes().guess_type(path)[0] or 'text/html'

    print(f'    \033[1;36m[{str(index + 1).rjust(2, "0")}]\033[1;37m {path} \033[0;33m"{ext}"\033[0m')

print()

if ask('you want to download all files'):
    download_files(file_paths)

print('\n\033[1;32mGoodbye\033[0m')
