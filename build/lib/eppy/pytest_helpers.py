# Copyright (c) 2012 Santosh Philip

"""helpers for pytest"""

# taken from python's unit test
# may be covered by Python's license

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

def almostequal(first, second, places=7, printit=True):
    """docstring for almostequal"""
    if round(abs(second-first), places) != 0:
        if printit:
            print(round(abs(second-first), places))
            print("notalmost: %s != %s" % (first, second))
        return False
    else:
        return True
