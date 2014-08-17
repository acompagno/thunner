from os import path, makedirs
from traceback import print_exception
from time import time
from  datetime import datetime

# Class in charge of of the logs for thunner
class ThunnerLogger:

    # Constants
    LOGS_DIR = 'logs'
    DEBUG_PATH = 'logs/debug.log'
    ERROR_PATH = 'logs/error.log'
    DEBUG_FORMAT = '[%s] %s\n'
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEBUG_CONFIG_KEY = 'debug'

    debugEnabled = False

    def __init__(self, config = None):
        if not path.exists(self.LOGS_DIR):
            makedirs(self.LOGS_DIR)
        if config != None and self.DEBUG_FORMAT not in config:
            self.debugEnabled = config[self.DEBUG_CONFIG_KEY]


    # Write to error log
    def error(self, system = None):
        if system == None:
            return
        type, value, trace = system.exc_info()
        with open(self.ERROR_PATH, 'a+') as errorLogFile:
            print_exception(type, value, trace, file = errorLogFile)

    # Write to debug log
    def debug(self, message = None):
        if message == None or not self.debugEnabled:
            return
        timeStamp = datetime.fromtimestamp(time()).strftime(self.TIMESTAMP_FORMAT)
        with open(self.DEBUG_PATH, 'a+') as debugLogFile:
            debugLogFile.write(self.DEBUG_FORMAT % (timeStamp, message))