import logging

logFormatter = logging.Formatter("[NLULOGS] %(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("{0}/{1}.log".format('logs/', 'nlu'))
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)