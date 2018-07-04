import threading
import os
import time
import requests
from selenium import webdriver

def start_light_app():
    os.system('python grassroot-nlu/main.py')

def test_light_build():
    driver = webdriver.Chrome(service_args=['--verbose'])
    threading.Thread(target=start_light_app).start()
    time.sleep(200)
    # driver.get('http://localhost:5000/')
    x = requests.get('http://localhost:5000/').content
    print('x: %s' % x)
    if 'What would you like to do' in str(x):
        print('home page retrieved successfully')
    else:
    	raise ValueError("path not available.")

    # driver.get('http://localhost:5000/datetime?date_string=tomorrow')
    y = requests.get('http://localhost:5000/datetime?date_string=tomorrow').content
    print('y: %s' % y)
    if len(y) == 16:
        print('datetime engine seems operational')
    else:
    	raise ValueError("path not available.")

    driver.get('http://127.0.0.1:5000/shutdown')
    driver.close()

test_light_build()