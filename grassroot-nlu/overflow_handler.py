import time
import os
from logger import rootLogger

def overflow_handler():
    try:
    	rootLogger.info('Cleaning overflow counter...')
    	os.system('rm logs/overflowBlock')
    	file = open('logs/overflowBlock', 'w')
    	file.write('0')
    	file.close()
    	rootLogger.info('overflowBlock cleared.')
    	time.sleep(60)
    except Exception as e:
    	rootLogger.error(str(e))

while True:
	overflow_handler()