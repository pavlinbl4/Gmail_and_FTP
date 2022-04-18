"""
конвертирует все файлы webp в заданной папке
в jpeg и удаляет исходные webp файлы
"""
import re
from PIL import Image
import os
import fnmatch

destination = '/Volumes/big4photo/Documents/NewProspect/2022_4'  # расположение обработанных файлов отчетов


def convert_to_jpeg(file_name, destination):
    file_name_no_extension = re.sub(r'\.webp', '', file_name)
    im = Image.open(f'{destination}/{file_name}').convert("RGB")
    im.save(f'{destination}/{file_name_no_extension}.JPG')


def find_report(destination):  # поиск заданных файлов в папке загрузок
    list_of_files = os.listdir(destination)
    pattern = '*.webp'
    count = 0
    for file_name in list_of_files:
        if fnmatch.fnmatch(file_name, pattern):
            count += 1
            print(file_name)
            convert_to_jpeg(file_name, destination)
            os.remove(f'{destination}/{file_name}')
    if count == 0:
        print('нет нужного файла')


find_report(destination)
