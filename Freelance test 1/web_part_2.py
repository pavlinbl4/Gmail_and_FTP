from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import re
import time
import random


# goods_file = '/Volumes/big4photo/Downloads/products_no_barcode.xlsx'
goods_file = '/Users/evgeniy/Downloads/products_no_barcode.xlsx'


def save_data_to_file(file_name,line,search_data):
    data = [0] * 4
    data[0] = search_data[0]  # id
    data[1] = line[1]
    if len(line[0]) == 8:
        data[2] = line[0]
    elif len(line[0]) == 13:
        data[3] = line[0]
    elif len(line[0]) == 1:
        data[2] = 'товар не найден'
        data[3] = 'товар не найден'
    else:
        data[2] = 'wrong code len'
        data[3] = 'wrong code len'
    with open(f'{file_name}.csv','a') as input_file:
        writer = csv.writer(input_file)
        writer.writerow(data)



def write_to_separate_file(search_data):
    rezult = "данные в отдельный файл"
    file_name = 'separate_file'
    all_lines = main(search_data)
    cleared_all_lines = check_value(all_lines,search_data) # дополнительно проверяю результаты по value     check_value(product_line)
    for line in cleared_all_lines:
        save_data_to_file(file_name,line,search_data)
    log_cvs(search_data,rezult)
    # добавляю результат в лог файл


def add_barcode_to_file(search_data):
    rezult = 'баркод добавлен и исходный файл'
    # print(f'2 - записываю данные в исходный файл')
    file_name = 'move_to_excel'
    product_line = main(search_data)
    # for line in product_line:
    line = product_line[0]
    save_data_to_file(file_name, line, search_data)
    log_cvs(search_data,rezult)
    # записываю баркод в нужную колонку исходного файла
    # добавляю результат в лог файл


def check_value(all_lines,search_data):  # в случае с поиском по нескольким параметрам проверяю еще вес
    cleared_all_lines = []
    for line in all_lines:
        if re.findall(r'\d+', search_data[2])[0] in line[1]:  # дополнительно проверяю на вес
            cleared_all_lines.append(line)
            # print(f'записываю даные в файд {line}')
    return cleared_all_lines




def log_cvs(search_data,rezult):
    log_data = [search_data[0],rezult]
    with open('log.csv', 'a') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(log_data)


def replace_symbols(search_text):
    search_text = search_text.strip().replace("  ", ' ').replace(" ", "+")
    return search_text.replace("$", "%24").replace("%", "%25").replace("&", "%26")


def create_search(goods_file):  # 1. получаю строку поиска из предоставленного файла
    df = pd.read_excel(goods_file)
    for i in range(475,len(df)):    # for i in range(len(df)):
        product_id = df.loc[i, 'product_id']
        print(f"запрос по id {product_id}")
        if df.loc[i, 'description'] == 0:  # товара нет в поле описания, результат заносим в отдельный файл
            one_row = df.loc[i, ['product_title', 'trademark', 'value', 'unit']]
            one_row = one_row.values.astype(str)
            value = one_row[2]
            if one_row[1] != '0':  # если trademark  не указан, то строка поиска немного другая
                search_text = f'{one_row[0].replace(",", "")}+{one_row[1]}+{value}{one_row[3]}'
            else:
                search_text = f'{one_row[0].replace(",", "")}+{value}{one_row[3]}'
            search_text = replace_symbols(search_text)  # подготовливаю поисковую строку
            search_data = [product_id, search_text, value]  # возвращаю необходимые данные
            # print(f'1 - данные для поиска {search_data}')
            write_to_separate_file(search_data)  # в description нет данного товара записываю результат в отдельный файл
        else:
            search_text = df.loc[i, 'description']
            search_text = search_text.replace(',', '')  # удаляю ненужные запятые в описании товара
            search_text = replace_symbols(search_text)  # подготовливаю поисковую строку
            search_data = [product_id, search_text, None]  # возвращаю необходимые данные
            # print(f'1 - данные для поиска {search_data}')
            add_barcode_to_file(search_data)  # в description есть товар записываю штрих код  в исходный файл файл


def get_html(url):
    time.sleep(random.randrange(10,20))
    req = requests.get(url)
    return req.text


def get_data(html, search_data):  # функция парсящая сайт по созданному запросу и возвращающая информацию
    soup = BeautifulSoup(html, 'lxml')
    try:
        trs = soup.find(class_="randomBarcodes").find_all('tr')
        all_lines = []
        for i in range(1, len(trs)):
            tds = trs[i].find_all('td')
            product_line = []
            for td in tds:
                product_line.append(td.text.strip())
            product_line = product_line[1:3]
            all_lines.append(product_line)
        return all_lines


    except:
        rezult = "данный товар не обнаружен"
        # log_cvs(search_data, rezult)
        print(f'нет такого товара {search_data}')
        all_lines = [['0',search_data[1]]]
        return all_lines


def main(search_data):
    url = 'https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=' + search_data[1]
    product_line = get_data(get_html(url), search_data)
    return product_line


create_search(goods_file)
