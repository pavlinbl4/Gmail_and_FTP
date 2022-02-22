# проверяю только сегоднящние публикации

import requests
import json
import time
import fake_headers
import datetime
import os

today = str(datetime.date.today())


def lenta_ru_time_converter(lenta_ru_time):
    return datetime.datetime.strptime(time.ctime(lenta_ru_time), '%a %b %d %H:%M:%S %Y').strftime('%Y-%m-%d')


def get_html(url):
    headers = fake_headers.Headers().generate()
    time.sleep(1)
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        time.sleep(10)
        print("bad status code")
        r = requests.get(url, headers=headers)
    return r.text


def main():
    number = 0

    autor = [
        "Фото: Александр Коряков / «Коммерсантъ»",
        "Фото: Евгений Павленко / «Коммерсантъ»"]
    for a in range(2):
        url = f"https://lenta.ru/search/v2/process?from={str(number)}" \
              f"&size=10&sort=2&title_only=0&domain=1&modified,format=yyyy-MM-dd&query={autor[a]}"
        rezult = json.loads(get_html(url))

        for i in rezult['matches']:
            if lenta_ru_time_converter(i['pubdate']) == today:
                print(i['image_url'])
                os.makedirs(f"{today}/{autor[a][6:-16]}", exist_ok=True)
                filename = i['image_url'].split("/")[-1]
                r = requests.get(i['image_url'])
                with open(f'{today}/{autor[a][6:-16]}/{filename}', 'wb') as download_file:
                    for chunk in r.iter_content(9000):
                        download_file.write(chunk)


if __name__ == '__main__':
    main()
