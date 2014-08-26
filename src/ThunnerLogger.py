from os import path, makedirs
from traceback import print_exception
from time import time
from  datetime import datetime

class ThunnerLogger:
    """
    Class responsible for handling the logs for thunner
    """

    # Constants
    LOGS_DIR = 'logs'
    DEBUG_PATH = 'logs/debug.log'
    ERROR_PATH = 'logs/error.log'
    MESSAGE_FORMAT = '[%s] [%s] %s\n'
    TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S'
    DEBUG_CONFIG_KEY = 'debug'

    debugEnabled = False

    def __init__(self, config = None):
        """
        Initializes the an instance of ThunnerLogger

        :param config: Dict containing the configuration for thunner.
                        if config is None, debugging messages will not be displayed
        """
        if not path.exists(self.LOGS_DIR):
            makedirs(self.LOGS_DIR)
        if config is not None and self.MESSAGE_FORMAT not in config:
            self.debugEnabled = config[self.DEBUG_CONFIG_KEY]

    def getTimeAndDate(self):
        """
        Get time and date string for logging

        :return: String containing the time and date in the appropriate format
        """
        return datetime.fromtimestamp(time()).strftime(self.TIMESTAMP_FORMAT)

    def error(self, system, message = None):
        """
        Write an error to the log

        :param system: Instance of system used to extract the stack trace
                        This parameter cant be None
        :param message: String containing an error message.
                        If this parameter is None, the default error message will be displayed
        :return:
        """
        if system is None:
            return
        errorType, errorValue, stackTrace = system.exc_info()
        timeStamp = self.getTimeAndDate()
        errorMessage = message if message is not None else 'No error message specified'
        with open(self.ERROR_PATH, 'a+') as errorLogFile:
            errorLogFile.write(self.MESSAGE_FORMAT % (timeStamp, 'ERROR', errorMessage))
            print_exception(errorType, errorValue, stackTrace, file = errorLogFile)

    def debug(self, message = None):
        """
        Write a debug message to the log

        :param message: Message that will be displayed
                    If this parameter is None, nothing will be written to the log
        :return:
        """
        if message is None or not self.debugEnabled:
            return
        timeStamp = self.getTimeAndDate()
        with open(self.DEBUG_PATH, 'a+') as debugLogFile:
            debugLogFile.write(self.MESSAGE_FORMAT % (timeStamp, 'DEBUG', message))