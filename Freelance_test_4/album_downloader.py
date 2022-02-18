import os
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime, timedelta
import random
import time

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Referer': 'https://3125tiger.x.yupoo.com/',
           'Connection': 'keep-alive'
           }


def get_album_date(full_album_link):
    url = full_album_link
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')

    album_date = soup.find('time', class_="text_overflow").text.strip()  # получаю дату создания альбома
    return album_date


def write_album_name(download_info):
    with open(f'downloaded_albums - {download_info[1]}.csv', 'a') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(download_info)


def download_image(picture_link, album_name):
    print(picture_link)
    os.makedirs(album_name, exist_ok=True)  # создаю папку с именем альбома куда скачаю снимки
    r = requests.get(picture_link, stream=True, headers=headers)
    # time.sleep(1)
    file_name = picture_link.split('/')[-1]  # сохраняю оригинальное имя файла
    with open(f'{album_name}/{file_name}', 'bw') as download_file:
        for chunk in r.iter_content(9000):
            download_file.write(chunk)


def work_with_album(full_album_link, album_name):
    url = full_album_link
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    pictures = soup.find_all('div', class_="image__imagewrap")  # нахожу все снимки в альбоме
    print(f"количеcтво снимков в альбоме по тэгам - {len(pictures)}")
    number_of_images_in_album = soup.find("h2").find_all("span")[1].text
    print(f'количеcтво снимков в альбоме из описания - {number_of_images_in_album}')
    album_name = f'{album_name} :  ({number_of_images_in_album} images)'
    # print(album_name)


    for picture in pictures:  # перебираю список снимков в альбоме и получаю ссылку на хайрез
        picture_link = f"https:{picture.find('img').get('data-origin-src')}"
        print(picture_link)
        download_image(picture_link, album_name)  # запускаю качалку хайреза


def get_html(url):
    r = requests.get(url, headers=headers)
    time.sleep(random.randrange(1,3))
    print(r.status_code)
    if r.status_code != 200:
        print("Ошибка ответа сервера")
        return
    return r.text


def main():
    day_shift = int(input(f"Введите\n\
    '0\' - альбомы добавленные сегодня,\n\
    '1\' - альбомы добавленные вчера,\n\
    '2\' - альбомы добавленные позавчера\n\
    и тд\n"))
    yesterday = (datetime.now() - timedelta(days=day_shift)).strftime("%Y-%m-%d")  # дата сдвига альбома
    print(f" будут скачаны альбомы с датой {yesterday}")

    url = 'https://3125tiger.x.yupoo.com/albums?tab=gallery'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    albums = soup.find_all(class_="showindex__children")  # нахожу все альбомы на странице
    count = 0
    for i in range(len(albums)):  # перебираю все альбомы на первой странице
        album_link = albums[i].find(class_="album__main").get('href')
        album_name = str(albums[i].find(class_="text_overflow album__title").text)
        full_album_link = f'https://3125tiger.x.yupoo.com{album_link}'
        album_date = get_album_date(full_album_link)  # получаю дату альбома со страницы сайта
        print(f' Проверяю album_name - {album_name}, album_date - {album_date}, count - {i}')

        if album_date == yesterday:  # если альбом вчерашний, то скачиваю его
            count += 1
            print(f"Скачиваю альбом {album_name}")
            print(full_album_link)
            write_album_name([album_name, album_date, full_album_link])  # записываю информацию о скачиваемом альбоме
            work_with_album(full_album_link, album_name)  # запускаю скачивание
        # elif album_date == (datetime.now() - timedelta(days=day_shift + 2)).strftime("%Y-%m-%d"):
        #     print("Работа программы завершена")
        #     return
    print(f"Работа программы завершена скачано {count} альбомов")

if __name__ == "__main__":
    main()


