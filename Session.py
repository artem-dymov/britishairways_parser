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

import logging
from typing import Union

from Flight import Flight


class Session:
    def __init__(self):
        user_agent = ('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')

        options = Options()

        # options.add_argument('--headless=new')

        # options.add_argument(user_agent)
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')

        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-gpu')

        self.driver = uc.Chrome(use_subprocess=True, options=options)
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

        # if page have this element than page is loaded
        # if page not loaded in 180 sec, this func will return error
        loading_marker: WebElement = WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//app-flight-list'))
        )

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

        search_button = WebDriverWait(self.driver, 150).until(EC.presence_of_element_located(
            (By.XPATH, '//button[@class="primary search-button"]'))
        )
        search_button.click()

    # returns None if no flights available
    def parse_page(self) -> Union[list[Flight], None]:
        # TODO add a check if search results in not empty (in that case func must return None)
        # flights_divs = self.driver.find_elements(By.XPATH, '//div[contains(@class, " flight ")]')

        # it is necessary to wait until staleness
        test_flight = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
            (By.XPATH, '//div[contains(@class, " flight ")]')
        ))
        WebDriverWait(self.driver, 30).until(EC.staleness_of(test_flight))

        try:
            flights_divs = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@class, " flight ")]')
            ))
        except TimeoutError:
            logging.info('No flights available.')
            return None

        logging.debug(f'Found {len(flights_divs)} flights.')

        flights: list[Flight] = []
        counter = 1

        for flight_div in flights_divs:
            logging.debug(f'Parsing flight {counter}')
            flights.append(self.parse_flight(flight_div))

            counter += 1

        return flights

    def parse_flight(self, flight_div: WebElement) -> Flight:
        logging.debug('Parsing flight data.')
        # print('\ninnerHTML')
        # print(flight_div.get_attribute('innerHTML'))

        # print('\n\nshadow_root')
        # try:
        #     x = flight_div.shadow_root
        #     print(x)
        # except Exception as e:
        #     print('shadow error')
        #     print(e)

        # time and location
        departure: WebElement = WebDriverWait(flight_div, 20).until(EC.presence_of_element_located(
            (By.XPATH, './/h4/span[1]')

        ))
        departure: str = departure.text

        arrival: WebElement = WebDriverWait(flight_div, 20).until(EC.presence_of_element_located(
            (By.XPATH, './/h4/span[2]')
        ))
        arrival: str = arrival.text

        company: WebElement = WebDriverWait(flight_div, 20).until(EC.presence_of_element_located(
            (By.XPATH, './/div/div/span[1]/span[1]/span[1]')
        ))
        company: str = company.text

        stops_info: WebElement = WebDriverWait(flight_div, 20).until(EC.presence_of_element_located(
            (By.XPATH, './/div/div/span[2]/span')
        ))
        stops_info: str = stops_info.text

        duration_summary: WebElement = WebDriverWait(flight_div, 20).until(EC.presence_of_element_located(
            (By.XPATH, './/div/div/span[3]')
        ))
        duration_summary: str = duration_summary.text

        # every flight can contain several flight cards
        # 1 flight card - 1 tariff
        flight_cards: list[WebElement] = WebDriverWait(flight_div, 20).until(EC.presence_of_all_elements_located(
            (By.XPATH, './/div[@class="flight-card"]')
        ))

        tariffs = {}
        for flight_card in flight_cards:
            print('tariff for')
            tariff_name = WebDriverWait(flight_card, 20).until(EC.presence_of_element_located(
                (By.XPATH, './/div[@class="flight-card-header"]//span[1]')
            ))
            print(f'tariff name in parser: {tariff_name.text}')
            # 'text' property of WebElement return empty string if element is not visible
            # so in this case we should use 'get_attribute("textContent")' method instead
            tariff_name = tariff_name.get_attribute('textContent')

            tariff_price = WebDriverWait(flight_card, 20).until(EC.presence_of_element_located(
                (By.XPATH, './/div[@class="flight-card-header"]//span[2]')
            ))
            tariff_price = tariff_price.get_attribute('textContent')

            tariff_select_btn = WebDriverWait(flight_card, 10).until(EC.presence_of_element_located(
                (By.XPATH, './/ba-button[contains(@class, "select-button")]')
            ))

            tariffs.update(
                {tariff_name: (tariff_price, tariff_select_btn)}
            )

        open_flight_cards_btn = WebDriverWait(flight_div, 10).until(EC.presence_of_element_located(
                (By.XPATH, './/ba-button[contains(@class, "flight-button")]')
            ))

        flight = Flight(departure, arrival, company, stops_info, duration_summary, tariffs, open_flight_cards_btn)
        print(f'flight: {flight.departure}')
        return flight

    def submit_tariff(self, tariff_select_btn: WebElement):
        pass

