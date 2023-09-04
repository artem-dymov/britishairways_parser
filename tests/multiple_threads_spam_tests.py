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

from tests.spam_tests import spam_tests

# Создаем потоки для каждой вкладки
threads = []

for i in range(6):
    thread = Thread(target=spam_tests, args=(50,))
    threads.append(thread)

# Запускаем потоки
for thread in threads:
    thread.start()
    time.sleep(10)

# Ждем завершения всех потоков
for thread in threads:
    thread.join()
