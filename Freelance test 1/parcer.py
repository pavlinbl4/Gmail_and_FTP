from bs4 import BeautifulSoup
import requests

search_data = [914, "Драже+m%26m's+криспи+36.0г", '36.0']


def get_html(url):
    req = requests.get(url)
    return req.text


def get_data(html, search_data):  # функция парсящая сайт по созданному запросу и возвращающая информацию
    soup = BeautifulSoup(html, 'lxml')
    print(f'варим суп')
    try:
        trs = soup.find(class_="randomBarcodes").find_all('tr')
        for i in range(1, len(trs)):  # for i in range(1, len(trs)):
            tds = trs[i].find_all('td')
            product_line = []
            for td in tds:
                product_line.append(td.text.strip())
            print(product_line)

    except:
        print('нет такого товара')


def main(search_data):
    url = 'https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=' + search_data[1]
    get_data(get_html(url), search_data)


main(search_data)
