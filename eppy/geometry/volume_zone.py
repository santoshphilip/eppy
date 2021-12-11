# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

""""This module is used for calculation of zone volume for E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

# Find the intersection between two lines
# V = (1/6)*|(a-d).((b-d)x(c-d))| http://en.wikipedia.org/wiki/Tetrahedron
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

try:
    import numpy as np
except ImportError as err:
    from tinynumpy import tinynumpy as np


def vol_tehrahedron(poly):
    """volume of a irregular tetrahedron"""
    p_a = np.array(poly[0])
    p_b = np.array(poly[1])
    p_c = np.array(poly[2])
    p_d = np.array(poly[3])
    return abs(
        np.dot(
            np.subtract(p_a, p_d),
            np.cross(np.subtract(p_b, p_d), np.subtract(p_c, p_d)),
        )
        / 6
    )


def central_p(poly1, poly2):
    central_point = np.array([0.0, 0.0, 0.0])
    for i in range(len(poly1)):
        central_point = np.add(
            central_point, np.add(np.array(poly1[i]), np.array(poly2[i]))
        )
    return np.divide(np.divide(central_point, (len(poly1))), 2)


def vol(poly1, poly2):
    """ "volume of a zone defined by two polygon bases"""
    c_point = central_p(poly1, poly2)
    c_point = (c_point[0], c_point[1], c_point[2])
    vol_therah = 0
    num = len(poly1)
    poly1.append(poly1[0])
    poly2.append(poly2[0])
    for i in range(num - 2):
        # the upper part
        tehrahedron = [c_point, poly1[0], poly1[i + 1], poly1[i + 2]]
        vol_therah += vol_tehrahedron(tehrahedron)
        # the bottom part
        tehrahedron = [c_point, poly2[0], poly2[i + 1], poly2[i + 2]]
        vol_therah += vol_tehrahedron(tehrahedron)
    # the middle part
    for i in range(num):
        tehrahedron = [c_point, poly1[i], poly2[i], poly2[i + 1]]
        vol_therah += vol_tehrahedron(tehrahedron)
        tehrahedron = [c_point, poly1[i], poly1[i + 1], poly2[i]]
        vol_therah += vol_tehrahedron(tehrahedron)
    return vol_therah
