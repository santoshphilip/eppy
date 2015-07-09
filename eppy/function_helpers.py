# Copyright (c) 2012 Santosh Philip

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

"""helper functions for the functions called by bunchdt"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
# import geometry
from eppy.geometry import surface as g_surface

def grouper(num, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * num
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def getcoords(ddtt):
    """return the coordinates of the surface"""
    n_vertices_index = ddtt.objls.index('Number_of_Vertices')
    first_x = n_vertices_index + 1 # X of first coordinate
    pts = ddtt.obj[first_x:]
    return list(grouper(3, pts))

def area(ddtt):
    """area of the surface"""
    coords = getcoords(ddtt)
    return g_surface.area(coords)

def height(ddtt):
    """height of the surface"""
    coords = getcoords(ddtt)
    return g_surface.height(coords)

def width(ddtt):
    """width of the surface"""
    coords = getcoords(ddtt)
    return g_surface.width(coords)

def azimuth(ddtt):
    """azimuth of the surface"""
    coords = getcoords(ddtt)
    return g_surface.azimuth(coords)

def tilt(ddtt):
    """tilt of the surface"""
    coords = getcoords(ddtt)
    return g_surface.tilt(coords)

