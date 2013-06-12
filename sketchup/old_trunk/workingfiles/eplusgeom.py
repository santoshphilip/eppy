# Copyright (c) 2012 Santosh Philip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

#!/usr/bin/env python
"""
Functions to generate energyplus geometry
"""

try:
    set
except NameError:
    from sets import Set as set
from textwrap import dedent
import geometry
import flatten

def getlayers(dct):
    """get the list of layers"""
    layerlist = []
    for value in dct.values():
        layerlist.append(value['layer'])
    lst = list(set(layerlist))
    lst.sort()
    return lst

def surfacetype(ang):
    """given the angle that the surface makes with the horizontal, return the surface type"""
    if ang < 45:
        return 'ROOF'
    if ang > 135:
        return 'FLOOR'
    return 'WALL'
    
def makezones(dct):
    """make all the zones in energyplus
    it puts
    - wall name
    - Ceiling height
    - Volume
    =======
    Things not yet done:
    - throw exception if there is no floor
    """
    snippet1 = """ZONE,
"""
    snippet2 = """    0,                       !- Relative North (to building) {deg}
    0,                       !- X Origin {m}
    0,                       !- Y Origin {m}
    0,                       !- Z Origin {m}
    1,                       !- Type
    1,                       !- Multiplier
"""
    layerlist = getlayers(dct)
    txt = """!-   ===========  ALL OBJECTS IN CLASS: ZONE ===========

"""
    for layer in layerlist:
        layerline = '    %s,\n' % (layer, ) 
        minb, maxb = zonebounds(dct, layer)
        ceilingheight = maxb[2] - minb[2]
        ceilingheightline = '    %s,\n' % (ceilingheight)
        volume = zonearea(dct, layer) * ceilingheight
        volumeline = '    %s;\n' % (volume, )
        txt += snippet1 + layerline + snippet2 + ceilingheightline + volumeline
    return txt
    
def makewalls(dct):
    """make all walls
    it puts:
    - wall name
    - Surface Type
    - construction material
    - InsideFaceEnvironment
    - num vertices
    - points (counterclockwise)
    - interior walls
    =============
    not yet done:
    - comments with right formatting
    - top left corrner stuff
    """
    snippet1 = """Surface:HeatTransfer,
"""
    snippet2 = """    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.50000,                 !- View Factor to Ground
"""
    dct = marksameface(dct) # mark interior walls
    keylist = dct.keys()
    keylist.sort()
    txt = """!-   ===========  ALL OBJECTS IN CLASS: SURFACE:HEATTRANSFER ===========

"""
    for wallname in keylist:
        if dct[wallname]['parent'] == None:
            wallnameline = '    %s,\n' % (wallname, ) 
            surfacetypeline = '    %s,\n' % (surfacetype(dct[wallname]['surfacedirection']), )
            materialnameline = '    %s,\n' % (dct[wallname]['material'], )
            InsideFaceEnvrionmentline = '    %s,\n' % (dct[wallname]['layer'], )
            if dct[wallname]['nextto']:
                outsidefaceenvironmentline = '    %s,\n' % (dct[wallname]['nextto'], )
            else:
                outsidefaceenvironmentline = '    %s,\n' % ('ExteriorEnvironment', )
            points = dct[wallname]['points']
            vertexline = '    %s,\n' % (len(points), )
            coordlst = []
            for pts3 in points:
                for pt in pts3:
                    coordline = '    %s,' % (pt, )
                    coordlst.append(coordline)
            coordlst[-1] = coordlst[-1][:-1] + ';'
            coordsnippet = '\n'.join(coordlst)
            txt +=  snippet1 + \
                    wallnameline + \
                    surfacetypeline + \
                    materialnameline + \
                    InsideFaceEnvrionmentline + \
                    outsidefaceenvironmentline + \
                    snippet2 + \
                    vertexline + \
                    coordsnippet + \
                    '\n'
    return txt
    
def makewindows(dct):
    """make all windows
    it puts:
    - window name
    - base surface name
    - material
    - number of vertices
    - points
    =========
    Not yet done
    - check on window rotation direction
    """
    snippet1 = """Surface:HeatTransfer:Sub,
"""
    snippet2 = """    WINDOW,                  !- Surface Type
"""
    snippet3 = """    ,                        !- OutsideFaceEnvironment Object
    0.50000,                 !- View Factor to Ground
    ,                        !- Name of shading control
    ,                        !- WindowFrameAndDivider Name
    1,                       !- Multiplier
"""
    keylist = dct.keys()
    keylist.sort()
    txt = """!-   ===========  ALL OBJECTS IN CLASS: SURFACE:HEATTRANSFER:SUB ===========

"""
    for wallname in keylist:
        if dct[wallname]['parent'] != None:
            windowname = wallname
            windownamestring = '    %s,\n' % (windowname, )
            materialnamestring = '    %s,\n' % (dct[windowname]['material'], )
            basesurfacenamestring = '    %s,\n' % (dct[windowname]['parent'], )
            points = dct[windowname]['points']
            vertexline = '    %s,\n' % (len(points), )
            coordlst = []
            for pts3 in points:
                for pt in pts3:
                    coordline = '    %s,' % (pt, )
                    coordlst.append(coordline)
            coordlst[-1] = coordlst[-1][:-1] + ';'
            coordsnippet = '\n'.join(coordlst)
            txt += snippet1 + \
                   windownamestring + \
                   snippet2 + \
                   materialnamestring + \
                   basesurfacenamestring + \
                   snippet3 +\
                   vertexline + \
                   coordsnippet +\
                   '\n'
    return txt    
        
def zonearea(dct, zone):
    """return the area of the zone
    this is the sum of all areas of faces that have 'surfacedirection'=180"""
    facelist = dct.keys()
    zonefacelist = [face for face in facelist if dct[face]['layer'] == zone]
    zonefloorlist = [face for face in zonefacelist \
                        if dct[face]['surfacedirection'] == 180]
    areas = [geometry.polygonarea3d(dct[floor]['points']) for floor in zonefloorlist]
    return sum(areas)

def zonebounds(dct, zone):
    """return the bounding rectangle of the zone
    bounding rectangle = [p1,p2] and p = [x, y, z]"""
    facelist = dct.keys()
    zonefacelist = [face for face in facelist if dct[face]['layer'] == zone]
    zonefaces = [dct[face]['points'] for face in zonefacelist]
    points = []
    for zoneface in zonefaces:
        for pt in zoneface:
            points.append(pt)
    allx = [x for x, y, z in points]
    ally = [y for x, y, z in points]
    allz = [z for x, y, z in points]
    bmin = [min(val) for val in [allx, ally, allz]]
    bmax = [max(val) for val in [allx, ally, allz]]
    return tuple(bmin), tuple(bmax)

def sameface(face1, face2):
    """return True if the 2 faces are made up of identical points
    where: face = (p1,p2,p3,p4) and p = (x,y,z)"""
    face1 = [tuple(pt) for pt in face1]
    face2 = [tuple(pt) for pt in face2]
    return set(face1) == set(face2)

def marksameface(dct):
    """update dct to indicate all faces that have a face next to it"""
    faces = dct.keys()
    faces.sort()
    for face in faces:
        dct[face]['nextto'] = None
    for f1 in faces:
        for f2 in faces:
            if f1 != f2:
                if sameface(dct[f1]['points'], dct[f2]['points']):
                    dct[f1]['nextto'] = f2
    return dct

def main():
    pass


if __name__ == '__main__':
    main()

