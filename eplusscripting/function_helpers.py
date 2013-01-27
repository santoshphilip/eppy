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
    
