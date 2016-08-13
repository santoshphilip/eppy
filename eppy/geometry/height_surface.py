# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

## {{{ http://code.activestate.com/recipes/578276/ (r1)
## modified by Tuan Tran trantuan@hawaii.edu at L+U, www.coolshadow.com
"""height and surface"""
try:
    import numpy as np
    from np.linalg import det
except ImportError as err:
    import tinynumpy.tinynumpy as np
    from np.tinylinalg import det


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

def unit_normal(a, b, c):
    """unit normal vector of plane defined by points a, b, and c"""
    x = det([
        [1, a[1], a[2]], [1, b[1], b[2]], [1, c[1], c[2]]])
    y = det([
        [a[0], 1, a[2]], [b[0], 1, b[2]], [c[0], 1, c[2]]])
    z = det([
        [a[0], a[1], 1], [b[0], b[1], 1], [c[0], c[1], 1]])
    magnitude = (x**2 + y**2 + z**2)**.5

    if magnitude < 0.00000001:
        mag = (0, 0, 0)
    else: mag = (x/magnitude, y/magnitude, z/magnitude)
    
    return mag

def height(poly):
    """average height of a polygon"""
    num = len(poly)
    hgt = 0.0
    for i in range(num):
        hgt += (poly[i][2])
    return hgt/num

def test_area():
    pts = [(0,0,0), (0,1,0), (1,1,0), (1,0,0)]
    assert area(pts) == 1
    assert area(list(reversed(pts))) == 1
    pts = [(0,0,0), (1,1,0), (0,1,0)]
    assert area(pts) == 0.5
    assert area(list(reversed(pts))) == 0.5
    pts = [(0,0,0), (0,1,0)]
    assert area(pts) == 0
    