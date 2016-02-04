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
"""py.test for eppylog"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from logging import Logger
import json
import os

from testfixtures import LogCapture

from eppy.eppylog import eppylog


THIS_DIR = os.path.dirname(os.path.realpath(__file__))


@eppylog.LogLevel('info')
def decorated_info_function(a, b, c=0):
    """Test function to be logged at INFO level.
    """
    return a * b + c


@eppylog.LogLevel('debug')
def decorated_debug_function(a, b, c=0):
    """Test function to be logged at DEBUG level.
    """
    return a * b + c


def test_getlogger():
    """ensure a logger is created when we try to create one.
    """
    logger1 = eppylog.getlogger(__name__)
    assert isinstance(logger1, Logger)


class TestLogDecorator(object):

    """
    Test that functions are logged as expected when wrapped with the logging
    decorator.

    """

    def setup_method(self, test_method):
        """set log levels to DEBUG
        """
        self.logs = ['file', 'json', 'console']
        self.current_levels = [eppylog.getloggerlevel(log) for
                               log in self.logs]
        for log, _level in zip(self.logs, self.current_levels):
            eppylog.setloggerlevel(log, 'DEBUG')

    def teardown_method(self, test_method):
        """reset log levels to initial levels
        """
        for log, level in zip(self.logs, self.current_levels):
            eppylog.setloggerlevel(log, level)

    def test_logdecorator(self):
        """test that logging using a decorator works
        """
        with LogCapture() as log_cap:
            decorated_info_function(2, 4, c=6)
        log_cap.check(
            ('console',
             'INFO',
             u"function: eppy.tests.test_eppylog.decorated_info_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]"),
            ('json',
             'INFO',
             u"{u'function': u'eppy.tests.test_eppylog.decorated_info_function', u'returns': [14], u'args': (2, 4), u'log_level': u'INFO', u'kwargs': {'c': 6}}"),
            ('file',
             'INFO',
             u"function: eppy.tests.test_eppylog.decorated_info_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]"))

        with LogCapture() as log_cap:
            decorated_debug_function(2, 4, c=6)
        log_cap.check(
            ('console',
             'DEBUG',
             u"function: eppy.tests.test_eppylog.decorated_debug_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]"),
            ('json',
             'DEBUG',
             u"{u'function': u'eppy.tests.test_eppylog.decorated_debug_function', u'returns': [14], u'args': (2, 4), u'log_level': u'DEBUG', u'kwargs': {'c': 6}}"),
            ('file',
             'DEBUG',
             u"function: eppy.tests.test_eppylog.decorated_debug_function, args: (2, 4), kwargs: {'c': 6}, returns: [14]"))

    def test_logobjects(self):
        """test logging of objects works as expected, with decorated overridden
        class methods being logged, and the __repr__ value being used in the
        logs rather than a reference
        """
        class DummyObject(object):

            """Test object to be logged.
            """

            def __repr__(self):
                return 'dummy object'

            @eppylog.LogLevel('debug')
            def __getattr__(self, *args, **kwargs):
                return "I'm an attribute"

        with LogCapture() as log_cap:
            # create an object
            obj = DummyObject()
            # access an attribute
            obj.x

        log_cap.check(
            ('console',
             'DEBUG',
             u"function: eppy.tests.test_eppylog.__getattr__, args: (dummy object, 'x'), kwargs: {}, returns: [I'm an attribute]"),
            ('json',
             'DEBUG',
             u'{u\'function\': u\'eppy.tests.test_eppylog.__getattr__\', u\'returns\': [u"I\'m an attribute"], u\'args\': (dummy object, \'x\'), u\'log_level\': u\'DEBUG\', u\'kwargs\': {}}'),
            ('file',
             'DEBUG',
             u"function: eppy.tests.test_eppylog.__getattr__, args: (dummy object, 'x'), kwargs: {}, returns: [I'm an attribute]"))


def test_setloggerlevel():
    """check that setting the log level for a given logger works.
    """
    # get current handler level
    current_level = eppylog.getloggerlevel('json')
    eppylog.setloggerlevel('json', 'INFO')
    new_level = eppylog.getloggerlevel('json')
    eppylog.setloggerlevel('json', current_level)
    assert new_level == 'INFO'


def test_jsonlog():
    """check that each JSON log entry is valid JSON
    """
    with open('eppy.json', 'r') as json_log:
        # if all load then they are valid JSON
        _logs = [json.loads(record) for record in json_log.readlines()]
