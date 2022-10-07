# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

## {{{ http://code.activestate.com/recipes/578276/ (r1)
## modified by Tuan Tran trantuan@hawaii.edu at L+U, www.coolshadow.com
"""height and surface"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import numpy as np
except ImportError as err:
    import tinynumpy as np


# area of a polygon
def area(poly):
    """area"""
    if len(poly) < 3:  # not a plane - no area
        return 0
    total = [0, 0, 0]
    num = len(poly)
    for i in range(num):
        vi1 = poly[i]
        vi2 = poly[(i + 1) % num]
        prod = np.cross(vi1, vi2)
        total[0] += prod[0]
        total[1] += prod[1]
        total[2] += prod[2]
    result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result / 2)


# average height of a polygon
def height(poly):
    """height"""
    num = len(poly)
    hgt = 0.0
    for i in range(num):
        hgt += poly[i][2]
    return hgt / num


# unit normal vector of plane defined by points a, b, and c
def unit_normal(apnt, bpnt, cpnt):
    """unit normal"""
    xvar = np.tinylinalg.det(
        [[1, apnt[1], apnt[2]], [1, bpnt[1], bpnt[2]], [1, cpnt[1], cpnt[2]]]
    )
    yvar = np.tinylinalg.det(
        [[apnt[0], 1, apnt[2]], [bpnt[0], 1, bpnt[2]], [cpnt[0], 1, cpnt[2]]]
    )
    zvar = np.tinylinalg.det(
        [[apnt[0], apnt[1], 1], [bpnt[0], bpnt[1], 1], [cpnt[0], cpnt[1], 1]]
    )
    magnitude = (xvar**2 + yvar**2 + zvar**2) ** 0.5
    if magnitude < 0.00000001:
        mag = (0, 0, 0)
    else:
        mag = (xvar / magnitude, yvar / magnitude, zvar / magnitude)
    return mag


## end of http://code.activestate.com/recipes/578276/ }}}
