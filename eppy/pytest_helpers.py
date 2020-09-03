# Copyright (c) 2011 Santosh Philip
# Copyright (c) 2015 Jamie Bull

"""helpers for pytest"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PATH_TO_EPPY = os.path.join(THIS_DIR)

INTEGRATION_TESTS = os.path.join(PATH_TO_EPPY, os.pardir, "tests", "integration")
INTEGRATION_FILES = os.path.join(INTEGRATION_TESTS, "data2test")

RESOURCES_DIR = os.path.join(PATH_TO_EPPY, "resources")
IDD_FILES = os.path.join(RESOURCES_DIR, "iddfiles")
IDF_FILES = os.path.join(RESOURCES_DIR, "idffiles")


def do_integration_tests():
    """
    Check whether the 'EPPY_INTEGRATION' environment variable has been set to do
    integration tests.

    Returns
    -------
    bool

    """
    return os.getenv("EPPY_INTEGRATION", False)


def almostequal(first, second, places=7, printit=True):
    """docstring for almostequal
    # taken from python's unit test
    # may be covered by Python's license

    """
    if round(abs(second - first), places) != 0:
        if printit:
            print(round(abs(second - first), places))
            print("notalmost: %s != %s" % (first, second))
        return False
    else:
        return True
