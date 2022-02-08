import requests
import json


# def csv_writer(i):
#     with open("lenta_ru.csv", 'a') as input_file:
#         columns = ['title', 'image_url', 'url', "pubdate"]
#         writer = csv.DictWriter(input_file, fieldnames=columns)
#         writer.writerow(i)


def get_html(url):
    r = requests.get(url)
    return r.text


def main():
    number = 0

    while True:
        url = f"https://lenta.ru/search/v2/process?from={number}&size=10&sort=2&title_only=0&domain=1&modified,format=yyyy-MM-dd&query=Фото: Евгений Павленко / «Коммерсантъ»"
        rezult = json.loads(get_html(url))
        number += 1
        print(f"page number: {number}, записи в файле {len(rezult['matches'])}")
        if len(rezult['matches']) == 0:
            break


        with open(f"data_file_{number}.json", "a") as write_file:
            json.dump(rezult, write_file)
        # for i in rezult["matches"]:
        #     print(i['title'])
        #     print(i['image_url'])
        #     print(i['url'])
        #     print(i["pubdate"])


if __name__ == '__main__':
    main()
