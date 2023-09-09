from parser.Session import Session
import time
import random
import logging

import traceback

from selenium.webdriver.common.by import By

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.remote.webelement import WebElement


# logger = logging.getLogger('selenium.webdriver.remote.remote_connection')
# logger.setLevel(logging.NOTSET)

def spam_tests():
    logging.basicConfig(level=logging.DEBUG, filename=f"parser.log", filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    logging.getLogger('selenium.webdriver.common.service').setLevel(logging.CRITICAL)
    logging.getLogger('undetected_chromedriver.patcher').setLevel(logging.CRITICAL)
    logging.getLogger('urllib3.connectionpool').setLevel(logging.CRITICAL)
    logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.CRITICAL)

    # format="%(asctime)s %(levelname)s %(message)s"
    loggers = logging.Logger.manager.loggerDict.keys()

    # -----------------


    logging.info('Creating session.')
    session = Session()

    logging.info('Doing startup request.')
    time.sleep(5)
    session.startup_manual_request()


    origin_dest_data = ['NYC-LON_2023-09-12', 'LON-NYC_2023-09-18', 'LON-WAW_2023-09-11', 'LON-MAD_2023-09-27', 'LON-MAD_2023-10-15',
            'LON-NYC_2023-11-11', 'NYC-WAW_2023-12-10', 'LON-NYC_2023-09-19', 'LON-NYC_2023-09-18']
    o_d_dataset = ['NYC-LON', 'LON-NYC', 'LON-WAW', 'WAW-LON', 'LON-MAD', 'MAD-LON', 'NYC-WAW', 'WAW-NYC']

    # https://www.britishairways.com/travel/book/public/en_ua/flightList?onds=LON-NYC,%20LON-WAW_2023-12-4&ad=1&yad=0&ch=0&inf=0&cabin=M&flex=LOWEST&ond=1
    def create_test_onds():
        o_d = random.choice(o_d_dataset)
        year = '_2023-'

        m = random.randint(9, 12)
        d = random.randint(1, 30)
        m_d = f'{m}-{d}'

        onds = o_d + year + m_d
        return onds


    def if_book_page() -> bool:
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

    def show_time_results(subm_fl):
        if subm_fl:
            subm_fl.sort()
            subm_fl.reverse()

            print('\nMAX TIME SPENDED (5 biggest)')
            logging.info(f'MAX TIME SPENDED (5 biggest)\n{subm_fl[0]}\n{subm_fl[1]}\n'
                         f'{subm_fl[2]}\n{subm_fl[3]}\n{subm_fl[4]}')

            for i in range(5):
                print(subm_fl[i])

            sum = 0.0
            for i in subm_fl:
                sum += i

            average = sum / len(subm_fl)
            print(f'AVERAGE SUBMITTING TEST TIME: {average}')
            logging.info(f'AVERAGE SUBMITTING TEST TIME: {average}\n\n')


    test_times = {
        'flights_parsing': [],
        'submitting_flight': []
    }
    failed_tests = {
        'flights_parsing': 0, 'submitting_flight': 0
    }
    for i in range(5):
        logging.info(f'\n\nTest iteration №{i}')
        onds = create_test_onds()

        start_flights_parsing_time = time.time()

        logging.info('Creating weblink.')
        weblink = session.create_search_link(onds=onds)

        # TEST 1
        # Getting access to page with flights and parsing flights data
        logging.info('\nBeginning TEST 1\n')

        try:
            logging.debug(f'Request weblink: {weblink}')
            logging.info('Making request')
            session.make_request(weblink)
            logging.info('Request made successfully')
        except Exception as e:
            logging.critical(f'Error occurred!\n{e}')
            print('Test failed')
            traceback.format_exc()

            failed_tests['flights_parsing'] += 1
            failed_tests['flights_parsing'] += 1
            continue

        try:
            logging.info('Parsing page...')
            flights = session.parse_page()

            if not flights:
                logging.info('No flights available. Skipping this request.')
                print('No flights available. Skipping this request.')
                continue

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
                                 f'\nfares: '

                for fare_name, fare_price in flight.fares.items():
                    flights_data += f'|{fare_name} - {fare_price}|'

                counter += 1

            flights_data += '\n\n-------------------------------'

            logging.debug(flights_data)
        except Exception as e:
            logging.critical(f'Error occurred! TEST 1 FAILED!\n{e}')
            print(e)
            print('TEST 1 failed')
            traceback.format_exc()

            failed_tests['flights_parsing'] += 1
            continue

        flights_parsing_time = time.time() - start_flights_parsing_time
        test_times['flights_parsing'].append(flights_parsing_time)

        logging.info(f'\nFlights parsing test completed.\nTime spend in seconds: {flights_parsing_time}\n')
        print(f'Flights parsing test completed\nTime spend in seconds: {flights_parsing_time}\n')

        # TEST 2
        # Test access to book page of flights

        # choosing random flight from all flights on page to test booking
        # count = 0
        # choice_flight = random.randint(0, len(flights)-1)
        #
        # for flight in flights:
        #     if count == choice_flight:
        #
        #         # flight.open_flight_cards_btn.click()
        #
        #         # choosing random fare of flight to test booking
        #         fare_count = 0
        #         choice_fare = random.randint(0, len(flight.fares.keys())-1)
        #         for fare_name, fare_value in flight.fares.items():
        #             if fare_count == choice_fare:
        #                 start_submitting_flight_time = time.time()
        #
        #                 # noinspection PyTypeChecker
        #                 select_btn: WebElement = fare_value[1]
        #
        #                 try:
        #                     session.select_fare(select_btn)
        #                 except Exception as e:
        #                     logging.warning(f'Error accessing book page (select_fare func returned error)!! TEST 2 FAILED!!\n{e}')
        #
        #                     failed_tests['submitting_flight'] += 1
        #                     continue
        #
        #
        #                 if if_book_page():
        #                     logging.info('Final page accessed successfuly!')
        #                 else:
        #                     print('THIS EXCEPTION')
        #                     logging.warning('Error accessing book page (not book page in the end)!! TEST 2 FAILED!!!')
        #
        #                     failed_tests['submitting_flight'] += 1
        #                     continue
        #
        #                 session.go_to_flights_page()
        #
        #                 submitting_flight_time = time.time() - start_submitting_flight_time
        #                 test_times['submitting_flight'].append(submitting_flight_time)
        #
        #             fare_count += 1
        #     count += 1

    print('TEST ENDED')

    # print(test_times['submitting_flight'])
    # subm_fl = test_times['submitting_flight']
    # print('\n\nSUBMITTING FLIGHT TIME RESULTS')
    # show_time_results(subm_fl)

    fl_par = test_times['flights_parsing']
    print('\n\nPARSING FLIGHTS TIME RESULTS')
    show_time_results(fl_par)

    print(f'FAILED TESTS:\n{failed_tests}')


if __name__ == '__main__':
    spam_tests()