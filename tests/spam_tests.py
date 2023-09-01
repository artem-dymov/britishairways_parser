from Session import Session
import time
import random
import logging

import traceback


# logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
# logger.setLevel(logging.NOTSET)

logging.basicConfig(level=logging.DEBUG, filename="parser.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

logging.getLogger('selenium.webdriver.common.service').setLevel(logging.CRITICAL)
logging.getLogger('undetected_chromedriver.patcher').setLevel(logging.CRITICAL)
logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.CRITICAL)

# format="%(asctime)s %(levelname)s %(message)s"
loggers = logging.Logger.manager.loggerDict.keys()
print(loggers)


logging.info('Creating session.')
session = Session()

logging.info('Doing startup request.')
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


test_times = []
for i in range(1):
    logging.info(f'\n\nTest iteration №{i}')
    onds = create_test_onds()

    print(f'Created random onds: {onds}')
    start_time = time.time()

    logging.info('Creating weblink.')
    weblink = session.create_search_link(onds=onds)

    try:
        logging.debug(f'Request weblink: {weblink}')
        logging.info('Making request')
        session.make_request(weblink)
        logging.info('Request made successfully')
    except Exception as e:
        logging.critical(f'Error occurred!\n{e}')
        print('Test failed')
        traceback.format_exc()
        continue

    try:
        logging.info('Parsing page...')
        flights = session.parse_page()
        print(f'flights: {flights}')
        logging.info('Page parsed successfully!')


        flights_data = '\n-------------------------------'

        counter = 1
        for flight in flights:
            flights_data += f'\n\nFlight {counter}' \
                             f'\nDeparture: {flight.departure}' \
                             f'\nArrival: {flight.arrival}' \
                             f'\nCompany: {flight.company}' \
                             f'\nDuration summary: {flight.duration_summary}' \
                             f'\nStops info: {flight.stops_info}' \
                             f'\nDetailed info link: {flight.detailed_info_link}' \
                             f'\nTariffs: '

            for tariff_name, tariff_price in flight.tariffs.items():
                flights_data += f'|{tariff_name} - {tariff_price}|'

            counter += 1

        flights_data += '\n\n-------------------------------'

        logging.debug(flights_data)
    except Exception as e:
        logging.critical(f'Error occurred!\n{e}')
        print('Test failed')
        traceback.format_exc()
        continue

    test_time = time.time() - start_time
    test_times.append(test_time)

    print('Test completed', f'\nTime spend in seconds: {test_time}','\n')

print('TEST ENDED')

if test_times:
    test_times.sort()
    test_times.reverse()

    print('MAX TIME SPENDED (5 biggest)')
    print(test_times)

    for i in range(1):
        print(test_times[i])

    sum = 0.0
    for i in test_times:
        sum += i

    average = sum / len(test_times)
    print(f'AVERAGE TEST TIME: {average}')

time.sleep(200)