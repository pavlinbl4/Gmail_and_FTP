from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Firefox()

site = "http://1kas.sudrf.ru/modules.php?name=sud_delo#"
driver.get(site)
driver.find_element(By.ID, "top_menu").find_element(By.TAG_NAME, "b").click()
driver.implicitly_wait(5)
driver.find_element(By.NAME, "dic").click()

driver.find_element(By.ID, 'popup')
driver.find_element(By.CLASS_NAME, "bsrLawBook").find_element(By.NAME, "lwbart-sublevel").click()

check_box = driver.find_element(By.ID, "lwbart-inp-780000")
actions = ActionChains(driver)
actions.move_to_element(check_box)
driver.find_element(By.ID, "lwbart-inp-780000").click()
driver.find_element(By.CSS_SELECTOR, '#sublevel-00 > ul:nth-child(1) > li:nth-child(17) > a:nth-child(1)').click()

driver.find_element(By.ID, "lwbart-inp-780010").click()
driver.find_element(By.ID, "lwbart-inp-780020").click()
driver.find_element(By.ID, "lwbart-inp-780030").click()
driver.find_element(By.ID, "lwbart-inp-780040").click()

driver.find_element(By.ID, "cat_close").find_element(By.TAG_NAME, "a").click()

time.sleep(3)
driver.implicitly_wait(5)

driver.find_element(By.NAME, "Submit").click()
time.sleep(3)

url = driver.current_url
print(url)

driver.save_screenshot('itog.png'
)

driver.close()
