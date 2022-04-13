"""
протестированный скрипт, котороый открывает страницу с
отчетом на сайте photoxpress и получает информацию о дате составления
отчета
рефакторинг 20220413 - скрипт заносит в текстовый файл дату появления нового отчета
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from datetime import datetime
import os
from user_auth import pxp_user, pxp_pass


def notification(message):
    title = "PXP report"
    command = f'''
    osascript -e 'display notification "{message}" with title "{title}"'
    '''
    os.system(command)

def setting_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # фоновый режим
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # невидимость автоматизации
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
    return chrome_options


def main():
    try:
        browser.get('http://photoxpress.ru/commerce/commerce_base.asp?action=pc')
        browser.switch_to.frame("main_frame")
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=text]')))
        login_input = browser.find_element(By.CSS_SELECTOR, 'input[type=text]')
        password_input = browser.find_element(By.CSS_SELECTOR, 'input[type=password]')
        login_input.send_keys(pxp_user)
        password_input.send_keys(pxp_pass)
        browser.find_element(By.CSS_SELECTOR, 'input[type=image]').click()
        browser.switch_to.frame("left_frame")
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr[3]/td[2]/strong/small/a")))
        browser.find_element(By.XPATH, "/html/body/table[2]/tbody/tr[3]/td[2]/strong/small/a").click()
        browser.switch_to.parent_frame()
        browser.switch_to.frame("right_frame")
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type=image]')))
        browser.find_element(By.CSS_SELECTOR, 'input[type=image]').click()
        period = browser.find_element(By.XPATH, "/html/body/table[1]/tbody/tr/td[2]/strong/small/font[2]").text

        print(period)
        print(datetime.now().strftime("%Y-%m-%d"))
        notification(f"last report date\n\n{period}")


        with open('/Volumes/big4photo/Documents/PXP/reports_date.txt', 'r') as log_file:
            lines = log_file.readlines()
            if len(lines) != 0:
                last_date = lines[-1].strip()[13:]
            else:
                last_date = '*'
        with open('/Volumes/big4photo/Documents/PXP/reports_date.txt', 'a') as log_file:
            if last_date != period:
                log_file.write(f'{datetime.now().strftime("%Y-%m-%d")} - {period}\n')

        browser.close()
        browser.quit()
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()


if __name__ == '__main__':
    browser = webdriver.Chrome(options=setting_chrome_options())
    main()
