"""
eppy_log.py
~~~~~~~~~~~
A utility module for enabling logging in Eppy. See EEP!1 for details of the
intended implementation when complete.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import ConfigParser
import functools
import logging
import logging.config
import logging.handlers
import os
import time


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(THIS_DIR, 'eppylog.ini')

logging.config.fileConfig(CONFIG_FILE, disable_existing_loggers=1)
config = ConfigParser.ConfigParser()


def getlogger(name):
     return logging.getLogger(name)

def sethandlerlevel(handler, level):
    """
    TODO: Try to allow sethandlerlevel to be set during runtime
    """
    config.read(CONFIG_FILE)
    config.set('handler_{0}'.format(handler), 'level', level)
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def gethandlerlevel(handler):
    """get the handler level of a given handler, e.g. jsonHandler
    """
    config.read(CONFIG_FILE)
    level = config.get('handler_{0}'.format(handler), 'level')
    return level
    

class loglevel(object):
    """Logging decorator that allows you to log at a specified log level.
    """

    def __init__(self, level='INFO'):
        self.level = logging._levelNames[level.upper()]

    def __call__(self, func):
        """Returns a wrapper that wraps func and logs its name, parameters,
        and return values.
        """
        # set logger if it was not set earlier
        self.logger = getlogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwds):
            f_result = func(*args, **kwds)
            self.logger.log(
                self.level,
                {'timestamp': time.time(),
                 'log_level': self.level,
                 'call': '{0}.{1}'.format(func.__module__, func.func_name),
                 'args': args,
                 'kwargs': kwds,
                 'return_values': [f_result]})
            return f_result
        return wrapper  
