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

from selenium.common import exceptions as selenium_exceptions

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


def if_final_page() -> bool:
    try:
        h1: WebElement = WebDriverWait(session.driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//h1')
        ))

        if h1.text.strip().lower() == 'passenger details':
            return True
        else:
            return False
    except Exception:
        return False


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

count = 0
for flight in flights:
    if count == 2:
        # flight.open_flight_cards_btn.click()
        # time.sleep(5)
        for tariff_name, tariff_value in flight.tariffs.items():
            # noinspection PyTypeChecker
            select_btn: WebElement = tariff_value[1]

            session.select_tariff(select_btn)
            if if_final_page():
                logging.info('Final page accessed successfuly!')
            else:
                logging.warning('Erorr accessing final page!!')
            break
    count += 1


print('full end')
time.sleep(60)

# document.querySelector("#ba-button-14").shadowRoot.querySelector("button")