"""pytest for volume_zone.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

import volume_zone
from pytest_helpers import almostequal


data = (([(0,0,0),(1,0,0),(1,1,0),(0,1,0)],[(0,0,1),(1,0,1),(1,1,1),(0,1,1)],1), # base polygon, top polygon, answer,
        ([(0,0,0),(1,0,0),(1,1,0),(0,1,0)],[(0,0,0),(1,0,0),(1,1,2),(0,1,2)],1),
        )
  
def test_volume():
    for poly1,poly2,answer in data:
        result = volume_zone.vol(poly1,poly2)
        assert almostequal(answer, result, places=4) == True
    