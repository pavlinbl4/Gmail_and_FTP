import os
import requests
import json
import datetime
import time
import fake_headers
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl import load_workbook

today = str(datetime.date.today())


def lenta_ru_time_converter(lenta_ru_time):
    return datetime.datetime.strptime(time.ctime(lenta_ru_time), '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d')


def get_html(url):
    headers = fake_headers.Headers().generate()
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        time.sleep(10)
        print("bad status code")
        r = requests.get(url, headers=headers)
    return r.text


def make_subfolder(photograf):
    folder = f"Ъ - {today}/{photograf}"
    os.makedirs(folder, exist_ok=True)
    return folder


def download_image(folder, image_url):
    r = requests.get(image_url)
    image_name = image_url.split('/')[-1]
    with open(f"{folder}/{image_name}", 'wb') as download_file:
        for chunk in r.iter_content(9000):
            download_file.write(chunk)
    return f"{folder}/{image_name}"


# def open_xlsx_file():
#     if os.path.exists('Ъ_in_LentaRU.xlsx'):
#         wb = load_workbook('Ъ_in_LentaRU.xlsx')  # файл есть и открываю его
#         ws = wb.create_sheet(today)  # добавляю новую таблицу
#     else:
#         wb = Workbook()  # если файда еще нет
#         ws = wb.active  # если файда еще нет
#         ws.title = today  # если файда еще нет
#
#     ws.column_dimensions['C'].width = 50  # задаю шрину колонки
#     ws.column_dimensions['A'].width = 30
#     ws.column_dimensions['B'].width = 100
#     return ws, wb


def main():
    if os.path.exists('Ъ_in_LentaRU.xlsx'):
        wb = load_workbook('Ъ_in_LentaRU.xlsx')  # файл есть и открываю его
        ws = wb.create_sheet(today)  # добавляю новую таблицу
    else:
        wb = Workbook()  # если файда еще нет
        ws = wb.active  # если файда еще нет
        ws.title = today  # если файда еще нет

    ws.column_dimensions['C'].width = 50  # задаю шрину колонки
    ws.column_dimensions['A'].width = 30
    ws.column_dimensions['B'].width = 100
    number = 10

    while True:
        url = f"https://lenta.ru/search/v2/process?from=0&size={number}" \
              f"&sort=2&title_only=0&domain=1&modified,format=yyyy-MM-dd&query=фото Коммерсантъ"
        rezult = json.loads(get_html(url))
        count = 0
        for i in rezult['matches']:
            if lenta_ru_time_converter(i['pubdate']) == today:
                count += 1
                photograf = i['text'].split('/ Коммерсантъ')[0][6:].strip()
                image_url = i['image_url']
                ws.row_dimensions[count].height = 100  # задаю высоту столбца
                print(photograf, image_url, lenta_ru_time_converter(i['pubdate']))
                folder = make_subfolder(photograf)
                image_path = download_image(folder, image_url)

                img = Image(image_path)
                resize_height = img.height // 3  # уменьшая рарешение в два раза
                resize_width = img.width // 3  # уменьшая рарешение в два раза

                img.width = resize_width  # устанавливаю размер превью
                img.height = resize_height  # устанавливаю размер превью

                ws.add_image(img, f'B{count}')
                ws[f'A{count}'] = photograf
        # print(count)
        if count < 10:
            wb.save('Ъ_in_LentaRU.xlsx')
            break
        number += 10


if __name__ == '__main__':
    main()
