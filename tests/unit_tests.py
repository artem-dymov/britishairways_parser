from parser.Session import Session
import time


def show_current_time():
    current_time = time.localtime(time.time())
    return f'Current system time: {current_time.tm_hour}h {current_time.tm_min}m {current_time.tm_sec}s'

def autocomplete_test():
    session = Session()

    try:
        session.startup_manual_request()
        print(f'Test completed successfully. {show_current_time()}\n\n')

        session.driver.close()
        del session

    except Exception as e:
        print(f'Test failed. {show_current_time()}\n\n')

    time.sleep(2)

for i in range(100):
    autocomplete_test()

