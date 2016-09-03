# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""pytest for volume_zone.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

from eppy.geometry.volume_zone import central_p
from eppy.geometry.volume_zone import vol_tehrahedron
from eppy.geometry.volume_zone import vol
from eppy.pytest_helpers import almostequal


def test_volume():
    """py.test for volume"""
    data = (
        (
            [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
            [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
            , 1
        ), # poly1, poly2, answer
        (
            [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)],
            [(0, 0, 0), (1, 0, 0), (1, 1, 2), (0, 1, 2)]
            , 1
        ), # poly1, poly2, answer
        )
    for poly1, poly2, answer in data:
        result = vol(poly1, poly2)
        assert almostequal(answer, result, places=4) == True
        

def test_vol_tetrahedron():
    poly1 = [(0.0625,0.0625,0.0625), (0,0,0), (0,1,0), (1,1,0), (1,0,0)]
    assert vol_tehrahedron(poly1) == 0.0625 / 6


def test_vol_zone():
    poly1 = [(0,0,0), (0,1,0), (1,1,0), (1,0,0)]
    poly2 = [(0,0,1), (0,1,1), (1,1,1), (1,0,1)]
    assert almostequal(vol(poly1, poly2), 1)

    poly1 = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    poly2 = [(0, 0, 0), (1, 0, 0), (1, 1, 2), (0, 1, 2)]
    assert almostequal(vol(poly1, poly2), 1)


def test_central_p():
    poly1 = [(0,0,0), (0,1,0), (1,1,0), (1,0,0)]
    poly2 = [(0,0,1), (0,1,1), (1,1,1), (1,0,1)]
    c_point = central_p(poly1, poly2)
    c_point = (c_point[0], c_point[1], c_point[2])
    assert c_point == (0.5, 0.5, 0.5)
    
