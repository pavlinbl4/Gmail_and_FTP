"""
проверяю как работает селениум
"""

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


url ='https://www.tassphoto.com/ru/asset/fullTextSearch/search/%D0%A1%D0%B5%D0%BC%D0%B5%D0%BD%20%D0%9B%D0%B8%D1%85%D0%BE%D0%B4%D0%B5%D0%B5%D0%B2/page/'

options = webdriver.ChromeOptions()
options.add_argument(
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4200.0 Iron Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

browser = webdriver.Chrome(options=options)

def get_html(page_number):
    browser.get(f'{url}')
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "userrequest"))
    )
    search_input = browser.find_element(By.ID, "userrequest")
    search_input.clear()
    search_input.send_keys('Семен Лиходеев')
    search_input.send_keys(Keys.ENTER)
    browser.get(f'{url}{page_number}')
    html = browser.page_source
    browser.save_screenshot(f"page_number-{page_number}.png")
    return html


page_number = 5
get_html(page_number)
browser.close()
browser.quit()




