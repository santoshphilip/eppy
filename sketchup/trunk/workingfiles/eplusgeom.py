#!/usr/local/bin/python

## EPlusInterface (EPI) - An interface for EnergyPlus
## Copyright (C) 2004 Santosh Philip
##
## This file is part of EPlusInterface.
## 
## EPlusInterface is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## EPlusInterface is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with EPlusInterface; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
##
##
## Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
## santosh_philip AT yahoo DOT com
## Please send all bug reports, enhancement proposals, questions and comments to that address.
## 
## VERSION: 0.005

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
        layerline = makeline(layer, '!- Zone Name')
        minb, maxb = zonebounds(dct, layer)
        ceilingheight = maxb[2] - minb[2]
        ceilingheightline = makeline(ceilingheight, '!- Ceiling Height {m}')
        volume = zonearea(dct, layer) * ceilingheight
        volumeline = '    %s;\n' % (volume, )
        volumeline = makeline(volume, '!- Volume {m3}', comma=';')
        txt += snippet1 + layerline + snippet2 + ceilingheightline + volumeline + '\n'
    return txt
    
def makewalls(dct):
    """make all walls
    it puts:
    - wall name
    - Surface Type
    - construction material
    - InsideFaceEnvironment
    - num vertices
    - points (counterclockwise - same as sketchup)
    - interior walls
        - NoSun, NoWind
    - Floor
        - NoSun, NoWind
        - veiwfactor to ground = 0
    - Roof
        - viewfactor to ground = 0
    - comments with right formatting
    =============
    not yet done:
    - refacator the code - it's too long .. make a class that genereates the lines ?
    - top left corrner stuff
    - view factor to ground can be calculated correctly using pleijel diagrams
        - toggle this due to high calculation time
    """
    snippet1 = """Surface:HeatTransfer,
"""
    dct = marksameface(dct) # mark interior walls
    keylist = dct.keys()
    keylist.sort()
    txt = """!-   ===========  ALL OBJECTS IN CLASS: SURFACE:HEATTRANSFER ===========

"""
    for wallname in keylist:
        if dct[wallname]['parent'] == None:
            wallnameline = makeline(wallname, '!- User Supplied Surface Name') 
            surftype = surfacetype(dct[wallname]['surfacedirection'])
            surfacetypeline = makeline(surftype, '!- Surface Type')
            materialnameline = makeline(dct[wallname]['material'], '!- Construction Name of the Surface')
            InsideFaceEnvrionmentline = makeline(dct[wallname]['layer'], '!- InsideFaceEnvironment')
            if dct[wallname]['nextto']:
                outsidefaceenvironmentline = makeline(dct[wallname]['nextto'], '!- OutsideFaceEnvironment')
                outsidefaceenvobjectline = makeline('OtherZoneSurface', '!- OutsideFaceEnvironment Object')
                sunexpline = makeline('NoSun', '!- Sun Exposure')
                windwxpline = makeline('NoWind', '!- Wind Exposure')
            else:
                outsidefaceenvironmentline = makeline('ExteriorEnvironment', '!- OutsideFaceEnvironment')
                outsidefaceenvobjectline = makeline('', '!- OutsideFaceEnvironment Object')
                sunexpline = makeline('SunExposed', '!- Sun Exposure')
                windwxpline = makeline('WindExposed', '!- Wind Exposure')
            if surftype in ['ROOF', 'FLOOR']:
                viewfactorline = makeline('0.0', '!- View Factor to Ground')
            else:
                viewfactorline = makeline('0.5', '!- View Factor to Ground')
            points                         = dct[wallname]['points']
            vertexline                     = makeline(len(points), '!- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface')
            coordlst                       = []
            numpoints                      = len(points)
            for i, pts3 in enumerate(points):
                for j, pt in enumerate(pts3):
                    xyz = dict(((0, 'X'), (1, 'Y'), (2, 'Z')))
                    comment = '!- Vertex %s %s-coordinate {m}' % (i + 1, xyz[j])
                    if (i == numpoints - 1) and (j == 2):
                        comma = ';'
                    else:
                        comma = ','
                    coordline = makeline(pt, comment, comma=comma)
                    coordlst.append(coordline)
            coordsnippet = ''.join(coordlst)
            txt +=  snippet1 + \
                    wallnameline + \
                    surfacetypeline + \
                    materialnameline + \
                    InsideFaceEnvrionmentline + \
                    outsidefaceenvironmentline + \
                    outsidefaceenvobjectline + \
                    sunexpline + \
                    windwxpline + \
                    viewfactorline + \
                    vertexline + \
                    coordsnippet + '\n'
    return txt
    
def makewindows(dct):
    """make all windows
    it puts:
    - window name
    - base surface name
    - material
    - number of vertices
    - points
    - checked on window rotation direction
    =========
    Not yet done
    - view factor to ground
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
            windownamestring = makeline(windowname, '!- User Supplied Surface Name')
            materialnamestring = makeline(dct[windowname]['material'], '!- Construction Name of the Surface')
            basesurfacenamestring = makeline(dct[windowname]['parent'], '!- Base Surface Name')
            points = dct[windowname]['points']
            vertexline = makeline(len(points), '!- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface')
            coordlst = []
            numpoints = len(points)
            for i, pts3 in enumerate(points):
                for j, pt in enumerate(pts3):
                    xyz = dict(((0, 'X'), (1, 'Y'), (2, 'Z')))
                    comment = '!- Vertex %s %s-coordinate {m}' % (i + 1, xyz[j])
                    if (i == numpoints - 1) and (j == 2):
                        comma = ';'
                    else:
                        comma = ','
                    coordline = makeline(pt, comment, comma=comma)
                    coordlst.append(coordline)
            coordsnippet = ''.join(coordlst)
            txt += snippet1 + \
                   windownamestring + \
                   snippet2 + \
                   materialnamestring + \
                   basesurfacenamestring + \
                   snippet3 +\
                   vertexline + \
                   coordsnippet + '\n'
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

def makeline(data, comment, tabsize=4, datasize=25, comma=','):
    """make a formatted line for the energyplus file"""
    datacomma = '%s%s' % (data, comma)
    tab = ' ' * tabsize
    return '%s%s%s\n' % (tab, datacomma.ljust(datasize), comment)    

def main():
    pass


if __name__ == '__main__':
    main()

