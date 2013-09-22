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

""""This module is used for calculation of zone area for E+ surfaces"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

# import area_surface as surf
import surface 

def area(poly):
    """Calculation of zone area"""
    poly_xy = []
    N = len(poly)
    for i in range(N):
        poly[i] = poly[i][0:2] + (0,)
        poly_xy.append(poly[i])
    return surface.area(poly)