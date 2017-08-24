#!/usr/bin/env python2.7

"""Define the output log function"""

import logging
import time
import os
import constants

log_path = constants.LOG_PATH
test_build = constants.TEST_BUILD

class Log:
    def __init__(self):
        now1 = time.strftime('%Y-%m-%d')
        now2 = time.strftime('%H-%M-%S')
        tmp_log_dir = os.path.join(log_path, '{0}'.format(now1), '{0}'.format(now2), '{0}'.format(test_build))
        if not os.path.exists(tmp_log_dir):
            os.makedirs(tmp_log_dir)
        tmp_log_path = os.path.join(tmp_log_dir, 'final_result.log')
        if not os.path.exists(tmp_log_path):
            os.mknod(tmp_log_path)
        #self.logname = os.path.join(tmp_log_dir, 'final_result.log')
        self.logname = tmp_log_path

    def __printconsole(self, level, message):
        # Create  a logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # Create a handler, write to the log file
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # Create a streamhandler , output the log to the console
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        # define handler output formatter
        formatter = logging.Formatter('[%(module)s]%(asctime)s (%(funcName)s) %(levelname)s :: %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)

        # Add handler to logger
        logger.addHandler(fh)
        logger.addHandler(sh)

        # record the message
        if level == 'info':
            logger.info(message)
        elif level == 'debug':
            logger.debug(message)
        elif level == 'warning':
            logger.warning(message)
        elif level == 'error':
            logger.error(message)
        logger.removeHandler(sh)
        logger.removeHandler(fh)
        fh.close()

    def debug(self, message):
        self.__printconsole('debug', message)

    def info(self, message):
        self.__printconsole('info', message)

    def warning(self, message):
        self.__printconsole('warning', message)

    def error(self, message):
        self.__printconsole('error', message)



