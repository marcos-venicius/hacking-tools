import requests
import os
from settings import HEADERS


class FilesDownloader:
    def __init__(self, files, output):
        self.files = files
        self.output = output

    def __get_content(self, url):
        response = requests.get(url, headers=HEADERS)

        return response.content

    def __download(self, files):
        print(f'\nDOWNLOADING {len(files)} FILES\n')

        if not os.path.exists(self.output):
            os.mkdir(self.output)

        if not os.path.isdir(self.output):
            raise Exception(f'"{self.output}" is not a folder')

        for filename, filepath, fileurl in files:
            print('?', filename)

            dirpath = os.path.join(self.output, *filepath)
            filepath = os.path.join(self.output, *filepath, filename)

            os.makedirs(dirpath, exist_ok=True)

            content = self.__get_content(fileurl)

            with open(filepath, 'wb') as file:
                file.write(content)
                file.close()

            print('+', filename, '    ', dirpath)

    def all(self):
        self.__download(self.files)

    def by_index(self, indexes: list[int]):
        indexes = set(indexes)

        files = []

        for index in indexes:
            if index < 1 or index > len(self.files):
                continue

            files.append(self.files[index - 1])

        self.__download(files)

