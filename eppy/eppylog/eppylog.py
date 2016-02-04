# Copyright (c) 2015 Jamie Bull

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.
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
import logging.config
import os


THIS_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_FILE = os.path.join(THIS_DIR, 'eppylog.ini')

logging.config.fileConfig(CONFIG_FILE, disable_existing_loggers=1)
CONFIG = ConfigParser.ConfigParser()


def getlogger(name):
    """get a logger with the given name
    generally called using `logger = eppylog.getlogger(__name__)`
    """
    return logging.getLogger(name)


def setloggerlevel(logger, level):
    """set the logger level for a given logger
    """
    logger_level = logging.getLevelName(level.upper())
    getlogger(logger).setLevel(logger_level)
    CONFIG.read(CONFIG_FILE)
    CONFIG.set('logger_{0}'.format(logger), 'level', level)
    with open(CONFIG_FILE, 'w') as configfile:
        CONFIG.write(configfile)


def getloggerlevel(logger):
    """get the logger level of a given logger
    """
    CONFIG.read(CONFIG_FILE)
    level = CONFIG.get('logger_{0}'.format(logger), 'level')
    return level


class LogLevel(object):

    """logging decorator that allows you to log at a specified log level.
    usage:
    >>> @eppylog.LogLevel('DEBUG')
    >>> def my_debug_function(*args, **kwargs):
    >>>    '''a function to be logged at the DEBUG level
    >>>    '''
    >>>    ...
    """

    def __init__(self, level='INFO'):
        self.level = logging.getLevelName(level.upper())
        self.levelname = level.upper()
        # set loggers if not set earlier
        self.console_logger = getlogger('console')
        self.json_logger = getlogger('json')
        self.file_logger = getlogger('file')

    def __call__(self, func):
        """returns a wrapper that wraps func and logs its name, parameters,
        and return values
        """

        @functools.wraps(func)
        def wrapped(*args, **kwds):
            """Wrap the function and log its details.
            """
            f_result = func(*args, **kwds)
            self._log_console(func, args, kwds, f_result)
            self._log_json(func, args, kwds, f_result)
            self._log_file(func, args, kwds, f_result)
            return f_result
        return wrapped

    def _log_json(self, func, args, kwds, f_result):
        """log a function call to the JSON log
        """
        return self.json_logger.log(
            self.level,
            {"log_level": self.levelname,
             'function': '%s.%s' % (func.__module__, func.func_name),
             'args': args, 'kwargs': kwds, 'returns': [f_result]})

    def _log_console(self, func, args, kwds, f_result):
        """log a function call to the console
        """
        return self.console_logger.log(
            self.level,
            'function: %s, args: %s, kwargs: %s, returns: [%s]',
            '.'.join([func.__module__, func.func_name]),
            args, kwds, f_result)

    def _log_file(self, func, args, kwds, f_result):
        """log a function call to the log file
        """
        return self.file_logger.log(
            self.level,
            'function: %s, args: %s, kwargs: %s, returns: [%s]',
            '.'.join([func.__module__, func.func_name]),
            args, kwds, f_result)
