# Copyright (c) 2012 Santosh Philip

"""helpers for pytest"""

# taken from python's unit test
# may be covered by Python's license

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
