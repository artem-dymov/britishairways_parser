from Session import Session
import time
import random
import logging

import traceback

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

from threading import Thread

from tests.custom_tests import spam_tests

# Создаем потоки для каждой вкладки
threads = []

for i in range(4):
    thread = Thread(target=spam_tests, args=(i,))
    threads.append(thread)

# Запускаем потоки
for thread in threads:
    thread.start()
    time.sleep(2)

# Ждем завершения всех потоков
for thread in threads:
    thread.join()


# session = Session()

# time.sleep(5)
# session.startup_manual_request()
# time.sleep(20)
# search_link = session.create_search_link('MAD-LHR_2023-09-10')
# session.make_request(search_link)
# time.sleep(30)
# print(session.parse_flight())
#
# time.sleep(20)
# search_link = session.create_search_link('NYC-LON_2023-09-12')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('LON-NYC_2023-09-18')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('LON-WAW_2023-09-11')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('LON-MAD_2023-09-27')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('LON-MAD_2023-10-15')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('LON-NYC_2023-11-11')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('NYC-WAW_2023-12-10')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('LON-NYC_2023-09-19')
# session.make_request(search_link)
#
# time.sleep(20)
# search_link = session.create_search_link('LON-NYC_2023-09-18')
# session.make_request(search_link)
#

