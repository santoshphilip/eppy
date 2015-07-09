# Copyright (c) 2012 Tuan Tran

"""This module is used for assisted calculations on E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

####### The following code within the block credited by ActiveState Code
# Recipes code.activestate.com
## {{{ http://code.activestate.com/recipes/578276/ (r1)







import numpy as np
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
    result = np.dot(total, unit_normal(poly[0], poly[1], poly[2]))
    return abs(result/2)

#unit normal vector of plane defined by points a, b, and c
def unit_normal(a_pnt, b_pnt, c_pnt):
    """unit normal"""
    x_val = np.linalg.det(
        [[1, a_pnt[1], a_pnt[2]], [1, b_pnt[1], b_pnt[2]], [1, c_pnt[1],
                                                            c_pnt[2]]])
    y_val = np.linalg.det(
        [[a_pnt[0], 1, a_pnt[2]], [b_pnt[0], 1, b_pnt[2]], [c_pnt[0], 1,
                                                            c_pnt[2]]])
    z_val = np.linalg.det(
        [[a_pnt[0], a_pnt[1], 1], [b_pnt[0], b_pnt[1], 1], [c_pnt[0],
                                                            c_pnt[1], 1]])
    magnitude = (x_val**2 + y_val**2 + z_val**2)**.5
    mag = (x_val/magnitude, y_val/magnitude, z_val/magnitude)
    if magnitude < 0.00000001:
        mag = (0, 0, 0)
    return mag
## end of http://code.activestate.com/recipes/578276/ }}}

# distance between two points
def dist(pnt1, pnt2):
    """Distance between two points"""
    return ((pnt2[0] - pnt1[0])**2 + (pnt2[1] - pnt1[1])**2 + (pnt2[2] - pnt1[2])**2)**0.5

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

# angle between two vectors
def angle2vecs(vec1, vec2):
    """angle between two vectors"""
    # vector a * vector b = |a|*|b|* cos(angle between vector a and vector b)
    dot = np.dot(vec1, vec2)
    vec1_modulus = np.sqrt((vec1*vec1).sum())
    vec2_modulus = np.sqrt((vec2*vec2).sum())
    if (vec1_modulus * vec2_modulus) == 0:
        cos_angle = 1
    else: cos_angle = dot / (vec1_modulus * vec2_modulus)
    return math.degrees(np.arccos(cos_angle))

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
    