import threading
import os
import time
from selenium import webdriver

def start_light_app():
    os.system('python grassroot-nlu/main.py')

def test_light_build():
    driver = webdriver.Chrome(service_args=['--verbose'])
    threading.Thread(target=start_light_app).start()
    x = driver.get('http://localhost:5000/')
    y = driver.get('http://localhost:5000/datetime?date_string=tomorrow')
    z = driver.get('http://localhost:5000/nullpath')
    try:
        print('x: %s, \n\ny: %s, \n\nz: %s' % (x,y,z))
    except:
    	pass
    print('driver: %s' % driver)
    print('\n\ndriver.title: %s' % driver.title)
    driver.get('http://127.0.0.1:5000/shutdown')

test_light_build()