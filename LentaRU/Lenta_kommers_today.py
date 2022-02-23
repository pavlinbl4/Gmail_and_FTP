import os
import requests
import json
import datetime
import time
import fake_headers

today = str(datetime.date.today())


# print(today)


def lenta_ru_time_converter(lenta_ru_time):
    return datetime.datetime.strptime(time.ctime(lenta_ru_time), '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d')


def get_html(url):
    headers = fake_headers.Headers().generate()
    # time.sleep(1)
    r = requests.get(url, headers=headers)
    # print(r.status_code)
    if r.status_code != 200:
        time.sleep(10)
        print("bad status code")
        r = requests.get(url, headers=headers)
    return r.text

def make_subfolder(photograf):
    folder = f"Ъ - {today}/{photograf}"
    os.makedirs(folder,exist_ok=True)
    return folder

def download_image(folder,image_url):
    r = requests.get(image_url)
    image_name = image_url.split('/')[-1]
    with open(f"{folder}/{image_name}",'wb') as download_file:
        for chunk in r.iter_content(9000):
            download_file.write(chunk)


def main():

    number = 10
    while True:
        url = f"https://lenta.ru/search/v2/process?from=0&size={number}&sort=2&title_only=0&domain=1&modified,format=yyyy-MM-dd&query=фото Коммерсантъ"
        rezult = json.loads(get_html(url))
        count = 0
        for i in rezult['matches']:
            if lenta_ru_time_converter(i['pubdate']) ==  today:
                count += 1
                # main_data = {'title': i['title'], 'image_url': i['image_url'], 'url': i['url'], 'pubdate': time.ctime(i['pubdate'])}
                photograf = i['text'].split('/ Коммерсантъ')[0][6:].strip()
                image_url = i['image_url']
                print(photograf, image_url, lenta_ru_time_converter(i['pubdate']))
                folder = make_subfolder(photograf)
                download_image(folder,image_url)
        print(count)
        if count < 10:
            break
        number += 10


if __name__ == '__main__':
    main()
