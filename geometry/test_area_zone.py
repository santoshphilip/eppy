""" pytest for area_zone.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

import area_zone
from pytest_helpers import almostequal

def test_area():
    """test for area of a zone"""
    
    data = (([(0,0,0), (1,0,1), (1,1,0), (0,1,1)],1),# polygon, answer,
             ([(0,0,0), (1,0,0), (1,0,1), (0,0,1)],0),
             ([(0,0,0), (0,1,0), (0,1,1), (0,0,1)],0),
             ([(0,0,4), (5,0,4), (5,5,6), (0,5,6)],25),
            )
    for poly,answer in data:
        result = area_zone.area(poly)
        assert almostequal(answer, result, places=4) == True