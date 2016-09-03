# Copyright (c) 2012 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""helpers for pytest"""

import os


def almostequal(first, second, places=7):
    """docstring for almostequal"""
    # convert to float first
    try:
        first = float(first)
        second = float(second)
    except ValueError:
        # handle non-float types
        return str(first) == str(second)
    # test floats for near-equality
    if round(abs(second-first), places) != 0:
        return False
    else:
        return True


def do_integration_tests():
    """
    Check whether the 'EPPY_INTEGRATION' environment variable has been set to do
    integration tests.
    
    Returns
    -------
    bool
    
    """
    return os.getenv('EPPY_INTEGRATION', False)
