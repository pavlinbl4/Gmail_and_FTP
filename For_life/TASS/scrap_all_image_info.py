import requests
from bs4 import BeautifulSoup

url = "https://www.tassphoto.com/ru/asset/fullTextSearch/search/%D0%A1%D0%B5%D0%BC%D0%B5%D0%BD+%D0%9B%D0%B8%D1%85%D0%BE%D0%B4%D0%B5%D0%B5%D0%B2/page/1"


def get_html(url):
    return requests.get(url).text


def main():
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    thumbs_data = soup.find('ul', id="mosaic").find_all('div', class_="thumb-content thumb-width thumb-height")
    images_on_page = len(soup.find('ul', id="mosaic").find_all('a', class_="zoom"))
    for i in range(images_on_page):
        print(thumbs_data[i].find(class_="date").text)
        print(thumbs_data[i].find(class_="title").text)
        print(thumbs_data[i].find('p').text)
        print(
            soup.find('ul', id="mosaic").find_all(class_="thumb-text")[i].text.strip().split('\n')[-1].lstrip().replace(
                ' Семен Лиходеев/ТАСС', ''))
        print(soup.find('ul', id="mosaic").find_all('a', class_="zoom")[i].find('img').get('src'))


if __name__ == "__main__":
    main()
