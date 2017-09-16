from config import *
import datetime
import time

while True:
    timer = str(datetime.datetime.now())
    timer = timer[11:16]
    if timer == this_moment:
        print("Here we go...")
        start_training()
    else:
        time.sleep(1)
        pass