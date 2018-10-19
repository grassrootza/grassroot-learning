from logger import rootLogger
import time
import os
import threading
from mail_service import mail

def notify_dev():
    time.sleep(180)
    rootLogger.info('Attempting to send nlu requests to developer.')
    file = open('logs/requests.txt', 'a')
    file.close()
    f = open('logs/requests.txt', 'r')
    ff = f.read()
    f.close()
    os.remove('logs/requests.txt')
    requests = ff.split('\n')
    rootLogger.info('found requests: %s' % requests)
    if len(requests) > 1:
    	mail(str(ff), 'Training Data')
    else:
    	rootLogger.info('No new requests found.')


while True:
    notify_dev()