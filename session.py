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

import undetected_chromedriver as uc
import config
import time


class Session:
    def __init__(self):
        user_agent = ('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')

        options = Options()

        # options.add_argument('--headless=new')

        options.add_argument(user_agent)
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')

        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-gpu')

        self.driver = uc.Chrome(use_subprocess=True)
        # self.driver = uc.Chrome()

        # Enabling cookie is strictly necessary
        self.open_homepage()
        self.enable_cookie()

        time.sleep(1)

        # self.driver.tab_new(config.homepage_weblink)

    def open_homepage(self) -> None:
        self.driver.get(config.homepage_weblink)

    def enable_cookie(self) -> None:
        # cookie acceptance button
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//button[@id="ensCloseBanner"]').click()

    # https://www.britishairways.com/travel/book/public/en_us/flightList?onds=LON-LIS_2023-08-28&ad=1&yad=0&ch=0&inf=0&cabin=M&flex=LOWEST&ond=1
    @staticmethod
    def create_search_link(onds, ad=1, yad=0, ch=0, inf=0, cabin='M', flex='LOWEST', ond=1) -> str:
        params = f'?onds={onds}&ad={ad}&yad={yad}&ch={ch}&inf={inf}&cabin={cabin}&flex={flex}&ond={ond}'
        weblink = config.base_request_link + params
        return weblink

    def make_request(self, weblink) -> None:
        self.driver.get(weblink)

    def startup_manual_request(self):
        inputs = self.driver.find_elements(By.XPATH, '//input[@name="searchEntry"]')

        from_input = inputs[0]
        to_input = inputs[1]

        from_input.send_keys('LIS')
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//div[@class="search-bar-dropdown"]/ul/li').click()

        to_input.send_keys('NYC')
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//div[@class="search-bar-dropdown"]/ul/li').click()

        time.sleep(2)
        # print('manual search submit start')
        search_button = self.driver.find_element(By.XPATH, '//button[@class="primary search-button"]')
        # print('manual search submit end')
        search_button.click()



    def parse_flight(self):
        locations = self.driver.find_element(By.XPATH, '//main//h1').text
        return locations
