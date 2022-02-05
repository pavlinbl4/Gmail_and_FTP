from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Firefox()

site = "http://1kas.sudrf.ru/modules.php?name=sud_delo#"
driver.get(site)
driver.find_element(By.ID,"top_menu").find_element(By.TAG_NAME,"b").click()
time.sleep(5)
driver.find_element(By.NAME,"dic").click()
time.sleep(15)



driver.close()