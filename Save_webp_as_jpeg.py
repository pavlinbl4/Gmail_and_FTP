"""
конвертирует все файлы webp в папке downloads
в jpeg и удаляет исходные webp файлы
"""

from PIL import Image
import os
import fnmatch

destination = '/Volumes/big4photo/Downloads/'  # расположение обработанных файлов отчетов


def convert_to_jpeg(file_name, destination):
    print(f"найден файл {file_name.split('.')[0]}")
    im = Image.open(f'{destination}{file_name}').convert("RGB")
    im.save(f'{destination}{file_name.split(".")[0]}.jpg')


def find_report(destination):  # поск заданных файлов в папке загрузок
    list_of_files = os.listdir(destination)
    pattern = '*.webp'
    count = 0
    for file_name in list_of_files:
        if fnmatch.fnmatch(file_name, pattern):
            count += 1
            convert_to_jpeg(file_name, destination)
            os.remove(f'{destination}{file_name}')
    if count == 0:
        print('нет нужного файла')


find_report(destination)
