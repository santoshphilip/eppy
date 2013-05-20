# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

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

