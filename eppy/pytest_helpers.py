# Copyright (c) 2012 Santosh Philip

"""helpers for pytest"""

# taken from python's unit test
# may be covered by Python's license

def almostequal(first, second, places=7):
    """docstring for almostequal"""
    if round(abs(second-first), places) != 0:
        return False
    else:
        return True
