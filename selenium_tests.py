import threading
import os
import time
from selenium import webdriver

def start_light_app():
    os.system('python grassroot-nlu/main.py')

def test_light_build():
    driver = webdriver.Chrome(service_args=['--verbose'])
    threading.Thread(target=start_light_app).start()
    time.sleep(30)
    driver.get('http://localhost:5000/')
    print('driver.title1: %s' % driver.title)
    driver.get('http://localhost:5000/datetime?date_string=tomorrow')
    print('driver.title2: %s' % driver.title)
    driver.get('http://localhost:5000/nullpath')
    print('\n\ndriver.title3: %s' % driver.title)
    if '404' in driver.title:
    	raise ValueError("No such path.")
    driver.get('http://127.0.0.1:5000/shutdown')
    driver.close()

test_light_build()