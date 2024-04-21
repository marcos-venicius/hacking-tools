import requests
import os
import cache
from settings import HEADERS


class FilesDownloader:
    def __init__(self, files, output):
        self.files = files
        self.output = output
        self.cache = cache.load(db='grep.json')

    def __get_content(self, url):
        if url in self.cache: return self.cache[url]

        response = requests.get(url, headers=HEADERS, timeout=5000)

        self.cache[url] = response.text

        return response.text

    def __max_filename_length(self, files) -> int:
        m = 0

        for filename, _, _ in files:
            filename_length = len(filename)

            if filename_length > m:
                m = filename_length
        
        return m

    def __download(self, files):
        max_filename_length = self.__max_filename_length(files)
        downloaded_files = 0
        failed_downloads = 0

        print(f'\nDOWNLOADING {len(files)} FILES\n')

        if not os.path.exists(self.output):
            os.mkdir(self.output)

        if not os.path.isdir(self.output):
            raise Exception(f'"{self.output}" is not a folder')

        for filename, filepath, fileurl in files:
            print('?', filename.ljust(max_filename_length + 5, ' '), end=' ')

            dirpath = os.path.join(self.output, *filepath)
            filepath = os.path.join(self.output, *filepath, filename)

            try:
                content = self.__get_content(fileurl)

                os.makedirs(dirpath, exist_ok=True)
            except:
                print('!', filepath)
                failed_downloads += 1
                continue

            with open(filepath, 'wb') as file:
                file.write(content.encode('utf-8'))
                file.close()

            downloaded_files += 1
            print('+', filepath)

        print()
        print(f'+ {downloaded_files} FILES DOWNLOADED SUCCESSFULLY')
        print(f'! {failed_downloads} DOWNLOADS FAILED\n')

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

