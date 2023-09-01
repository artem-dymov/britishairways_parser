from typing import List

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common import exceptions
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.shadowroot import ShadowRoot
from selenium.webdriver.chrome.options import Options

import undetected_chromedriver as uc
import config
import time

import logging
import random

from Session import Session

logging.basicConfig(level=logging.DEBUG, filename="parser.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

logging.getLogger('selenium.webdriver.common.service').setLevel(logging.CRITICAL)
logging.getLogger('undetected_chromedriver.patcher').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.CRITICAL)

session = Session()

time.sleep(5)
session.startup_manual_request()

origin_dest_data = ['NYC-LON_2023-09-12', 'LON-NYC_2023-09-18', 'LON-WAW_2023-09-11', 'LON-MAD_2023-09-27', 'LON-MAD_2023-10-15',
        'LON-NYC_2023-11-11', 'NYC-WAW_2023-12-10', 'LON-NYC_2023-09-19', 'LON-NYC_2023-09-18']
o_d_dataset = ['NYC-LON', 'LON-NYC, LON-WAW', 'WAW-LON', 'LON-MAD', 'MAD-LON', 'NYC-WAW', 'WAW-NYC']

def create_test_onds():
    o_d = random.choice(origin_dest_data)
    year = '_2023-'

    m = random.randint(9, 12)
    d = random.randint(1, 30)
    m_d = f'{m}-{d}'

    onds = o_d + year + m_d
    return onds


onds = create_test_onds()

weblink = session.create_search_link(onds=onds)
session.make_request(weblink)

flights = session.parse_page()

print('flights parsed')

flights_data = '\n-------------------------------'

counter = 1
for flight in flights:
    flights_data += f'\n\nFlight {counter}' \
                    f'\nDeparture: {flight.departure}' \
                    f'\nArrival: {flight.arrival}' \
                    f'\nCompany: {flight.company}' \
                    f'\nDuration summary: {flight.duration_summary}' \
                    f'\nStops info: {flight.stops_info}' \
                    f'\nTariffs: '

    for tariff_name, tariff_value in flight.tariffs.items():
        flights_data += f'|{tariff_name} - {tariff_value[0]}|'

    counter += 1

flights_data += '\n\n-------------------------------'

logging.debug(flights_data)

print('waiting')
time.sleep(15)


count = 0
for flight in flights:
    if count == 2:
        # flight.open_flight_cards_btn.click()
        time.sleep(5)
        for tariff_name, tariff_value in flight.tariffs.items():
            # noinspection PyTypeChecker
            select_btn: WebElement = tariff_value[1]
            print('clicking')
            # getting access to #shadow-root
            shadow_root: ShadowRoot = select_btn.shadow_root
            # WebDriverWait(shadow_root, 20).until(EC.element_to_be_clickable(
            #     (By.CSS_SELECTOR, 'button')
            # )).click()
            # shadow_root.find_element(By.CSS_SELECTOR, 'button:first-child')

            # DO NOT DELETE!!!!!!!!!!!!!
            # this line presses on select button and opens page with specified flight and tariff
            session.driver.execute_script('arguments[0].shadowRoot.querySelector("button").click()', select_btn)

            break
    count += 1

print('full end')
time.sleep(60)

# document.querySelector("#ba-button-14").shadowRoot.querySelector("button")