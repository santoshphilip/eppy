"""
eppylog.py
~~~~~~~~~~~
A utility module for enabling logging in Eppy. See EEP!1 for details of usage.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ConfigParser
import functools
import json
import logging
import logging.config
import logging.handlers
import os
import time

from pythonjsonlogger import jsonlogger

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(THIS_DIR, 'eppylog.ini')

logging.config.fileConfig(CONFIG_FILE, disable_existing_loggers=1)
config = ConfigParser.ConfigParser()


def getlogger(name):
    """get a logger with the given name
    generally called using `logger = eppylog.getlogger(__name__)`
    """
    return logging.getLogger(name)

def setloggerlevel(logger, level):
    """set the logger level for a given logger
    """
    getlogger(logger).setLevel(logging._levelNames[level])
    config.read(CONFIG_FILE)
    config.set('logger_{0}'.format(logger), 'level', level)
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def getloggerlevel(logger):
    """get the logger level of a given logger
    """
    config.read(CONFIG_FILE)
    level = config.get('logger_{0}'.format(logger), 'level')
    return level
    

class loglevel(object):
    """logging decorator that allows you to log at a specified log level.
    usage:
    >>> @eppylog.loglevel('DEBUG')
    >>> def my_debug_function(*args, **kwargs):
    >>>    '''a function to be logged at the DEBUG level
    >>>    '''
    >>>    ...
    """

    def __init__(self, level='INFO'):
        self.level = logging._levelNames[level.upper()]
        self.levelname = level.upper()
        
    def __call__(self, func):
        """returns a wrapper that wraps func and logs its name, parameters,
        and return values
        """
        # set loggers if not set earlier
        self.console_logger = getlogger('console')
        self.json_logger = getlogger('json')
        self.file_logger = getlogger('file')

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            f_result = func(*args, **kwds)
            self._log_console(func, args, kwds, f_result)
            self._log_json(func, args, kwds, f_result)
            
            self._log_file(func, args, kwds, f_result)
            
            return f_result
        return wrapper  

    def _log_json(self, func, args, kwds, f_result):
        """log a function call to the JSON log
        """
        return self.json_logger.log(
            self.level,
            {"log_level": self.levelname,
             'function':'%s.%s' % (func.__module__, func.func_name),
             'args':args, 'kwargs':kwds, 'returns':[f_result]})

    def _log_console(self, func, args, kwds, f_result):
        """log a function call to the console
        """
        return self.console_logger.log(self.level, 
            'function: {0}, args: {1}, kwargs: {2}, returns: [{3}]'.format(
                '.'.join([func.__module__, func.func_name]), 
                args, kwds, f_result))

    def _log_file(self, func, args, kwds, f_result):
        """log a function call to the log file
        """
        return self.file_logger.log(
            self.level, 
            'function: {0}, args: {1}, kwargs: {2}, returns: [{3}]'.format(
                '.'.join([func.__module__, func.func_name]), 
                args, kwds, f_result))
