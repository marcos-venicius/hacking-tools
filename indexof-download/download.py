import requests
import os
from settings import HEADERS

def download_files(files_url: list[str], path='./downloads') -> None:
    print('\nDownloading\n')

    if not os.path.exists(path):
        os.mkdir(path)

    for file in files_url:
        response = requests.get(file, headers=HEADERS)
        filename = file.split('/')[-1]

        file_path = os.path.join(path, filename)

        with open(file_path, 'wb') as file:
            file.write(response.content)
            file.close()

        print(f'+ {filename}')

    print(f'\n{len(files_url)} files downloaded to {path} folder\n')
