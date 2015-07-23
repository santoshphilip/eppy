# Copyright (c) 2012 Tuan Tran
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""pytest for surface.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

import eppy.geometry.surface as surface
from eppy.pytest_helpers import almostequal

def test_area():
    """test the area of a polygon poly"""
    
    data = (([(0,0,0), (1,0,0), (1,1,0), (0,1,0)],1),# polygon, answer,
             ([(0,0,0), (1,0,0), (1,0,1), (0,0,1)],1),
             ([(0,0,0), (0,1,0), (0,1,1), (0,0,1)],1),
             ([(0,0,0), (0,1,0), (0,2,0), (0,3,0)],0),
             ([(-4.611479, 6.729214, -0.332978),
             (-0.694944, 4.990984, 2.243709),
             (-2.147088,0.302854,1.288344),
             (-6.063622,2.041084,-1.288344)],25),
            )
    for poly,answer in data:
        result = surface.area(poly)
        assert almostequal(answer, result, places=4) == True
        

def test_height():
    """test the height of a polygon poly"""
    
    data = (([(0,0,0), (1,0,0), (1,1,0), (0,1,0)],1),# polygon, answer,
             ([(0,0,0), (8,0,0), (11,0,4), (3,0,4)],5),
             ([(0,0,0), (10,0,0), (10,9,0), (0,9,0)],9),
             ([(3.571913,-9.390334,1.487381), (10.905826,-6.194443,1.487381),                 (8.998819,-1.818255,0.0), (1.664906, -5.014146, 0.0)],5),
             ([(0.0, 0.0, 3.0), (0.0, 0.0, 2.4), (30.5, 0.0, 2.4), (30.5, 0.0, 3.0)], 0.6),
            )
    for poly,answer in data:
        result = surface.height(poly)
        assert almostequal(answer, result, places=5) == True

def test_width():
    """test the width of a polygon poly """
    
    data = (([(0,0,0), (1,0,0), (1,1,0), (0,1,0)],1),# polygon, answer,
             ([(0,0,0), (8,0,0), (11,0,4), (3,0,4)],8),
             ([(0,0,0), (10,0,0), (10,9,0), (0,9,0)],10),
             ([(3.571913,-9.390334,1.487381), (10.905826,-6.194443,1.487381),                 (8.998819,-1.818255,0.0), (1.664906, -5.014146, 0.0)],8),
            )
    for poly,answer in data:
        result = surface.width(poly)
        assert almostequal(answer, result, places=4) == True
        
def test_azimuth():
    """test the azimuth of a polygon poly"""
    data = (([(0,0,0), (1,0,0), (1,1,1), (0,1,1)],180),# polygon, answer,
            ([(0,0,0), (1,0,0), (1,1,0), (0,1,0)],0),
            ([(3.571913,-9.390334,1.487381), (10.905826,-6.194443,1.487381),                 (8.998819,-1.818255,0.0), (1.664906, -5.014146, 0.0)],360 - 23.546134),
            )
    for poly,answer in data:
        result = surface.azimuth(poly)
        assert almostequal(answer, result, places=3) == True
        
def test_tilt():
    """test the tilt of a polygon poly"""
    data = (([(0,0,0), (1,0,0), (1,1,0), (0,1,0)],0),# polygon, answer,
            ([(0,0,0), (5,0,0), (5,0,8), (0,0,8)],90),
            ([(0,0,0), (1,0,0), (1,1,1), (0,1,1)],45),
            ([(3.571913,-9.390334,1.487381), (10.905826,-6.194443,1.487381),                 (8.998819,-1.818255,0.0), (1.664906, -5.014146, 0.0)],90-72.693912),
            )
    for poly,answer in data:
        result = surface.tilt(poly)
        assert almostequal(answer, result, places=3) == True
