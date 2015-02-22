# Copyright (c) 2012 Tuan Tran

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

## {{{ http://code.activestate.com/recipes/578276/ (r1)
## modified by Tuan Tran trantuan@hawaii.edu at L+U, www.coolshadow.com
"""height and surface"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np

# area of a polygon
def area(poly):
    """area"""
    if len(poly) < 3: # not a plane - no area
        return 0
    total = [0, 0, 0]
    num = len(poly)
    for i in range(num):
        vi1 = poly[i]
        vi2 = poly[(i+1) % num]
        prod = np.cross(vi1, vi2)
        total[0] += prod[0]
        total[1] += prod[1]
        total[2] += prod[2]
    result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result/2)

# average height of a polygon
def height(poly):
    """height"""
    num = len(poly)
    hgt = 0.0
    for i in range(num):
        hgt += (poly[i][2])
    return hgt/num

#unit normal vector of plane defined by points a, b, and c
def unit_normal(apnt, bpnt, cpnt):
    """unit normal"""
    xvar = np.linalg.det([
        [1, apnt[1], apnt[2]], [1, bpnt[1], bpnt[2]], [1, cpnt[1], cpnt[2]]])
    yvar = np.linalg.det([
        [apnt[0], 1, apnt[2]], [bpnt[0], 1, bpnt[2]], [cpnt[0], 1, cpnt[2]]])
    zvar = np.linalg.det([
        [apnt[0], apnt[1], 1], [bpnt[0], bpnt[1], 1], [cpnt[0], cpnt[1], 1]])
    magnitude = (xvar**2 + yvar**2 + zvar**2)**.5
    if magnitude < 0.00000001:
        mag = (0, 0, 0)
    else: mag = (xvar/magnitude, yvar/magnitude, zvar/magnitude)
    return mag
## end of http://code.activestate.com/recipes/578276/ }}}

