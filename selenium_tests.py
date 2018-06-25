import threading
import os
import time
from selenium import webdriver

def start_light_app():
    os.system('python grassroot-nlu/main.py')

def test_light_build():
    driver = webdriver.Chrome(service_args=['--verbose'])
    threading.Thread(target=start_light_app).start()
    time.sleep(40)
    driver.get('http://localhost:5000/')
    if '404' in driver.title:
    	raise ValueError("path not available.")
    driver.get('http://localhost:5000/datetime?date_string=tomorrow')
    if '404' in driver.title:
    	raise ValueError("path not available.")
    driver.get('http://127.0.0.1:5000/shutdown')
    driver.close()

test_light_build()