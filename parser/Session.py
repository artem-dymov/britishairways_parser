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
from selenium.common import exceptions as selenium_exceptions
from selenium.webdriver.remote.shadowroot import ShadowRoot

import undetected_chromedriver as uc
import config
import time

import logging
from typing import Union

from Flight import Flight


class Session:
    def __init__(self):
        # user_agent = ('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36')

        options = Options()

        # options.add_argument('--headless=new')
        # options.add_argument('--headless')

        # options.add_argument(user_agent)
        options.add_argument('--no-sandbox')
        options.add_argument('--start-maximized')

        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-proxy-server')

        # options.add_argument("--proxy-server='direct://'")
        # options.add_argument("--proxy-bypass-list=*")

        self.driver = uc.Chrome(use_subprocess=True, options=options)
        # self.driver = uc.Chrome()

        # Enabling cookie is strictly necessary
        self.open_homepage()
        self.enable_cookie()

        self.page = 0

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

    def waiting_when_page_loaded(self) -> bool:
        try:
            element_if_page_loaded = WebDriverWait(self.driver, 90).until(EC.presence_of_element_located(
                (By.XPATH, '//ba-button[contains(@class, "search")]')
            ))

            return True
        except TimeoutError:
            logging.critical('PAGE LOADING ERROR, TIME ERROR')
            return False

    def make_request(self, weblink) -> None:
        self.driver.get(weblink)

        # if page have this element than page is loaded
        # if page not loaded in 180 sec, this func will return error
        loading_marker: WebElement = WebDriverWait(self.driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//app-flight-list'))
        )
        self.page = 1

    def startup_manual_request(self):
        while True:
            try:
                self.open_homepage()

                # wait until 2 entry forms on homepage will be loaded
                inputs = WebDriverWait(self.driver, 60).until(EC.presence_of_all_elements_located(
                    (By.XPATH, '//input[@name="searchEntry"]')
                ))

                from_input = inputs[0]
                to_input = inputs[1]

                from_input.send_keys('LIS')
                WebDriverWait(self.driver, 120).until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="search-bar-dropdown"]/ul/li')
                )).click()

                to_input.send_keys('NYC')
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@class="search-bar-dropdown"]/ul/li')
                )).click()

                search_button = WebDriverWait(self.driver, 150).until(EC.presence_of_element_located(
                    (By.XPATH, '//button[@class="primary search-button"]'))
                )
                search_button.click()
            except selenium_exceptions.TimeoutException:
                logging.warning('Restarting startup_manual_request')
                print('Restarting startup_manual_request')
                continue

            try:
                self.waiting_when_page_loaded()
                break
            except selenium_exceptions.TimeoutException:
                logging.warning('Restarting startup_manual_request')
                print('Restarting startup_manual_request')
                continue

        print('\nSTARTUP STUF SUCCESSFUL\n')
        logging.info('\nSTARTUP STUF SUCCESSFUL\n')

    # returns None if no flights available
    def parse_page(self) -> Union[list[Flight], None]:
        # TODO add a check if search results in not empty (in that case func must return None)
        # flights_divs = self.driver.find_elements(By.XPATH, '//div[contains(@class, " flight ")]')

        def if_flight_available() -> bool:
            try:
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(
                    (By.XPATH, '//app-flight-list-results')
                ))
                return True
            except selenium_exceptions.NoSuchElementException:
                return False
            except selenium_exceptions.TimeoutException:
                return False

        if self.waiting_when_page_loaded():
            if not if_flight_available():
                self.driver.refresh()
                if self.waiting_when_page_loaded():
                    if not if_flight_available():
                        return None
                else:
                    raise selenium_exceptions.TimeoutException
        else:
            raise selenium_exceptions.TimeoutException


        # it is necessary to wait until staleness
        test_flight = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, '//div[contains(@class, " flight ")]')
        ))
        # WebDriverWait(self.driver, 100).until(EC.staleness_of(test_flight))

        try:
            flights_divs: list[WebElement] = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located(
                (By.XPATH, '//div[contains(@class, " flight ")]')
            ))
        except TimeoutError:
            logging.warning('No flights available.')
            return None

        logging.debug(f'Found {len(flights_divs)} flights.')

        flights: list[Flight] = []
        counter = 1

        for flight_div in flights_divs:
            logging.debug(f'Parsing flight {counter}')
            flights.append(self.parse_flight(flight_div))

            counter += 1
        return flights

    @staticmethod
    def parse_flight(flight_div: WebElement) -> Flight:

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
        # 1 flight card - 1 fare
        flight_cards: list[WebElement] = WebDriverWait(flight_div, 20).until(EC.presence_of_all_elements_located(
            (By.XPATH, './/div[@class="flight-card"]')
        ))

        fares = {}
        for flight_card in flight_cards:
            fare_name = WebDriverWait(flight_card, 20).until(EC.presence_of_element_located(
                (By.XPATH, './/div[@class="flight-card-header"]//span[1]')
            ))
            # 'text' property of WebElement return empty string if element is not visible
            # so in this case we should use 'get_attribute("textContent")' method instead
            fare_name = fare_name.get_attribute('textContent')

            fare_price = WebDriverWait(flight_card, 20).until(EC.presence_of_element_located(
                (By.XPATH, './/div[@class="flight-card-header"]//span[2]')
            ))
            fare_price = fare_price.get_attribute('textContent')

            fare_select_btn = WebDriverWait(flight_card, 10).until(EC.presence_of_element_located(
                (By.XPATH, './/ba-button[contains(@class, "select-button")]')
            ))

            fares.update(
                {fare_name: (fare_price, fare_select_btn)}
            )

        open_flight_cards_btn = WebDriverWait(flight_div, 10).until(EC.presence_of_element_located(
                (By.XPATH, './/ba-button[contains(@class, "flight-button")]')
            ))
        flight = Flight(departure, arrival, company, stops_info, duration_summary, fares, open_flight_cards_btn)
        return flight

    def select_fare(self, select_btn: WebElement):
        def click_agree_button():
            agree_ba_button = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located(
                (By.XPATH, '//ba-button[contains(@class, "agree-button")]')
            ))
            # agree_ba_button2 = self.driver.find_element(By.XPATH, '//ba-button[contains(@class, "agree-button")]')
            self.driver.execute_script('arguments[0].shadowRoot.querySelector("button").click()',
                                       agree_ba_button)
        # shadow_root: ShadowRoot = WebDriverWait(select_btn, 30).until(EC.presence_of_element_located())
        # shadow_root: ShadowRoot = select_btn.shadow_root

        # this line presses on select button and opens page with specified flight and fare
        self.driver.execute_script('arguments[0].shadowRoot.querySelector("button").click()', select_btn)
        self.page = 2

        # second page agree
        click_agree_button()
        self.page = 3

        try:
            logging.debug('closing sign in window')
            # sign in close
            ba_guest_btn = WebDriverWait(self.driver, 25).until(EC.presence_of_element_located(
                (By.XPATH, '//lib-sign-in-modal/ba-modal//ba-button[contains(@class, "guest")]')
            ))
            self.driver.execute_script(
                'return arguments[0].shadowRoot.querySelector("button").click()',
                ba_guest_btn)
        except Exception as e:
            print(e)

    def go_back(self):
        self.driver.back()

    def go_to_flights_page(self):
        while 'flightList' not in self.driver.current_url:
            self.driver.back()


