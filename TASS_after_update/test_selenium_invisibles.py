from selenium import webdriver
import time


options = webdriver.ChromeOptions()
options.add_argument("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0")
options.add_argument("--disable-blink-features=AutomationControlled")
browser = webdriver.Chrome(options=options)

browser.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')
time.sleep(3)

browser.close()
browser.quit()
