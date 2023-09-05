import time

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
