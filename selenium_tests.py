import threading
import os
import time
from selenium import webdriver

def start_light_app():
    os.system('python grassroot-nlu/main.py')

def test_light_build():
    driver = webdriver.Chrome(service_args=['--verbose'])
    threading.Thread(target=start_light_app).start()
    driver.get('http://localhost:5000/')
    driver.get('http://localhost:5000/datetime?date_string=tomorrow')
    driver.get('http://localhost:5000/nullpath')
    print('driver: %s' % driver)
    print('\n\ndriver.title: %s' % driver.title)
    driver.get('http://127.0.0.1:5000/shutdown')

test_light_build()