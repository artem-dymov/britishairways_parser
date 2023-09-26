from parser.Session import Session
import time
import random
import logging

import traceback

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement

from multiprocessing import Process
from multiprocessing import Manager, Queue

from api.process_session import process_session


print('Starting test')

manager = Manager()
queue: Queue = manager.Queue()
results = manager.dict()

processes = []
for i in range(1):
    process = Process(target=process_session, args=(queue, results,))

    process.daemon = True
    process.start()
    process.join()
    processes.append(process)



print(processes)
print('for completed')
# print('after sleeping')

# processes.reverse()
