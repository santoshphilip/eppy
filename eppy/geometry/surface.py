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

"""This module is used for assisted calculations on E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

####### The following code within the block credited by ActiveState Code Recipes code.activestate.com
## {{{ http://code.activestate.com/recipes/578276/ (r1)

import numpy as np
import math

def area(poly):
    """Area of a polygon poly""" 
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

#unit normal vector of plane defined by points a, b, and c
def unit_normal(a, b, c):
    x = np.linalg.det([[1,a[1],a[2]],[1,b[1],b[2]],[1,c[1],c[2]]])
    y = np.linalg.det([[a[0],1,a[2]],[b[0],1,b[2]],[c[0],1,c[2]]])
    z = np.linalg.det([[a[0],a[1],1],[b[0],b[1],1],[c[0],c[1],1]])
    magnitude = (x**2 + y**2 + z**2)**.5
    mag = (x/magnitude, y/magnitude, z/magnitude)
    if magnitude < 0.00000001: mag = (0,0,0)
    return mag
## end of http://code.activestate.com/recipes/578276/ }}}

# distance between two points
def dist(p1,p2):
    """Distance between two points"""
    return ((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)**0.5

# width of a rectangular polygon        
def width(poly):
    """Width of a polygon poly"""
    N = len(poly) - 1
    if abs(poly[N][2] - poly[0][2]) < abs(poly[1][2] - poly[0][2]):
        return dist(poly[N],poly[0])
    elif abs(poly[N][2] - poly[0][2]) > abs(poly[1][2] - poly[0][2]):
        return dist(poly[1], poly[0])
    else: return max(dist(poly[N], poly[0]), dist(poly[1], poly[0]))

# height of a polygon poly
def height(poly):
    """Height of a polygon poly"""
    N = len(poly) - 1
    if abs(poly[N][2] - poly[0][2]) > abs(poly[1][2] - poly[0][2]):
        return dist(poly[N],poly[0])
    elif abs(poly[N][2] - poly[0][2]) < abs(poly[1][2] - poly[0][2]):
        return dist(poly[1], poly[0])
    else: 
        return min(dist(poly[N], poly[0]), dist(poly[1], poly[0]))
    
# angle between two vectors
def angle2vecs(vec1,vec2):
    # vector a * vector b = |a|*|b|* cos(angle between vector a and vector b)
    dot = np.dot(vec1,vec2)
    vec1_modulus = np.sqrt((vec1*vec1).sum())
    vec2_modulus = np.sqrt((vec2*vec2).sum())
    if (vec1_modulus * vec2_modulus) == 0:
        cos_angle = 1
    else: cos_angle = dot / (vec1_modulus * vec2_modulus)
    return math.degrees(np.arccos(cos_angle)) 

# orienation of a polygon poly
def azimuth(poly):
    """Azimuth of a polygon poly"""
    N = len(poly) - 1
    vec = unit_normal(poly[0], poly[1], poly[N])
    vec_azi = np.array([vec[0], vec[1], 0])
    vec_N = np.array([0, 1, 0])
    # update by Santosh
    # angle2vecs gives the smallest angle between the vectors
    # so for a west wall angle2vecs will give 90
    # the following 'if' statement will make sure 270 is returned    
    x_vector = vec_azi[0] 
    if x_vector < 0:
        return 360 - angle2vecs(vec_azi, vec_N)
    else:
        return angle2vecs(vec_azi, vec_N)
        
def tilt(poly):
    """Tilt of a polygon poly"""
    N = len(poly) - 1
    vec = unit_normal(poly[0], poly[1], poly[N])
    vec_alt = np.array([vec[0], vec[1], vec[2]])
    vec_z = np.array([0,0,1])
    # return (90 - angle2vecs(vec_alt, vec_z)) # update by Santosh
    return (angle2vecs(vec_alt, vec_z))
    