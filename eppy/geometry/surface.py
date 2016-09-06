# Copyright (c) 2012 Tuan Tran

# This file is part of eppy.
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""This module is used for assisted calculations on E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

# The following code within the block
# credited by ActiveState Code Recipes code.activestate.com
## {{{ http://code.activestate.com/recipes/578276/ (r1)
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import numpy as np
    from numpy import arccos as acos
except ImportError as err:
    from tinynumpy import tinynumpy as np
    from tinynumpy import tinylinalg as linalg
    from math import acos as acos
import math


def area(poly):
    """Area of a polygon poly"""
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
    if total == [0, 0, 0]:  # points are in a straight line - no area
        return 0
    result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result/2)

def unit_normal(pt_a, pt_b, pt_c):
    """unit normal vector of plane defined by points pt_a, pt_b, and pt_c"""
    x_val = np.linalg.det([[1, pt_a[1], pt_a[2]], [1, pt_b[1], pt_b[2]], [1, pt_c[1], pt_c[2]]])
    y_val = np.linalg.det([[pt_a[0], 1, pt_a[2]], [pt_b[0], 1, pt_b[2]], [pt_c[0], 1, pt_c[2]]])
    z_val = np.linalg.det([[pt_a[0], pt_a[1], 1], [pt_b[0], pt_b[1], 1], [pt_c[0], pt_c[1], 1]])
    magnitude = (x_val**2 + y_val**2 + z_val**2)**.5
    mag = (x_val/magnitude, y_val/magnitude, z_val/magnitude)
    if magnitude < 0.00000001:
        mag = (0, 0, 0)
    return mag
## end of http://code.activestate.com/recipes/578276/ }}}

# distance between two points
def dist(pt1, pt2):
    """Distance between two points"""
    return ((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2 + (pt2[2] - pt1[2])**2)**0.5

# width of a rectangular polygon
def width(poly):
    """Width of a polygon poly"""
    num = len(poly) - 1
    if abs(poly[num][2] - poly[0][2]) < abs(poly[1][2] - poly[0][2]):
        return dist(poly[num], poly[0])
    elif abs(poly[num][2] - poly[0][2]) > abs(poly[1][2] - poly[0][2]):
        return dist(poly[1], poly[0])
    else: return max(dist(poly[num], poly[0]), dist(poly[1], poly[0]))

# height of a polygon poly
def height(poly):
    """Height of a polygon poly"""
    num = len(poly) - 1
    if abs(poly[num][2] - poly[0][2]) > abs(poly[1][2] - poly[0][2]):
        return dist(poly[num], poly[0])
    elif abs(poly[num][2] - poly[0][2]) < abs(poly[1][2] - poly[0][2]):
        return dist(poly[1], poly[0])
    else:
        return min(dist(poly[num], poly[0]), dist(poly[1], poly[0]))


def angle2vecs(vec1, vec2):
    """angle between two vectors"""
    # vector a * vector b = |a|*|b|* cos(angle between vector a and vector b)
    dot = np.dot(vec1, vec2)
    vec1_modulus = np.sqrt(np.multiply(vec1, vec1).sum())
    vec2_modulus = np.sqrt(np.multiply(vec2, vec2).sum())
    if (vec1_modulus * vec2_modulus) == 0:
        cos_angle = 1
    else: cos_angle = dot / (vec1_modulus * vec2_modulus)
    return math.degrees(acos(cos_angle))

# orienation of a polygon poly
def azimuth(poly):
    """Azimuth of a polygon poly"""
    num = len(poly) - 1
    vec = unit_normal(poly[0], poly[1], poly[num])
    vec_azi = np.array([vec[0], vec[1], 0])
    vec_n = np.array([0, 1, 0])
    # update by Santosh
    # angle2vecs gives the smallest angle between the vectors
    # so for a west wall angle2vecs will give 90
    # the following 'if' statement will make sure 270 is returned
    x_vector = vec_azi[0]
    if x_vector < 0:
        return 360 - angle2vecs(vec_azi, vec_n)
    else:
        return angle2vecs(vec_azi, vec_n)

def tilt(poly):
    """Tilt of a polygon poly"""
    num = len(poly) - 1
    vec = unit_normal(poly[0], poly[1], poly[num])
    vec_alt = np.array([vec[0], vec[1], vec[2]])
    vec_z = np.array([0, 0, 1])
    # return (90 - angle2vecs(vec_alt, vec_z)) # update by Santosh
    return angle2vecs(vec_alt, vec_z)
