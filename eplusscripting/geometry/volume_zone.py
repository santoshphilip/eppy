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

""""This module is used for calculation of zone volume for E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

# Find the intersection between two lines
# V = (1/6)*|(a-d).((b-d)x(c-d))| http://en.wikipedia.org/wiki/Tetrahedron

import numpy as np

def vol_tehrahedron(poly):
    """volume of a irregular tetrahedron"""
    a = np.array(poly[0])
    b = np.array(poly[1])
    c = np.array(poly[2])
    d = np.array(poly[3])
    return abs(np.dot((a-d), np.cross((b-d),(c-d))) / 6)

def central_p(poly1,poly2):
    central_point = np.array([0.0, 0.0, 0.0])
    for i in range(len(poly1)):
        central_point += np.array(poly1[i]) + np.array(poly2[i])
    return central_point/ (len(poly1)) / 2

def vol(poly1,poly2):
    """"volume of a zone defined by two polygon bases """
    c_point = central_p(poly1, poly2)
    c_point = (c_point[0], c_point[1], c_point[2])
    vol_therah = 0
    N = len(poly1)
    poly1.append(poly1[0])
    poly2.append(poly2[0])
    for i in range(N-2):
        # the upper part
        tehrahedron = [c_point,poly1[0], poly1[i+1], poly1[i+2]]
        vol_therah += vol_tehrahedron(tehrahedron)
        # the bottom part
        tehrahedron = [c_point,poly2[0], poly2[i+1], poly2[i+2]]
        vol_therah += vol_tehrahedron(tehrahedron)
    # the middle part
    for i in range(N):
        tehrahedron = [c_point, poly1[i], poly2[i], poly2[i+1]]
        vol_therah += vol_tehrahedron(tehrahedron)
        tehrahedron = [c_point, poly1[i], poly1[i+1], poly2[i]]
        vol_therah += vol_tehrahedron(tehrahedron)
    return vol_therah