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

import numpy as np

# area of a polygon
def area(poly):
    if len(poly) < 3: # not a plane - no area
        return 0
    total = [0, 0, 0]
    N = len(poly)
    for i in range(N):
        vi1 = poly[i]
        vi2 = poly[(i+1) % N]
        prod = np.cross(vi1, vi2)
        total[0] += prod[0]
        total[1] += prod[1]
        total[2] += prod[2]
    result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result/2)

# average height of a polygon
def height(poly):
    N = len(poly)
    h = 0.0
    for i in range(N):
        h += (poly[i][2])
    return h/N
        
#unit normal vector of plane defined by points a, b, and c
def unit_normal(a, b, c):
    x = np.linalg.det([[1,a[1],a[2]],[1,b[1],b[2]],[1,c[1],c[2]]])
    y = np.linalg.det([[a[0],1,a[2]],[b[0],1,b[2]],[c[0],1,c[2]]])
    z = np.linalg.det([[a[0],a[1],1],[b[0],b[1],1],[c[0],c[1],1]])
    magnitude = (x**2 + y**2 + z**2)**.5
    if magnitude < 0.00000001: mag = (0,0,0)
    else: mag = (x/magnitude, y/magnitude, z/magnitude)
    return mag
## end of http://code.activestate.com/recipes/578276/ }}}

