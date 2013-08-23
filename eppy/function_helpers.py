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
import itertools
import geometry.surface

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)
    
def getcoords(dt):
    """return the coordinates of the surface"""
    n_vertices_index = dt.objls.index('Number_of_Vertices')
    first_x = n_vertices_index + 1 # X of first coordinate
    pts = dt.obj[first_x:]
    return list(grouper(3, pts))

def area(dt):
    """area of the surface"""
    coords = getcoords(dt)
    return geometry.surface.area(coords)
    
def height(dt):
    """height of the surface"""
    coords = getcoords(dt)
    return geometry.surface.height(coords)
    
def width(dt):
    """width of the surface"""
    coords = getcoords(dt)
    return geometry.surface.width(coords)
    
def azimuth(dt):
    """azimuth of the surface"""
    coords = getcoords(dt)
    return geometry.surface.azimuth(coords)
    
def tilt(dt):
    """tilt of the surface"""
    coords = getcoords(dt)
    return geometry.surface.tilt(coords)
    
