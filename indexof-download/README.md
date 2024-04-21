# Index Of Download

Download files from index of directory

![Peek 2024-04-21 11-09](https://github.com/marcos-venicius/hacking-tools/assets/94018427/daca0485-6646-42e1-b39f-68876b80b3ee)

## Features

- Caching for fast reuse
- Download all files
- Download specific files
- Filter files

Usage:

```
usage: main.py [-h] [-o OUTPUT] [-nc] [-g GREP] url

Download index of files recursively

positional arguments:
  url                   Index of path. Example: http://example.com/index/of/path

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Folder to download files inside
  -nc, --no-cache       ignore cache
  -g GREP, --grep GREP  filter by a term

./main.py http://example.com/index/of/path
```
