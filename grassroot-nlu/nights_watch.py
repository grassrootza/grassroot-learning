from config import *
import datetime
import time

while True:
    timer = str(datetime.datetime.now())
    timer = timer[11:16]
    if timer == '13:55':
        print("Here we go...")
        start_training()
    else:
        time.sleep(0.5)
        pass