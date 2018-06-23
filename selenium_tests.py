import threading
import os
import time
from selenium import webdriver

def start_light_app():
    os.system('python grassroot-nlu/main.py')

def test_light_build():
    driver = webdriver.Chrome(service_args=['--verbose'])
    threading.Thread(target=start_light_app).start()
    time.sleep(3)
    driver.get('http://localhost:5000/')
    assert "Grassroot-nlu" in driver.title
    os.system('curl localhost:5000/shutdown')

test_light_build()