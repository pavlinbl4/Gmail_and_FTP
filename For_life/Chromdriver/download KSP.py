""" скрипт скачивания фотографий из архива по номеру съемки
"""
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from KSP_credintails import login, password, first_loggin
from bs4 import BeautifulSoup
import re

login = login
password = password
first_loggin = first_loggin

cgreen = '\33[0;32m'
cend = '\033[0m'
cred = '\033[91m'

options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
options.headless = True # фоновый режим работы
browser = webdriver.Chrome(options=options)


def shoot_number():
    number = 17472  # input(f"{cgreen}ENTER FIVE DIGITS OF SHOOT ID{cend}\n")
    return number


def get_total_images(html):
    soup = BeautifulSoup(html, 'lxml')
    total_images = soup.find('span', id='ctl00_MainContent_AllPhoto1').text
    total_images = int(re.findall(r'\d+', total_images)[0])  # количество файлов в съемке
    return total_images


def download_one_page(number_of_downloads, shoot_id, page,count):
    print(f'page {page}')
    print(f'number_of_downloads - {number_of_downloads}')
    print(f'https://image.kommersant.ru/photo/wp/default.aspx?shootnum={shoot_id}&sourcecode=KSP&pagesize=200&previewsize=128&page={page}&nl=true&ord=true')
           #https://image.kommersant.ru/photo/wp/default.aspx?shootnum=17472&sourcecode=KSP&pagesize=200&previewsize=128&page=2&nl=true&ord=T

    browser.get(
        f'https://image.kommersant.ru/photo/wp/default.aspx?shootnum={shoot_id}&sourcecode=KSP&pagesize=200&previewsize=128&page={str(page)}&nl=true&ord=true')


    for x in range(number_of_downloads):
        index = ("0000" + str(count))[-5:]
        count += 1
        print(f'index - {index}')

        new_window = browser.window_handles[0]
        browser.switch_to.window(new_window)
        browser.find_element(By.CSS_SELECTOR,
                             f"#unselected_KSP_0{shoot_id}_{index} > a.ui-icon.ui-icon-plus").click()

        new_window = browser.window_handles[1]
        browser.switch_to.window(new_window)
        try:
            browser.find_element(By.CSS_SELECTOR, "div.hi-subpanel:nth-child(3) > a:nth-child(4)").click()
            print(f'{cgreen}image {f"KSP_0{shoot_id}_{index}"} downloaded{cend}')
            time.sleep(3)
            browser.close()
        except Exception as ex:
            print(f'image {cred}{f"KSP_0{shoot_id}_{index}"}{cend} not aviable')
            browser.close()


def autorization(shoot_id):
    try:
        browser.get(
            f'{first_loggin}/photo/wp/default.aspx?shootnum={shoot_id}'
            f'&sourcecode=KSP&pagesize=200&previewsize=128&page=1&nl=true')
        login_input = browser.find_element(By.ID, "LoginView_Login_UserName")
        login_input.send_keys(login)
        password_input = browser.find_element(By.ID, "LoginView_Login_Password")
        password_input.send_keys(password)
        browser.find_element(By.ID, "LoginView_Login_LoginButton").click()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


def main():
    shoot_id = shoot_number()
    autorization(shoot_id)

    html = browser.page_source
    total_images = get_total_images(html)  # количество снимков в съемке
    print(f'в съемке находится {cgreen}{total_images}{cend} снимков')

    count = 1
    if total_images <= 200:  # если количество снимков меньше 200 ( количество снимков на странице
        number_of_downloads = total_images  # количество скачиваний на странице с 200 картинками будет такое
        page = 1  # номер страницы с которой выкачиваю фото
        download_one_page(number_of_downloads, shoot_id, page, count)
        browser.close()
        browser.quit()

    else:  # если больше 200 снимков то нужно будет открывать новые страницы
        pages_number = total_images // 200
        # print(f'pages_number - {pages_number}')
        for page in range(1, pages_number + 2):
            if page != pages_number + 1:
                number_of_downloads = 200
            else:

                number_of_downloads = total_images % 200
            download_one_page(number_of_downloads, shoot_id, page,count)
            # print(f'запускаю скачивание со страницы {page}')
    print(f"скачивание завершено")
    browser.close()
    browser.quit()

if __name__ == "__main__":
    main()
