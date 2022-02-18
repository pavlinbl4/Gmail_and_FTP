import os

from bs4 import BeautifulSoup
import requests
import time
import csv
from datetime import datetime, timedelta

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Referer': 'https://3125tiger.x.yupoo.com/',
           'Connection': 'keep-alive'
           }



def write_album_name(download_info):
    with open('downloaded_albums.csv', 'a') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(download_info)


def download_image(picture_link, album_name):
    print(picture_link)
    os.makedirs(album_name, exist_ok=True)  # создаю папку с именем альбома куда скачаю снимки
    r = requests.get(picture_link, stream=True, headers=headers)
    time.sleep(1)
    file_name = picture_link.split('/')[-1]  # сохраняю оригинальное имя файла
    with open(f'{album_name}/{file_name}', 'bw') as download_file:
        for chunk in r.iter_content(9000):
            download_file.write(chunk)


def work_with_album(full_album_link, album_name):
    url = full_album_link
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pictures = soup.find_all('img', class_="autocover image__img image__portrait")  # нахожу все снимки в альбоме
    date = soup.find('time', class_="text_overflow").text.strip()  # получаю дату создания альбома
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    if date == datetime.now().strftime("%Y-%m-%d"):  # если альбом сегодняшни, то скачиваю его
    # if date == yesterday:  # если альбом вчерашний, то скачиваю его
        for picture in pictures:  # перебираю список снимков в альбоме и получаю ссылку на хайрез
            picture_link = f"https:{picture.get('data-origin-src')}"
            download_image(picture_link, album_name)  # запускаю качалку хайреза



def get_html(url):
    r = requests.get(url, headers=headers)
    return r.text


def main():
    url = 'https://3125tiger.x.yupoo.com/albums?tab=gallery'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    albums = soup.find_all(class_="showindex__children")  # нахожу все альбомы на странице
    count = 0
    for album in albums:  # нахожу ссылку на каждый альбом
        # while count < 10:  # цикл ограничивающий количество скачиваемых альбомов за раз больше для тестирования
        album_link = album.find(class_="album__main").get('href')
        album_name = str(album.find(class_="text_overflow album__title").text)
        full_album_link = f'https://3125tiger.x.yupoo.com{album_link}'
        print(album_name)
        print(full_album_link)
        today = datetime.now().strftime("%Y-%m-%d")  # на всякий случай записываю дату скачивания альбома
        write_album_name([album_name, today, full_album_link])  # записываю информацию о скачиваемом альбоме
        work_with_album(full_album_link, album_name)  # запускаю скачивание
            # count += 1


if __name__ == "__main__":
    main()
