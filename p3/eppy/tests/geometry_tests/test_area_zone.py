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

""" pytest for area_zone.py"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

import eppy.geometry.area_zone as area_zone
from eppy.pytest_helpers import almostequal

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