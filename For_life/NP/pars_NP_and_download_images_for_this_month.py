"""
20211029 объединяю файлы парсера в оин файл
"""

from bs4 import BeautifulSoup
import csv
import requests
import os
from datetime import datetime
from pathlib import Path


def make_documets_folder(name):
    (Path.home() / "Documents" / f"{name}").mkdir(parents=True, exist_ok=True)
    return Path.home() / "Documents" / f"{name}"


def get_html(url):
    req = requests.get(url)
    return req.text


def write_csv(data):
    with open(csv_file_path, 'a') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow((data["date"], data["name"], data["url"]))


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('div', class_="l-page__main-news--item")
    for title in articles:
        article_date = title.find(class_="l-page__main-news--date").text.split()[-3:]  # дата публикации
        article_name = title.find('div', class_="l-page__main-news--title").text  # заголовки статей
        image_src = title.find('img').get('src')
        image_link = f'https://newprospect.ru{image_src}'  # ссылка на изображение
        article_date_lookfine = " ".join(article_date)
        data = {"date": article_date_lookfine,
                "name": article_name,
                "url": image_link}
        write_csv(data)


def image_downloader(csv_file_path, month, month_number, current_year):
    os.makedirs(f"{folder_path}/{current_year}_{month_number}", exist_ok=True)
    with open(csv_file_path, 'r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            if month in row[0]:
                image_link = row[2]
                r = requests.get(image_link, stream=True)
                with open(
                        f"{folder_path}/{current_year}_{month_number}/{row[0]}__{row[1]}.JPG",
                        "bw") as f:
                    for chunk in r.iter_content(9000):
                        f.write(chunk)


def date_convert(month_number):  # функция преобразует введенный номер месяца в его название
    voc = {1: 'января',
           2: 'февраля',
           3: 'марта',
           4: 'апреля',
           5: 'мая',
           6: 'июня',
           7: 'июля',
           8: 'августа',
           10: 'октября',
           11: 'ноября',
           12: 'декабря'}
    month_name = voc[month_number]
    return month_name


def main():
    url = "https://newprospect.ru"
    for i in range(5):
        get_data(get_html(url))
        soup = BeautifulSoup(get_html(url), 'lxml')
        url = "https://newprospect.ru" + soup.find('li', class_='l-nav__pagination-item next').find('a').get('href')
    print('CSV file created')
    image_downloader(csv_file_path, month, month_number, current_year)
    print('Images downloaded - please select you images and run "create_report" script')


month_number = datetime.now().month
current_year = datetime.now().year

folder_path = make_documets_folder('NewProspect')

month = date_convert(month_number)
csv_file_path = f"{folder_path}/NP.csv"

if __name__ == '__main__':
    main()
