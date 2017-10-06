from config import this_moment,start_training
import datetime
import time

while True:
    timer = str(datetime.datetime.now())
    timer = timer[11:16]  # reader beware. This is a string slice, not a time value
    if timer == this_moment:
        print("Here we go...")
        start_training()
    else:
        time.sleep(1)
        pass