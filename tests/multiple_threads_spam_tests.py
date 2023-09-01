from Session import Session
import time
from threading import Thread

# -------
def parse_tab():
    session = Session()
    session.startup_manual_request()
    time.sleep(100)
    weblink = session.create_search_link(onds='MAD-NYC_2023-09-25')
    session.make_request(weblink)
    time.sleep(16)
    print(session.parse_flight())
    time.sleep(180)

# Создаем потоки для каждой вкладки
threads = []
for i in range(4):
    thread = Thread(target=parse_tab)
    threads.append(thread)

# Запускаем потоки
for thread in threads:
    thread.start()
    time.sleep(30)

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
print('ended')
time.sleep(2000)

