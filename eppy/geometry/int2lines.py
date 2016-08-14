# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""
Find the intersection between two lines
"""

from sympy import Segment3D
from sympy.geometry.point import Point3D


def intersection(a, b):
    """Find the intersection of two line segments.
    
    Parameters
    ----------
    a : list of tuples
        A line defined by two 3D points, e.g. [(0,1,1), (1,0,0)].
    b : list of tuples
        A second line defined by two 3D points, e.g. [(0,1,1), (1,0,0)].
    
    Returns
    -------
    list
        An empty list if the lines don't intersect, an [(x,y,z)] tuple if they
        intersect at a single point, or a [(x,y,z),(x,y,z)] list representing a
        line segment if they overlap.
    
    """
    l1 = Segment3D(Point3D(a[0]), Point3D(a[1]))
    l2 = Segment3D(Point3D(b[0]), Point3D(b[1]))
    intersect = l1.intersection(l2)
    if intersect:
        if isinstance(intersect[0], Point3D):
            pt = intersect[0].evalf()
            result = [pt_to_tuple(pt)]
        elif isinstance(intersect[0], Segment3D):
            pt1 = intersect[0].p1
            pt2 = intersect[0].p2
            result = [pt_to_tuple(pt1), pt_to_tuple(pt2)]
    else:
        result = []

    return result

def pt_to_tuple(pt):
    """Convert a Point3D to an (x,y,z) tuple.
    
    Parameters
    ----------
    pt : sympy.Point3D
        The point to convert.
    
    Returns
    -------
    tuple

    """
    return (pt.x, pt.y, pt.z)    