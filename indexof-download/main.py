#!/usr/bin/env python3

from download import FilesDownloader
from files_loader import FilesLoader
from question import Question
from filter import Filter
import argparse
import os

progname = os.path.basename(__file__)

parser = argparse.ArgumentParser(prog=progname, description='Download index of files recursively', epilog='./main.py http://example.com/index/of/path')

parser.add_argument('url', help='Index of path. Example: http://example.com/index/of/path')
parser.add_argument('-o', '--output', help='Folder to download files inside', default='./downloads')
parser.add_argument('-nc', '--no-cache', help='ignore cache', action="store_true", default=False)
parser.add_argument('-g', '--grep', help='filter by a term')

args = parser.parse_args()

url = args.url

print('SEARCHING FOR FILES...\n')

files_loader = FilesLoader(url, no_cache=args.no_cache)

files = files_loader.get()

files_loader.save()

filter_files = Filter(files, args.grep)

files = filter_files.filter()

print('\n')

if len(files) == 0:
    exit(0)

max_filename_size = files_loader.get_max_filename_size()

for index, (filename, filepath, fileurl) in enumerate(files):
    key = str(index + 1).ljust(3, ' ')

    print(key, '    ', filename.ljust(max_filename_size + 5, ' '), fileurl)

print()

question = Question({
    '1': 'Download all files',
    '2': 'Select files to download',
    '3': 'Exit'
})

option = question.ask('Choose an option> ')

if option == '1':
    files_downloader = FilesDownloader(files, args.output)

    files_downloader.all()

if option == '2':
    options = []

    try:
        options = list(map(int, set(input('Select file indexes [1 2 5 ...]> ').strip().split(' '))))
    except:
        print('NO FILES SELECTED')
        exit(0)

    files_downloader = FilesDownloader(files, args.output)

    files_downloader.by_index(options)

