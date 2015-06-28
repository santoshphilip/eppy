"""py.test for eppylog"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from logging import Logger

from testfixtures import LogCapture
import pytest

from eppy import eppylog

@eppylog.loglevel('info')
def decorated_info_function(a, b, c=0):
    return a * b + c

@eppylog.loglevel('debug')
def decorated_debug_function(a, b, c=0):
    return a * b + c

def test_getlogger():
    """ensure a logger is created when we try to create one.
    """
    logger1 = eppylog.getlogger(__name__)
    assert isinstance(logger1, Logger)

def test_logdecorator():
    """test that logging using a decorator works
    """
    with LogCapture() as l:
        decorated_info_function(2, 4, c=6)
    l.records[0].msg['timestamp'] = 1435000000.0
    l.check(("eppy.tests.test_eppylog",
        "INFO",
        "{u'log_level': 20, u'timestamp': 1435000000.0, u'args': (2, 4), u'call': u'eppy.tests.test_eppylog.decorated_info_function', u'return_values': [14], u'kwargs': {'c': 6}}",)
            )

    with LogCapture() as l:
        decorated_debug_function(2, 4, c=6)
    l.records[0].msg['timestamp'] = 1435000000.0
    l.check(("eppy.tests.test_eppylog",
        "DEBUG",
        "{u'log_level': 10, u'timestamp': 1435000000.0, u'args': (2, 4), u'call': u'eppy.tests.test_eppylog.decorated_debug_function', u'return_values': [14], u'kwargs': {'c': 6}}",)
            )

def test_sethandlerlevel():
    """check that setting the handler level for a given handler works.
    """
    # get current handler level
    current_level = eppylog.gethandlerlevel('jsonHandler')
    eppylog.sethandlerlevel('jsonHandler', 'INFO')
    new_level = eppylog.gethandlerlevel('jsonHandler')
    eppylog.sethandlerlevel('jsonHandler', current_level)
    assert new_level == 'INFO'