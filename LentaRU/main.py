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

    while True:
        autor = ["Фото: Александр Коряков / Коммерсантъ", "Фото: Евгений Павленко / «Коммерсантъ»"]
        url = f"https://lenta.ru/search/v2/process?from={str(number)}&size=10&sort=2&title_only=0&domain=1&modified,format=yyyy-MM-dd&query={autor[1]}"
        rezult = json.loads(get_html(url))


        print(f"page number: {number}, записи в файле {len(rezult['matches'])}")
        if len(rezult['matches']) == 0:
            print('empty json file')
            break

        # with open(f"data_file_{number}.json", "a") as write_file:
        #     # write_file.write(json.dumps(rezult))
        #     json.dump(rezult, write_file)

        for i in rezult['matches']:
            main_data = {'title': i['title'], 'image_url': i['image_url'], 'url': i['url'], 'pubdate': time.ctime(i['pubdate'])}
            print(main_data)
            csv_writer(main_data)
        number += 10



if __name__ == '__main__':
    main()
