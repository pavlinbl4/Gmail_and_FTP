import requests
import json
import csv
import time
import fake_headers



def csv_writer(i):
    with open("lenta_ru.csv", 'a') as input_file:
        columns = ['title', 'image_url', 'url', "pubdate"]
        writer = csv.DictWriter(input_file, fieldnames=columns)
        writer.writerow(i)


def get_html(url):
    # headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:96.0) Gecko/20100101 Firefox/96.0',
    #            "accept": "*/*"}
    headers = fake_headers.Headers().generate()
    r = requests.get(url,headers=headers)
    if r.status_code != 200:
        time.sleep(7)
        print("bad status code")
        r = requests.get(url, headers=headers)
    # print(r.status_code)
    return r.text


def main():
    number = 0

    while True:
        autor = "Фото: Александр Коряков / Коммерсантъ"  #    Фото: Евгений Павленко / «Коммерсантъ»
        url = f"https://lenta.ru/search/v2/process?from={str(number)}&size=10&sort=2&title_only=0&domain=1&modified,format=yyyy-MM-dd&query={autor}"
        rezult = json.loads(get_html(url))

        number += 1
        print(f"page number: {number}, записи в файле {len(rezult['matches'])}")
        if len(rezult['matches']) == 0:
            print('empty json file')
            break

        with open(f"data_file_{number}.json", "a") as write_file:
            json.dump(rezult, write_file)

        # for i in rezult['matches']:
        #     main_data = {'title': i['title'], 'image_url': i['image_url'], 'url': i['url'], 'pubdate': time.ctime(i['pubdate'])}
        #     print(main_data)
        #     csv_writer(main_data)


if __name__ == '__main__':
    main()
