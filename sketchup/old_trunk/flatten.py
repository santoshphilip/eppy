#!/usr/bin/env python
# encoding: utf-8
"""
flatten from the python cookbook
"""

import sys
import os

def list_or_tuple(x):
    """test if it is a list or tuple"""
    return isinstance(x, (list, tuple))

def flatten(sequence, to_expand=list_or_tuple):
    """flatten a list
    from python cookbook ed3 page 158"""
    for item in sequence:
        if to_expand(item):
            for subitem in flatten(item, to_expand):
                yield subitem
        else:
            yield item
            
def test_flatten():
    """py.test for flatten()"""
    flattenthis = [1, 2, [3, [], 4, [5, 6, ], 7, [8, ], 9]]
    flattened = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert flattened == [x for x in flatten(flattenthis)]

def main():
    pass


if __name__ == '__main__':
    main()

