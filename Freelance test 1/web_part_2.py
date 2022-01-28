from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import re

goods_file = '/Volumes/big4photo/Downloads/products_no_barcode.xlsx'

def write_to_separate_file(search_data):
    pass
    # провожу поиск на сайте    get_data(html,search_data)
    # дополнительно проверяю результаты по value     check_value(product_line)
    # записываю данные в отдельный файл
    # добавляю результат в лог файл

def add_barcode_to_file(search_data):
    pass
    # провожу поиск на сайте    get_data(html,search_data)
    # проверяю длинну баркода
    # записываю баркод в нужную колонку исходного файла
    # добавляю результат в лог файл

def check_value(product_line):  # в случае с поиском по нескольким параметрам проверяю еще вес
    if re.findall(r'\d+', search_data[2])[0] in product_line[5]:  # дополнительно проверяю на вес
        product_line = [product_line[5], product_line[3]]
        return product_line





def log_cvs(info):
    with open('log.csv','a') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(info)


def replace_symbols(search_text):
    search_text = search_text.strip().replace("  ", ' ').replace(" ", "+")
    return search_text.replace("$","%24").replace("%","%25").replace("&","%26")


def create_search(goods_file): # 1. получаю строку поиска из предоставленного файла
    df = pd.read_excel(goods_file)
    for i in range(1):
        product_id = df.loc[i, 'product_id']
        if df.loc[i, 'description'] == 0:  # товара нет в поле описания, результат заносим в отдельный файл
            one_row = df.loc[i, ['product_title', 'trademark', 'value', 'unit']]
            one_row = one_row.values.astype(str)
            value = one_row[2]
            search_text = f'{one_row[0].replace(",", "")}+{one_row[1]}+{value}{one_row[3]}'
            search_text = replace_symbols(search_text) # подготовливаю поисковую строку
            search_data = [product_id, search_text, value]  # возвращаю необходимые данные
            write_to_separate_file(search_data)  # в description нет данного товара записываю результат в отдельный файл
        else:
            search_text = df.loc[i, 'description']
            search_text = search_text.replace(',', '') # удаляю ненужные запятые в описании товара
            search_text = replace_symbols(search_text) # подготовливаю поисковую строку
            search_data = [product_id, search_text, 0 ]  # возвращаю необходимые данные
            add_barcode_to_file(search_data) # в description есть товар записываю штрих код  в исходный файл файл


def get_html(url):
    req = requests.get(url)
    return req.text


def get_data(html,search_data):   # функция парсящая сайт по созданному запросу и возвращающая информацию
    soup = BeautifulSoup(html, 'lxml')
    try:
        trs = soup.find(class_="randomBarcodes").find_all('tr')
        for i in range(1, len(trs)):
            product_line = []
            for td in trs[i]:
                product_line.append(td.text.strip())
                return product_line


    except:
        print('нет такого товара')


def main(search_data):
    url = 'https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=' + search_data[1]
    get_data(get_html(url),search_data)


# if __name__ == '__main__':
#     main(create_search(goods_file))  # 1. формирую поисковый запрос из исходного файла


create_search(goods_file)