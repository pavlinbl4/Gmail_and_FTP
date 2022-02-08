import requests
import json
import csv
import time


def csv_writer(i):
    with open("lenta_ru.csv", 'a') as input_file:
        columns = ['title', 'image_url', 'url', "pubdate"]
        writer = csv.DictWriter(input_file, fieldnames=columns)
        writer.writerow(i)


def get_html(url):
    r = requests.get(url)
    time.sleep(1)
    return r.text


def main():
    number = 0

    while True:
        url = f"https://lenta.ru/search/v2/process?from={str(number)}&size=10&sort=2&title_only=0&domain=1&modified,format=yyyy-MM-dd&query=Фото: Евгений Павленко / «Коммерсантъ»"
        rezult = json.loads(get_html(url))

        number += 1
        print(f"page number: {number}, записи в файле {len(rezult['matches'])}")
        if len(rezult['matches']) == 0:
            print('empty json file')
            break

        for i in rezult['matches']:
            main_data = {'title': i['title'], 'image_url': i['image_url'], 'url': i['url'], 'pubdate': time.ctime(i['pubdate'])}
            print(main_data)
            csv_writer(main_data)


if __name__ == '__main__':
    main()
