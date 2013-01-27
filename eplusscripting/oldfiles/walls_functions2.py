"""do just walls in eplusinterface"""

import itertools
from idfreader import idfreader
import geometry.surface

def add2(dt):
    return dt.Name, dt.Construction_Name
    
def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)
    
def getcoords(dt):
    """return the coordinates of the surface"""
    pts = dt.obj[11:]
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
    

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

# add functions
for surface in surfaces:
    surface.__functions = {'plus':add2, 
        'area':area,
        'height':height,
        'width':width,
        'azimuth':azimuth,
        'tilt':tilt,
    } 

wall = surfaces[0]

for surface in surfaces:
    name, construction = surface.plus
    area = surface.area
    height = surface.height
    width = surface.width
    azimuth = surface.azimuth
    tilt = surface.tilt
    print name, area, height, width, azimuth, tilt

# print wall.Name
# print wall.obj[10]
# print wall.obj[11]
# print wall.obj[12]
# print wall.plus
# print wall.__functions
# for surface in surfaces:
#     name, construction = surface.plus
#     n1, c1 = surface.Name, surface.Construction_Name
#     assert name == n1
#     assert construction == c1

# lst = range(12)
# coords = []
# for i in range(len(lst)):
#     i % 3
#     # coord = []
#     # for j in range(3):
#     #     coord.append(lst[i])
#     # coords.append(coord)
#     #     
# two = [(lst[i], i % 3) for i in range(len(pts))]    
# coords = []
# coord = []
# for i, j in two:
#     if j < 2:
#         coord.append(i)
#         continue
#     else:
#         coord.append(i)
#         coords.append(coord)
#         coord = []
    
    