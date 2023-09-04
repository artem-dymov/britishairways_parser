from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as us
import config

import time

options = Options()
options.add_argument(config.user_agent)
options.add_argument('--no-sandbox')
options.add_argument("--start-maximized")

options.add_argument("--enable-javascript")

# options.add_argument('--headless=new')

driver = us.Chrome(options=options)

print(0)
# driver.get('https://www.britishairways.com/travel/home/public/en_ua/')
driver.get('https://www.britishairways.com/travel/book/public/en_ua/flightList?onds=MAD-LHR_2023-08-30&ad=1&yad=0&ch=0&inf=0&cabin=M&flex=LOWEST&ond=1')
try:
    time.sleep(4)
    cookie_btn = driver.find_element(By.XPATH, '//button[@id="ensCloseBanner"]')
    cookie_btn.click()
except Exception as e:
    print(e)

time.sleep(200)
# driver.get('https://www.britishairways.com/travel/book/public/en_ua/flightList?onds=MAD-LHR_2023-08-26&ad=1&yad=0&ch=0&inf=0&cabin=M&flex=LOWEST&ond=1')
print('1')
print(driver.find_element(By.XPATH, '//div[contains(@class, " flight ")]//ba-content//span[contains(@class, "heading-sm")]').text)
