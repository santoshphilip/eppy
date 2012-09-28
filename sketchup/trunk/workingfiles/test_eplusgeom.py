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

"""py.test routines for eplusgeom.py"""

import eplusgeom
from pydottest import almostequals
from flatten import flatten

def test_makezone():
    """py.test for makezones()"""
    data = Zone_Data
    result = eplusgeom.makezones(Zone_Data.dct)
    eplustxt = Zone_Data.eplustxt
    # for resultline, eplusline in zip(result.splitlines(), eplustxt.splitlines()):
    #     assert resultline == eplusline
    assert eplusgeom.makezones(Zone_Data.dct) == Zone_Data.eplustxt
    
def test_getlayers():
    """py.test for getlayers()"""
    data = Zone_Data
    assert eplusgeom.getlayers(Zone_Data.dct) == Zone_Data.layers

def test_makewalls():
    """py.test for makewalls()"""
    data = AllWalls_Data
    result = eplusgeom.makewalls(AllWalls_Data.dct)
    eplustxt =  AllWalls_Data.eplustxt
    # assert len(result.splitlines()) == len(eplustxt.splitlines())
    for resultline, eplusline in zip(result.splitlines(), eplustxt.splitlines()):
        print resultline
        print eplusline
        assert resultline == eplusline
    # assert eplusgeom.makewalls(AllWalls_Data.dct) == AllWalls_Data.eplustxt
    
def test_makewindows():
    """py.test for makewindows"""
    data = Window_Data
    result = eplusgeom.makewindows(data.dct1)
    eplustxt = data.eplustxt1
    # for resultline, eplusline in zip(result.splitlines(), eplustxt.splitlines()):
    #     print resultline
    #     print eplusline
    #     assert resultline == eplusline
    assert result == eplustxt    
    result = eplusgeom.makewindows(data.dct2)
    eplustxt = data.eplustxt2
    # for resultline, eplusline in zip(result.splitlines(), eplustxt.splitlines()):
    #     print resultline
    #     print eplusline
    #     assert resultline == eplusline
    assert result == eplustxt    

def test_surfacetype():
    """py.test for surfacetype()"""
    data = (
        (0, 44, 50, 90, 100, 136, 180),
        ('ROOF', 'ROOF', 'WALL', 'WALL', 'WALL', 'FLOOR', 'FLOOR')
    )
    angles, types = data
    for ang, typ in zip(angles, types):
        assert eplusgeom.surfacetype(ang) == typ

def test_zonearea():
    """pyltest for zonearea()"""
    dct, area, zone = ZoneArea_Data.dct, ZoneArea_Data.area, ZoneArea_Data.zone
    result =  eplusgeom.zonearea(dct, zone)
    assert almostequals(result, area)
    
def test_zonebounds():
    """py.test for zonebounds"""
    data = ZoneBounds_Data
    dct, bounds = data.dct1, data.bounds1
    result = eplusgeom.zonebounds(dct, 'first')
    fresult, fbounds = flatten(result), flatten(bounds)
    for v1, v2 in zip(fresult, fbounds):
        assert almostequals(v1, v2, err=5)
    dct, bounds = data.dct2, data.bounds2
    result = eplusgeom.zonebounds(dct, 'first')
    fresult, fbounds = flatten(result), flatten(bounds)
    for v1, v2 in zip(fresult, fbounds):
        assert almostequals(v1, v2, err=5)

def test_sameface():
    """py.test for sameface()"""
    face1 = [[1,2,3], [3,4,5], [0,9,8]]
    face2 = [[0,9,8], [1,2,3], [3,4,5]]
    face3 = [[0,9,8], [1,2,3], [3,4,5.0]]
    face4 = [[0,9,8], [1,2,3], [3,4,2]]
    face5 = [[1,2,3], [3,4,5], [0,9,8], [5,6,0]]
    assert eplusgeom.sameface(face1, face2)
    assert eplusgeom.sameface(face1, face3)
    assert not eplusgeom.sameface(face1, face4)
    assert not eplusgeom.sameface(face1, face5)
    face1 = [[80.206243138786505, 61.7973218607668, -4.04550012885757e-15],
    [80.206243138786505, 110.297321860767, -4.04550012885757e-15],
    [80.206243138786505, 110.297321860767, 28.25],
    [80.206243138786505, 61.7973218607668, 28.25]]
    face2 =  [[80.206243138786505, 110.297321860767, -4.04550012885757e-15],
    [80.206243138786505, 61.7973218607668, -4.04550012885757e-15],
    [80.206243138786505, 61.7973218607668, 28.25],
    [80.206243138786505, 110.297321860767, 28.25]] # from Sketchup
    assert eplusgeom.sameface(face1, face2)
    face1 = [[-56.667213637101902, 173.09022834891701, -1.3757642575183699e-14],
    [-56.667213637101902, 372.34022834891698, -1.3757642575183699e-14],
    [-56.667213637101902, 372.34022834891698, 72.75],
    [-56.667213637101902, 173.09022834891701, 72.75]]
    face2 =  [[-56.667213637101902, 372.34022834891698, -1.3757642575183699e-14],
    [-56.667213637101902, 173.09022834891701, -1.3757642575183699e-14],
    [-56.667213637101902, 173.09022834891701, 72.75],
    [-56.667213637101902, 372.34022834891698, 72.75]] # from Sketchup
    assert eplusgeom.sameface(face1, face2)

def test_marksameface():
    """test.py for marksameface()"""
    dct, markeddct = MarkSameFace_Data.dct, MarkSameFace_Data.markeddct
    result = eplusgeom.marksameface(dct)
    resultfaces = result.keys()
    #--
    # markeddctfaces = markeddct.keys()
    # resultfaces.sort()
    # markeddctfaces.sort()
    # assert resultfaces == markeddctfaces
    # for face in resultfaces:
    #     print face
    #     print result[face]
    #     print markeddct[face]
    #     assert result[face] == markeddct[face]
    assert result == markeddct

def test_makeline():
    """py.test for makeline()"""
    data = 56.3
    comment = '!- this is a comment'
    commaline = '    56.3,                    !- this is a comment\n'
    result = eplusgeom.makeline(data, comment)
    assert result == commaline
    scolon = ';'
    scolonline = '    56.3;                    !- this is a comment\n'
    result = eplusgeom.makeline(data, comment, comma=scolon)
    assert result == scolonline
    
    
class Zone_Data(object):
    dct = {'1': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[-54.814574283752997,
                       450.80705971907798,
                       5.7705587212691398e-15],
                      [-54.814574283752997,
                       210.80705971907801,
                       5.7705587212691398e-15],
                      [-174.81457428375299,
                       210.80705971907801,
                       5.7705587212691398e-15],
                      [-174.81457428375299,
                       450.80705971907798,
                       5.7705587212691398e-15]],
           'surfacedirection': 180.0},
     '10': {'layer': 'second',
            'material': None,
            'normal': [1.0, 0.0, 0.0],
            'parent': None,
            'points': [[317.39986437368401,
                        -31.935616071834801,
                        -5.1202222995549502e-17],
                       [317.39986437368401,
                        172.064383928165,
                        -5.1202222995549502e-17],
                       [317.39986437368401, 172.064383928165, 36.0],
                       [317.39986437368401, -31.935616071834801, 36.0]],
            'surfacedirection': 90.0},
     '11': {'layer': 'second',
            'material': None,
            'normal': [-0.0, -1.0, -0.0],
            'parent': None,
            'points': [[77.399864373684096,
                        -31.935616071834801,
                        -5.1202222995549502e-17],
                       [317.39986437368401,
                        -31.935616071834801,
                        -5.1202222995549502e-17],
                       [317.39986437368401, -31.935616071834801, 36.0],
                       [77.399864373684096, -31.935616071834801, 36.0]],
            'surfacedirection': 90.0},
     '12': {'layer': 'second',
            'material': None,
            'normal': [-1.0, 0.0, 0.0],
            'parent': None,
            'points': [[77.399864373684096,
                        172.064383928165,
                        -5.1202222995549502e-17],
                       [77.399864373684096,
                        -31.935616071834801,
                        -5.1202222995549502e-17],
                       [77.399864373684096, -31.935616071834801, 36.0],
                       [77.399864373684096, 172.064383928165, 36.0]],
            'surfacedirection': 90.0},
     '2': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, 1.0],
           'parent': None,
           'points': [[-54.814574283752997, 210.80705971907801, 84.0],
                      [-54.814574283752997, 450.80705971907798, 84.0],
                      [-174.81457428375299, 450.80705971907798, 84.0],
                      [-174.81457428375299, 210.80705971907801, 84.0]],
           'surfacedirection': 0.0},
     '3': {'layer': 'first',
           'material': None,
           'normal': [1.0, 0.0, 0.0],
           'parent': None,
           'points': [[-54.814574283752997,
                       210.80705971907801,
                       5.7705587212691398e-15],
                      [-54.814574283752997,
                       450.80705971907798,
                       5.7705587212691398e-15],
                      [-54.814574283752997, 450.80705971907798, 84.0],
                      [-54.814574283752997, 210.80705971907801, 84.0]],
           'surfacedirection': 90.0},
     '4': {'layer': 'first',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'points': [[-174.81457428375299,
                       210.80705971907801,
                       5.7705587212691398e-15],
                      [-54.814574283752997,
                       210.80705971907801,
                       5.7705587212691398e-15],
                      [-54.814574283752997, 210.80705971907801, 84.0],
                      [-174.81457428375299, 210.80705971907801, 84.0]],
           'surfacedirection': 90.0},
     '5': {'layer': 'first',
           'material': None,
           'normal': [-1.0, 0.0, 0.0],
           'parent': None,
           'points': [[-174.81457428375299,
                       450.80705971907798,
                       5.7705587212691398e-15],
                      [-174.81457428375299,
                       210.80705971907801,
                       5.7705587212691398e-15],
                      [-174.81457428375299, 210.80705971907801, 84.0],
                      [-174.81457428375299, 450.80705971907798, 84.0]],
           'surfacedirection': 90.0},
     '6': {'layer': 'first',
           'material': None,
           'normal': [-0.0, 1.0, 0.0],
           'parent': None,
           'points': [[-54.814574283752997,
                       450.80705971907798,
                       5.7705587212691398e-15],
                      [-174.81457428375299,
                       450.80705971907798,
                       5.7705587212691398e-15],
                      [-174.81457428375299, 450.80705971907798, 84.0],
                      [-54.814574283752997, 450.80705971907798, 84.0]],
           'surfacedirection': 90.0},
     '7': {'layer': 'second',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[77.399864373684096,
                       172.064383928165,
                       -5.1202222995549502e-17],
                      [317.39986437368401,
                       172.064383928165,
                       -5.1202222995549502e-17],
                      [317.39986437368401,
                       -31.935616071834801,
                       -5.1202222995549502e-17],
                      [77.399864373684096,
                       -31.935616071834801,
                       -5.1202222995549502e-17]],
           'surfacedirection': 180.0},
     '8': {'layer': 'second',
           'material': None,
           'normal': [0.0, 0.0, 1.0],
           'parent': None,
           'points': [[317.39986437368401, 172.064383928165, 36.0],
                      [77.399864373684096, 172.064383928165, 36.0],
                      [77.399864373684096, -31.935616071834801, 36.0],
                      [317.39986437368401, -31.935616071834801, 36.0]],
           'surfacedirection': 0.0},
     '9': {'layer': 'second',
           'material': None,
           'normal': [-0.0, 1.0, 0.0],
           'parent': None,
           'points': [[317.39986437368401,
                       172.064383928165,
                       -5.1202222995549502e-17],
                      [77.399864373684096,
                       172.064383928165,
                       -5.1202222995549502e-17],
                      [77.399864373684096, 172.064383928165, 36.0],
                      [317.39986437368401, 172.064383928165, 36.0]],
           'surfacedirection': 90.0}}
    eplustxt = """!-   ===========  ALL OBJECTS IN CLASS: ZONE ===========

ZONE,
    first,                   !- Zone Name
    0,                       !- Relative North (to building) {deg}
    0,                       !- X Origin {m}
    0,                       !- Y Origin {m}
    0,                       !- Z Origin {m}
    1,                       !- Type
    1,                       !- Multiplier
    84.0,                    !- Ceiling Height {m}
    2419200.0;               !- Volume {m3}

ZONE,
    second,                  !- Zone Name
    0,                       !- Relative North (to building) {deg}
    0,                       !- X Origin {m}
    0,                       !- Y Origin {m}
    0,                       !- Z Origin {m}
    1,                       !- Type
    1,                       !- Multiplier
    36.0,                    !- Ceiling Height {m}
    1762560.0;               !- Volume {m3}

"""
    layers = ['first', 'second']


class AllWalls_Data(object):
    dct = {'1': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'surfacedirection':180,
           'parent': None,
           'points': [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]},
     '10': {'layer': 'second',
            'material': 'm10',
            'surfacedirection':90,
            'normal': [-0.0, -1.0, -0.0],
            'parent': None,
            'points': [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]},
     '11': {'layer': 'second',
            'material': 'm11',
            'normal': [-1.0, 0.0, 0.0],
            'surfacedirection':90,
            'parent': None,
            'points': [[11, 12, 13], [14, 15, 16], [17, 18, 19], [20, 21, 22]]},
     '12': {'layer': 'second',
            'material': 'None',
            'normal': [-0.0, 1.0, 0.0],
            'surfacedirection':90,
            'parent': None,
            'points': [[12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23]]},
     '2': {'layer': 'first',
           'material': 'None',
           'normal': [0.0, 0.0, -1.0],
           'surfacedirection':90,
           'parent': None,
           'points': [[12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23]]},
     '3': {'layer': 'first',
           'material': 'None',
           'normal': [0.0, 0.0, 1.0],
           'surfacedirection':90,
           'parent': None,
           'points': [[3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14]]},
     '4': {'layer': 'first',
           'material': 'None',
           'normal': [-0.0, 1.0, 0.0],
           'surfacedirection':90,
           'parent': None,
           'points': [[4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]},
     '5': {'layer': 'first',
           'material': 'None',
           'normal': [1.0, 0.0, 0.0],
           'surfacedirection':90,
           'parent': None,
           'points': [[5, 6, 7], [8, 9, 10], [11, 12, 13], [14, 15, 16]]},
     '6': {'layer': 'first',
           'material': 'None',
           'normal': [-0.0, -1.0, -0.0],
           'surfacedirection':90,
           'parent': None,
           'points': [[6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17]]},
     '7': {'layer': 'second',
           'material': 'None',
           'normal': [-1.0, 0.0, 0.0],
           'surfacedirection':90,
           'parent': None,
           'points': [[7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]]},
     '8': {'layer': 'second',
           'material': 'w8',
           'normal': [0.0, 0.0, 1.0],
           'surfacedirection':180,
           'parent': None,
           'points':[[8, 9, 10], [11, 12, 13], [14, 15, 16], [17, 18, 19]]},
     '9': {'layer': 'second',
           'material': 'None',
           'normal': [1.0, 0.0, 0.0],
           'surfacedirection':0,
           'parent': None,
           'points': [[9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20]]},
     'z10': {'layer': 'second',
            'material': 'm10',
            'surfacedirection':90,
            'normal': [-0.0, -1.0, -0.0],
            'parent': 9,
            'points': [[10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21]]},
           }
    eplustxt = """!-   ===========  ALL OBJECTS IN CLASS: SURFACE:HEATTRANSFER ===========

Surface:HeatTransfer,
    1,                       !- User Supplied Surface Name
    FLOOR,                   !- Surface Type
    None,                    !- Construction Name of the Surface
    first,                   !- InsideFaceEnvironment
    10,                      !- OutsideFaceEnvironment
    OtherZoneSurface,        !- OutsideFaceEnvironment Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    1,                       !- Vertex 1 X-coordinate {m}
    2,                       !- Vertex 1 Y-coordinate {m}
    3,                       !- Vertex 1 Z-coordinate {m}
    4,                       !- Vertex 2 X-coordinate {m}
    5,                       !- Vertex 2 Y-coordinate {m}
    6,                       !- Vertex 2 Z-coordinate {m}
    7,                       !- Vertex 3 X-coordinate {m}
    8,                       !- Vertex 3 Y-coordinate {m}
    9,                       !- Vertex 3 Z-coordinate {m}
    10,                      !- Vertex 4 X-coordinate {m}
    11,                      !- Vertex 4 Y-coordinate {m}
    12;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    10,                      !- User Supplied Surface Name
    WALL,                    !- Surface Type
    m10,                     !- Construction Name of the Surface
    second,                  !- InsideFaceEnvironment
    1,                       !- OutsideFaceEnvironment
    OtherZoneSurface,        !- OutsideFaceEnvironment Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    1,                       !- Vertex 1 X-coordinate {m}
    2,                       !- Vertex 1 Y-coordinate {m}
    3,                       !- Vertex 1 Z-coordinate {m}
    4,                       !- Vertex 2 X-coordinate {m}
    5,                       !- Vertex 2 Y-coordinate {m}
    6,                       !- Vertex 2 Z-coordinate {m}
    7,                       !- Vertex 3 X-coordinate {m}
    8,                       !- Vertex 3 Y-coordinate {m}
    9,                       !- Vertex 3 Z-coordinate {m}
    10,                      !- Vertex 4 X-coordinate {m}
    11,                      !- Vertex 4 Y-coordinate {m}
    12;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    11,                      !- User Supplied Surface Name
    WALL,                    !- Surface Type
    m11,                     !- Construction Name of the Surface
    second,                  !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    11,                      !- Vertex 1 X-coordinate {m}
    12,                      !- Vertex 1 Y-coordinate {m}
    13,                      !- Vertex 1 Z-coordinate {m}
    14,                      !- Vertex 2 X-coordinate {m}
    15,                      !- Vertex 2 Y-coordinate {m}
    16,                      !- Vertex 2 Z-coordinate {m}
    17,                      !- Vertex 3 X-coordinate {m}
    18,                      !- Vertex 3 Y-coordinate {m}
    19,                      !- Vertex 3 Z-coordinate {m}
    20,                      !- Vertex 4 X-coordinate {m}
    21,                      !- Vertex 4 Y-coordinate {m}
    22;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    12,                      !- User Supplied Surface Name
    WALL,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    second,                  !- InsideFaceEnvironment
    2,                       !- OutsideFaceEnvironment
    OtherZoneSurface,        !- OutsideFaceEnvironment Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    12,                      !- Vertex 1 X-coordinate {m}
    13,                      !- Vertex 1 Y-coordinate {m}
    14,                      !- Vertex 1 Z-coordinate {m}
    15,                      !- Vertex 2 X-coordinate {m}
    16,                      !- Vertex 2 Y-coordinate {m}
    17,                      !- Vertex 2 Z-coordinate {m}
    18,                      !- Vertex 3 X-coordinate {m}
    19,                      !- Vertex 3 Y-coordinate {m}
    20,                      !- Vertex 3 Z-coordinate {m}
    21,                      !- Vertex 4 X-coordinate {m}
    22,                      !- Vertex 4 Y-coordinate {m}
    23;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    2,                       !- User Supplied Surface Name
    WALL,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    first,                   !- InsideFaceEnvironment
    12,                      !- OutsideFaceEnvironment
    OtherZoneSurface,        !- OutsideFaceEnvironment Object
    NoSun,                   !- Sun Exposure
    NoWind,                  !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    12,                      !- Vertex 1 X-coordinate {m}
    13,                      !- Vertex 1 Y-coordinate {m}
    14,                      !- Vertex 1 Z-coordinate {m}
    15,                      !- Vertex 2 X-coordinate {m}
    16,                      !- Vertex 2 Y-coordinate {m}
    17,                      !- Vertex 2 Z-coordinate {m}
    18,                      !- Vertex 3 X-coordinate {m}
    19,                      !- Vertex 3 Y-coordinate {m}
    20,                      !- Vertex 3 Z-coordinate {m}
    21,                      !- Vertex 4 X-coordinate {m}
    22,                      !- Vertex 4 Y-coordinate {m}
    23;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    3,                       !- User Supplied Surface Name
    WALL,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    first,                   !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    3,                       !- Vertex 1 X-coordinate {m}
    4,                       !- Vertex 1 Y-coordinate {m}
    5,                       !- Vertex 1 Z-coordinate {m}
    6,                       !- Vertex 2 X-coordinate {m}
    7,                       !- Vertex 2 Y-coordinate {m}
    8,                       !- Vertex 2 Z-coordinate {m}
    9,                       !- Vertex 3 X-coordinate {m}
    10,                      !- Vertex 3 Y-coordinate {m}
    11,                      !- Vertex 3 Z-coordinate {m}
    12,                      !- Vertex 4 X-coordinate {m}
    13,                      !- Vertex 4 Y-coordinate {m}
    14;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    4,                       !- User Supplied Surface Name
    WALL,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    first,                   !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    4,                       !- Vertex 1 X-coordinate {m}
    5,                       !- Vertex 1 Y-coordinate {m}
    6,                       !- Vertex 1 Z-coordinate {m}
    7,                       !- Vertex 2 X-coordinate {m}
    8,                       !- Vertex 2 Y-coordinate {m}
    9,                       !- Vertex 2 Z-coordinate {m}
    10,                      !- Vertex 3 X-coordinate {m}
    11,                      !- Vertex 3 Y-coordinate {m}
    12,                      !- Vertex 3 Z-coordinate {m}
    13,                      !- Vertex 4 X-coordinate {m}
    14,                      !- Vertex 4 Y-coordinate {m}
    15;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    5,                       !- User Supplied Surface Name
    WALL,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    first,                   !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    5,                       !- Vertex 1 X-coordinate {m}
    6,                       !- Vertex 1 Y-coordinate {m}
    7,                       !- Vertex 1 Z-coordinate {m}
    8,                       !- Vertex 2 X-coordinate {m}
    9,                       !- Vertex 2 Y-coordinate {m}
    10,                      !- Vertex 2 Z-coordinate {m}
    11,                      !- Vertex 3 X-coordinate {m}
    12,                      !- Vertex 3 Y-coordinate {m}
    13,                      !- Vertex 3 Z-coordinate {m}
    14,                      !- Vertex 4 X-coordinate {m}
    15,                      !- Vertex 4 Y-coordinate {m}
    16;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    6,                       !- User Supplied Surface Name
    WALL,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    first,                   !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    6,                       !- Vertex 1 X-coordinate {m}
    7,                       !- Vertex 1 Y-coordinate {m}
    8,                       !- Vertex 1 Z-coordinate {m}
    9,                       !- Vertex 2 X-coordinate {m}
    10,                      !- Vertex 2 Y-coordinate {m}
    11,                      !- Vertex 2 Z-coordinate {m}
    12,                      !- Vertex 3 X-coordinate {m}
    13,                      !- Vertex 3 Y-coordinate {m}
    14,                      !- Vertex 3 Z-coordinate {m}
    15,                      !- Vertex 4 X-coordinate {m}
    16,                      !- Vertex 4 Y-coordinate {m}
    17;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    7,                       !- User Supplied Surface Name
    WALL,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    second,                  !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.5,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    7,                       !- Vertex 1 X-coordinate {m}
    8,                       !- Vertex 1 Y-coordinate {m}
    9,                       !- Vertex 1 Z-coordinate {m}
    10,                      !- Vertex 2 X-coordinate {m}
    11,                      !- Vertex 2 Y-coordinate {m}
    12,                      !- Vertex 2 Z-coordinate {m}
    13,                      !- Vertex 3 X-coordinate {m}
    14,                      !- Vertex 3 Y-coordinate {m}
    15,                      !- Vertex 3 Z-coordinate {m}
    16,                      !- Vertex 4 X-coordinate {m}
    17,                      !- Vertex 4 Y-coordinate {m}
    18;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    8,                       !- User Supplied Surface Name
    FLOOR,                   !- Surface Type
    w8,                      !- Construction Name of the Surface
    second,                  !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    8,                       !- Vertex 1 X-coordinate {m}
    9,                       !- Vertex 1 Y-coordinate {m}
    10,                      !- Vertex 1 Z-coordinate {m}
    11,                      !- Vertex 2 X-coordinate {m}
    12,                      !- Vertex 2 Y-coordinate {m}
    13,                      !- Vertex 2 Z-coordinate {m}
    14,                      !- Vertex 3 X-coordinate {m}
    15,                      !- Vertex 3 Y-coordinate {m}
    16,                      !- Vertex 3 Z-coordinate {m}
    17,                      !- Vertex 4 X-coordinate {m}
    18,                      !- Vertex 4 Y-coordinate {m}
    19;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer,
    9,                       !- User Supplied Surface Name
    ROOF,                    !- Surface Type
    None,                    !- Construction Name of the Surface
    second,                  !- InsideFaceEnvironment
    ExteriorEnvironment,     !- OutsideFaceEnvironment
    ,                        !- OutsideFaceEnvironment Object
    SunExposed,              !- Sun Exposure
    WindExposed,             !- Wind Exposure
    0.0,                     !- View Factor to Ground
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    9,                       !- Vertex 1 X-coordinate {m}
    10,                      !- Vertex 1 Y-coordinate {m}
    11,                      !- Vertex 1 Z-coordinate {m}
    12,                      !- Vertex 2 X-coordinate {m}
    13,                      !- Vertex 2 Y-coordinate {m}
    14,                      !- Vertex 2 Z-coordinate {m}
    15,                      !- Vertex 3 X-coordinate {m}
    16,                      !- Vertex 3 Y-coordinate {m}
    17,                      !- Vertex 3 Z-coordinate {m}
    18,                      !- Vertex 4 X-coordinate {m}
    19,                      !- Vertex 4 Y-coordinate {m}
    20;                      !- Vertex 4 Z-coordinate {m}

"""

class Window_Data(object):
    dct1 = {'2': {'layer': 'Layer0',
           'material': '<StoneVein>',
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'points': [[1.62660365955518,
                       226.34365957003899,
                       -8.2063549145093297e-15],
                      [295.87660365955497,
                       226.34365957003899,
                       -8.2063549145093297e-15],
                      [295.87660365955497, 226.34365957003899, 91.75],
                      [1.62660365955518, 226.34365957003899, 91.75]],
           'surfacedirection': '90'},
     '3': {'layer': 'Layer0',
           'material': '<StoneVein>',
           'normal': [-0.0, -1.0, -0.0],
           'parent': '2',
           'points': [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
           'surfacedirection': '90'}}
    eplustxt1 ="""!-   ===========  ALL OBJECTS IN CLASS: SURFACE:HEATTRANSFER:SUB ===========

Surface:HeatTransfer:Sub,
    3,                       !- User Supplied Surface Name
    WINDOW,                  !- Surface Type
    <StoneVein>,             !- Construction Name of the Surface
    2,                       !- Base Surface Name
    ,                        !- OutsideFaceEnvironment Object
    0.50000,                 !- View Factor to Ground
    ,                        !- Name of shading control
    ,                        !- WindowFrameAndDivider Name
    1,                       !- Multiplier
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    1,                       !- Vertex 1 X-coordinate {m}
    2,                       !- Vertex 1 Y-coordinate {m}
    3,                       !- Vertex 1 Z-coordinate {m}
    4,                       !- Vertex 2 X-coordinate {m}
    5,                       !- Vertex 2 Y-coordinate {m}
    6,                       !- Vertex 2 Z-coordinate {m}
    7,                       !- Vertex 3 X-coordinate {m}
    8,                       !- Vertex 3 Y-coordinate {m}
    9,                       !- Vertex 3 Z-coordinate {m}
    10,                      !- Vertex 4 X-coordinate {m}
    11,                      !- Vertex 4 Y-coordinate {m}
    12;                      !- Vertex 4 Z-coordinate {m}

"""
    dct2 = {'3': {'layer': 'Layer0',
           'material': None,
           'normal': [1.0, 0.0, 0.0],
           'parent': None,
           'points': [[3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14]],
           'surfacedirection': 90.0},
     '4': {'layer': 'Layer0',
           'material': '<Stone-Shakes>',
           'normal': [1.0, 0.0, 0.0],
           'parent': '3',
           'points': [[4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]],
           'surfacedirection': 90.0},
     '6': {'layer': 'Layer0',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'points': [[6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17]],
           'surfacedirection': 90.0},
     '7': {'layer': 'Layer0',
           'material': '<Stone walk>',
           'normal': [-0.0, -1.0, -0.0],
           'parent': '6',
           'points': [[7, 8, 9], [10, 11, 12], [13, 14, 15], [16, 17, 18]],
           'surfacedirection': 90.0},
     '8': {'layer': 'Layer0',
           'material': '<Ashlar Stone>',
           'normal': [-0.0, -1.0, -0.0],
           'parent': '6',
           'points': [[8, 9, 10], [11, 12, 13], [14, 15, 16], [17, 18, 19]],
           'surfacedirection': 90.0}}
    eplustxt2 = """!-   ===========  ALL OBJECTS IN CLASS: SURFACE:HEATTRANSFER:SUB ===========

Surface:HeatTransfer:Sub,
    4,                       !- User Supplied Surface Name
    WINDOW,                  !- Surface Type
    <Stone-Shakes>,          !- Construction Name of the Surface
    3,                       !- Base Surface Name
    ,                        !- OutsideFaceEnvironment Object
    0.50000,                 !- View Factor to Ground
    ,                        !- Name of shading control
    ,                        !- WindowFrameAndDivider Name
    1,                       !- Multiplier
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    4,                       !- Vertex 1 X-coordinate {m}
    5,                       !- Vertex 1 Y-coordinate {m}
    6,                       !- Vertex 1 Z-coordinate {m}
    7,                       !- Vertex 2 X-coordinate {m}
    8,                       !- Vertex 2 Y-coordinate {m}
    9,                       !- Vertex 2 Z-coordinate {m}
    10,                      !- Vertex 3 X-coordinate {m}
    11,                      !- Vertex 3 Y-coordinate {m}
    12,                      !- Vertex 3 Z-coordinate {m}
    13,                      !- Vertex 4 X-coordinate {m}
    14,                      !- Vertex 4 Y-coordinate {m}
    15;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer:Sub,
    7,                       !- User Supplied Surface Name
    WINDOW,                  !- Surface Type
    <Stone walk>,            !- Construction Name of the Surface
    6,                       !- Base Surface Name
    ,                        !- OutsideFaceEnvironment Object
    0.50000,                 !- View Factor to Ground
    ,                        !- Name of shading control
    ,                        !- WindowFrameAndDivider Name
    1,                       !- Multiplier
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    7,                       !- Vertex 1 X-coordinate {m}
    8,                       !- Vertex 1 Y-coordinate {m}
    9,                       !- Vertex 1 Z-coordinate {m}
    10,                      !- Vertex 2 X-coordinate {m}
    11,                      !- Vertex 2 Y-coordinate {m}
    12,                      !- Vertex 2 Z-coordinate {m}
    13,                      !- Vertex 3 X-coordinate {m}
    14,                      !- Vertex 3 Y-coordinate {m}
    15,                      !- Vertex 3 Z-coordinate {m}
    16,                      !- Vertex 4 X-coordinate {m}
    17,                      !- Vertex 4 Y-coordinate {m}
    18;                      !- Vertex 4 Z-coordinate {m}

Surface:HeatTransfer:Sub,
    8,                       !- User Supplied Surface Name
    WINDOW,                  !- Surface Type
    <Ashlar Stone>,          !- Construction Name of the Surface
    6,                       !- Base Surface Name
    ,                        !- OutsideFaceEnvironment Object
    0.50000,                 !- View Factor to Ground
    ,                        !- Name of shading control
    ,                        !- WindowFrameAndDivider Name
    1,                       !- Multiplier
    4,                       !- Number of Surface Vertex Groups -- Number of (X,Y,Z) groups in this surface
    8,                       !- Vertex 1 X-coordinate {m}
    9,                       !- Vertex 1 Y-coordinate {m}
    10,                      !- Vertex 1 Z-coordinate {m}
    11,                      !- Vertex 2 X-coordinate {m}
    12,                      !- Vertex 2 Y-coordinate {m}
    13,                      !- Vertex 2 Z-coordinate {m}
    14,                      !- Vertex 3 X-coordinate {m}
    15,                      !- Vertex 3 Y-coordinate {m}
    16,                      !- Vertex 3 Z-coordinate {m}
    17,                      !- Vertex 4 X-coordinate {m}
    18,                      !- Vertex 4 Y-coordinate {m}
    19;                      !- Vertex 4 Z-coordinate {m}

"""

class ZoneArea_Data(object):
    dct = {'1': {'layer': 'first',
           'material': None,
           'normal': [0.0, 1.0, 0.0],
           'parent': None,
           'points': [[299.26804385386203,
                       275.78656625474702,
                       1.83032150696908e-14],
                      [161.768043853862,
                       275.78656625474702,
                       1.83032150696908e-14],
                      [161.768043853862, 275.78656625474702, 96.0],
                      [299.26804385386203, 275.78656625474702, 96.0]],
           'surfacedirection': 90.0},
     '2': {'layer': 'second',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'points': [[-69.313540902754795,
                       86.137280742452702,
                       1.45834325218528e-15],
                      [68.128066054739307,
                       86.137280742452702,
                       1.45834325218528e-15],
                      [68.128066054739307, 86.137280742452702, 52.25],
                      [-119.968385137436, 86.137280742452702, 52.25],
                      [-119.968385137436,
                       86.137280742452702,
                       1.45834325218528e-15]],
           'surfacedirection': 90.0},
     '3': {'layer': 'second',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[-119.968385137436,
                       202.38728074245299,
                       1.45834325218528e-15],
                      [12.4839366948523,
                       202.38728074245299,
                       1.45834325218528e-15],
                      [-69.313540902754795,
                       86.137280742452702,
                       1.45834325218528e-15],
                      [-119.968385137436,
                       86.137280742452702,
                       1.45834325218528e-15]],
           'surfacedirection': 180.0},
     '4': {'layer': 'second',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[68.128066054739307,
                       86.137280742452702,
                       1.45834325218528e-15],
                      [-69.313540902754795,
                       86.137280742452702,
                       1.45834325218528e-15],
                      [12.4839366948523,
                       202.38728074245299,
                       1.45834325218528e-15],
                      [68.128066054739307,
                       202.38728074245299,
                       1.45834325218528e-15]],
           'surfacedirection': 180.0}}
    area = 21866.2124510904
    zone = 'second'

class ZoneBounds_Data(object):
    dct1 = {'1': {'layer': 'first',
           'material': None,
           'normal': [1.0, 0.0, 0.0],
           'parent': None,
           'points': [[180.0, 0.0, 0.0],
                      [180.0, 240.0, 0.0],
                      [180.0, 240.0, 60.0],
                      [180.0, 0.0, 60.0]],
           'surfacedirection': 90.0},
     '2': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, 1.0],
           'parent': None,
           'points': [[0.0, 240.0, 60.0],
                      [0.0, 0.0, 60.0],
                      [180.0, 0.0, 60.0],
                      [180.0, 240.0, 60.0]],
           'surfacedirection': 0.0},
     '3': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[0.0, 0.0, 0.0],
                      [0.0, 240.0, 0.0],
                      [180.0, 240.0, 0.0],
                      [180.0, 0.0, 0.0]],
           'surfacedirection': 180.0},
     '4': {'layer': 'first',
           'material': None,
           'normal': [-1.0, 0.0, 0.0],
           'parent': None,
           'points': [[0.0, 240.0, 0.0],
                      [0.0, 0.0, 0.0],
                      [0.0, 0.0, 60.0],
                      [0.0, 240.0, 60.0]],
           'surfacedirection': 90.0},
     '5': {'layer': 'first',
           'material': None,
           'normal': [0.0, 1.0, 0.0],
           'parent': None,
           'points': [[180.0, 240.0, 0.0],
                      [0.0, 240.0, 0.0],
                      [0.0, 240.0, 60.0],
                      [180.0, 240.0, 60.0]],
           'surfacedirection': 90.0},
     '6': {'layer': 'first',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'points': [[0.0, 0.0, 0.0],
                      [180.0, 0.0, 0.0],
                      [180.0, 0.0, 60.0],
                      [0.0, 0.0, 60.0]],
           'surfacedirection': 90.0},
     '7': {'layer': 'second',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[271.32453755763402,
                       207.22240502876201,
                       -1.9914461569524102e-15],
                      [205.32453755763399,
                       207.22240502876201,
                       -1.9914461569524102e-15],
                      [205.32453755763399,
                       284.47240502876201,
                       -1.9914461569524102e-15],
                      [271.32453755763402,
                       284.47240502876201,
                       -1.9914461569524102e-15]],
           'surfacedirection': 180.0}}
    bounds1 = ((0, 0, 0),
            (180, 240, 60))
    dct2 = {'1': {'layer': 'first',
           'material': None,
           'normal': [0.97814760073380602,
                      -9.2525158004783101e-17,
                      0.20791169081776001],
           'parent': None,
           'points': [[182.57609719256499,
                       56.925529321728199,
                       8.1778301334397092],
                      [177.47745706699101,
                       148.44700136261699,
                       32.165045985610199],
                      [166.68299121051999,
                       134.53547768835699,
                       82.949015069701801],
                      [171.78163133609399,
                       43.014005647467698,
                       58.961799217531301]],
           'surfacedirection': 78.0},
     '2': {'layer': 'first',
           'material': None,
           'normal': [-0.053811505283103002,
                      0.96592582628906798,
                      0.25316322799124502],
           'parent': None,
           'points': [[177.47745706699101,
                       148.44700136261699,
                       32.165045985610199],
                      [12.415049443160999,
                       148.44700136261699,
                       -2.9200518398867499],
                      [1.62058358668979, 134.53547768835699, 47.863917244204799],
                      [166.68299121051999,
                       134.53547768835699,
                       82.949015069701801]],
           'surfacedirection': 75.335224998629499},
     '3': {'layer': 'first',
           'material': None,
           'normal': [-0.20082727174830201,
                      -0.25881904510252102,
                      0.94481802947147098],
           'parent': None,
           'points': [[166.68299121051999,
                       134.53547768835699,
                       82.949015069701801],
                      [1.62058358668979, 134.53547768835699, 47.863917244204799],
                      [6.7192237122638003,
                       43.014005647467698,
                       23.876701392034299],
                      [171.78163133609399,
                       43.014005647467698,
                       58.961799217531301]],
           'surfacedirection': 19.122904308444699},
     '4': {'layer': 'first',
           'material': None,
           'normal': [0.053811505283103002,
                      -0.96592582628906798,
                      -0.25316322799124502],
           'parent': None,
           'points': [[17.513689568735, 56.925529321728199, -26.9072676920572],
                      [182.57609719256499,
                       56.925529321728199,
                       8.1778301334397092],
                      [171.78163133609399,
                       43.014005647467698,
                       58.961799217531301],
                      [6.7192237122638003,
                       43.014005647467698,
                       23.876701392034299]],
           'surfacedirection': 104.66477500137},
     '5': {'layer': 'first',
           'material': None,
           'normal': [0.20082727174830201,
                      0.25881904510252102,
                      -0.94481802947147098],
           'parent': None,
           'points': [[12.415049443160999,
                       148.44700136261699,
                       -2.9200518398867499],
                      [177.47745706699101,
                       148.44700136261699,
                       32.165045985610199],
                      [182.57609719256499,
                       56.925529321728199,
                       8.1778301334397092],
                      [17.513689568735, 56.925529321728199, -26.9072676920572]],
           'surfacedirection': 160.87709569155501},
     '6': {'layer': 'first',
           'material': None,
           'normal': [-0.97814760073380602,
                      9.2525158004783101e-17,
                      -0.20791169081776001],
           'parent': None,
           'points': [[12.415049443160999,
                       148.44700136261699,
                       -2.9200518398867499],
                      [17.513689568735, 56.925529321728199, -26.9072676920572],
                      [6.7192237122638003,
                       43.014005647467698,
                       23.876701392034299],
                      [1.62058358668979, 134.53547768835699, 47.863917244204799]],
           'surfacedirection': 102.0},
     '7': {'layer': 'second',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[262.75350511699099,
                       212.49385276807899,
                       9.8167176916946802e-15],
                      [160.75350511699099,
                       212.49385276807899,
                       9.8167176916946802e-15],
                      [160.75350511699099,
                       283.24385276807902,
                       9.8167176916946802e-15],
                      [262.75350511699099,
                       283.24385276807902,
                       9.8167176916946802e-15]],
           'surfacedirection': 180.0}}
    bounds2 = ((1.620584, 43.014006,  -26.907268),
        (182.576097, 148.447001, 82.949015))

class MarkSameFace_Data(object):
    dct = {'1': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[-357.16721363710201,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-357.16721363710201,
                       173.09022834891701,
                       -1.3757642575183699e-14]],
           'surfacedirection': 180.0},
     '10': {'layer': 'second',
            'material': None,
            'normal': [0.0, 1.0, 0.0],
            'parent': None,
            'points': [[243.83278636289799,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902, 372.34022834891698, 72.75],
                       [243.83278636289799, 372.34022834891698, 72.75]],
            'surfacedirection': 90.0},
     '11': {'layer': 'second',
            'material': None,
            'normal': [1.0, 0.0, 0.0],
            'parent': None,
            'points': [[243.83278636289799,
                        173.09022834891701,
                        -1.3757642575183699e-14],
                       [243.83278636289799,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [243.83278636289799, 372.34022834891698, 72.75],
                       [243.83278636289799, 173.09022834891701, 72.75]],
            'surfacedirection': 90.0},
     '12': {'layer': 'second',
            'material': None,
            'normal': [0.0, 0.0, 1.0],
            'parent': None,
            'points': [[243.83278636289799, 372.34022834891698, 72.75],
                       [-56.667213637101902, 372.34022834891698, 72.75],
                       [-56.667213637101902, 272.71522834891698, 72.75],
                       [-56.667213637101902, 173.09022834891701, 72.75],
                       [243.83278636289799, 173.09022834891701, 72.75]],
            'surfacedirection': 0.0},
     '13': {'layer': 'second',
            'material': '<Stone walk>',
            'normal': [-1.0, 0.0, 0.0],
            'parent': None,
            'points': [[-56.667213637101902,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        272.71522834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902, 272.71522834891698, 72.75],
                       [-56.667213637101902, 372.34022834891698, 72.75]],
            'surfacedirection': 90.0},
     '14': {'layer': 'second',
            'material': None,
            'normal': [0.0, 0.0, -1.0],
            'parent': None,
            'points': [[-56.667213637101902,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [243.83278636289799,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [243.83278636289799,
                        173.09022834891701,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        173.09022834891701,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        272.71522834891698,
                        -1.3757642575183699e-14]],
            'surfacedirection': 180.0},
     '2': {'layer': 'first',
           'material': '<Stone walk>',
           'normal': [1.0, 0.0, 0.0],
           'parent': None,
           'points': [[-56.667213637101902, 372.34022834891698, 72.75],
                      [-56.667213637101902, 272.71522834891698, 72.75],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       372.34022834891698,
                       -1.3757642575183699e-14]],
           'surfacedirection': 90.0},
     '3': {'layer': 'first',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'points': [[-357.16721363710201,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-56.667213637101902, 173.09022834891701, 72.75],
                      [-357.16721363710201, 173.09022834891701, 72.75]],
           'surfacedirection': 90.0},
     '4': {'layer': 'first',
           'material': None,
           'normal': [-1.0, 0.0, 0.0],
           'parent': None,
           'points': [[-357.16721363710201,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-357.16721363710201,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-357.16721363710201, 173.09022834891701, 72.75],
                      [-357.16721363710201, 372.34022834891698, 72.75]],
           'surfacedirection': 90.0},
     '5': {'layer': 'first',
           'material': '<Stone-masonry>',
           'normal': [1.0, 0.0, 0.0],
           'parent': None,
           'points': [[-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902, 272.71522834891698, 72.75],
                      [-56.667213637101902, 173.09022834891701, 72.75]],
           'surfacedirection': 90.0},
     '6': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, 1.0],
           'parent': None,
           'points': [[-56.667213637101902, 372.34022834891698, 72.75],
                      [-357.16721363710201, 372.34022834891698, 72.75],
                      [-357.16721363710201, 173.09022834891701, 72.75],
                      [-56.667213637101902, 173.09022834891701, 72.75],
                      [-56.667213637101902, 272.71522834891698, 72.75]],
           'surfacedirection': 0.0},
     '7': {'layer': 'first',
           'material': None,
           'normal': [0.0, 1.0, 0.0],
           'parent': None,
           'points': [[-56.667213637101902,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-357.16721363710201,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-357.16721363710201, 372.34022834891698, 72.75],
                      [-56.667213637101902, 372.34022834891698, 72.75]],
           'surfacedirection': 90.0},
     '8': {'layer': 'second',
           'material': '<Stone-masonry>',
           'normal': [-1.0, 0.0, 0.0],
           'parent': None,
           'points': [[-56.667213637101902, 173.09022834891701, 72.75],
                      [-56.667213637101902, 272.71522834891698, 72.75],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14]],
           'surfacedirection': 90.0},
     '9': {'layer': 'second',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'points': [[-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [243.83278636289799,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [243.83278636289799, 173.09022834891701, 72.75],
                      [-56.667213637101902, 173.09022834891701, 72.75]],
           'surfacedirection': 90.0}}
    markeddct = {'1': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'nextto': None,
           'points': [[-357.16721363710201,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-357.16721363710201,
                       173.09022834891701,
                       -1.3757642575183699e-14]],
           'surfacedirection': 180.0},
     '10': {'layer': 'second',
            'material': None,
            'normal': [0.0, 1.0, 0.0],
            'parent': None,
            'nextto': None,
            'points': [[243.83278636289799,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902, 372.34022834891698, 72.75],
                       [243.83278636289799, 372.34022834891698, 72.75]],
            'surfacedirection': 90.0},
     '11': {'layer': 'second',
            'material': None,
            'normal': [1.0, 0.0, 0.0],
            'parent': None,
            'nextto': None,
            'points': [[243.83278636289799,
                        173.09022834891701,
                        -1.3757642575183699e-14],
                       [243.83278636289799,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [243.83278636289799, 372.34022834891698, 72.75],
                       [243.83278636289799, 173.09022834891701, 72.75]],
            'surfacedirection': 90.0},
     '12': {'layer': 'second',
            'material': None,
            'normal': [0.0, 0.0, 1.0],
            'parent': None,
            'nextto': None,
            'points': [[243.83278636289799, 372.34022834891698, 72.75],
                       [-56.667213637101902, 372.34022834891698, 72.75],
                       [-56.667213637101902, 272.71522834891698, 72.75],
                       [-56.667213637101902, 173.09022834891701, 72.75],
                       [243.83278636289799, 173.09022834891701, 72.75]],
            'surfacedirection': 0.0},
     '13': {'layer': 'second',
            'material': '<Stone walk>',
            'normal': [-1.0, 0.0, 0.0],
            'parent': None,
            'nextto': '2',
            'points': [[-56.667213637101902,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        272.71522834891698,
                        -1.3757642575183699e-14],
                       [-56.667213637101902, 272.71522834891698, 72.75],
                       [-56.667213637101902, 372.34022834891698, 72.75]],
            'surfacedirection': 90.0},
     '14': {'layer': 'second',
            'material': None,
            'normal': [0.0, 0.0, -1.0],
            'parent': None,
            'nextto': None,
            'points': [[-56.667213637101902,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [243.83278636289799,
                        372.34022834891698,
                        -1.3757642575183699e-14],
                       [243.83278636289799,
                        173.09022834891701,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        173.09022834891701,
                        -1.3757642575183699e-14],
                       [-56.667213637101902,
                        272.71522834891698,
                        -1.3757642575183699e-14]],
            'surfacedirection': 180.0},
     '2': {'layer': 'first',
           'material': '<Stone walk>',
           'normal': [1.0, 0.0, 0.0],
           'parent': None,
           'nextto': '13',
           'points': [[-56.667213637101902, 372.34022834891698, 72.75],
                      [-56.667213637101902, 272.71522834891698, 72.75],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       372.34022834891698,
                       -1.3757642575183699e-14]],
           'surfacedirection': 90.0},
     '3': {'layer': 'first',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'nextto': None,
           'points': [[-357.16721363710201,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-56.667213637101902, 173.09022834891701, 72.75],
                      [-357.16721363710201, 173.09022834891701, 72.75]],
           'surfacedirection': 90.0},
     '4': {'layer': 'first',
           'material': None,
           'normal': [-1.0, 0.0, 0.0],
           'parent': None,
           'nextto': None,
           'points': [[-357.16721363710201,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-357.16721363710201,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-357.16721363710201, 173.09022834891701, 72.75],
                      [-357.16721363710201, 372.34022834891698, 72.75]],
           'surfacedirection': 90.0},
     '5': {'layer': 'first',
           'material': '<Stone-masonry>',
           'normal': [1.0, 0.0, 0.0],
           'parent': None,
           'nextto': '8',
           'points': [[-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902, 272.71522834891698, 72.75],
                      [-56.667213637101902, 173.09022834891701, 72.75]],
           'surfacedirection': 90.0},
     '6': {'layer': 'first',
           'material': None,
           'normal': [0.0, 0.0, 1.0],
           'parent': None,
           'nextto': None,
           'points': [[-56.667213637101902, 372.34022834891698, 72.75],
                      [-357.16721363710201, 372.34022834891698, 72.75],
                      [-357.16721363710201, 173.09022834891701, 72.75],
                      [-56.667213637101902, 173.09022834891701, 72.75],
                      [-56.667213637101902, 272.71522834891698, 72.75]],
           'surfacedirection': 0.0},
     '7': {'layer': 'first',
           'material': None,
           'normal': [0.0, 1.0, 0.0],
           'parent': None,
           'nextto': None,
           'points': [[-56.667213637101902,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-357.16721363710201,
                       372.34022834891698,
                       -1.3757642575183699e-14],
                      [-357.16721363710201, 372.34022834891698, 72.75],
                      [-56.667213637101902, 372.34022834891698, 72.75]],
           'surfacedirection': 90.0},
     '8': {'layer': 'second',
           'material': '<Stone-masonry>',
           'normal': [-1.0, 0.0, 0.0],
           'parent': None,
           'nextto': '5',
           'points': [[-56.667213637101902, 173.09022834891701, 72.75],
                      [-56.667213637101902, 272.71522834891698, 72.75],
                      [-56.667213637101902,
                       272.71522834891698,
                       -1.3757642575183699e-14],
                      [-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14]],
           'surfacedirection': 90.0},
     '9': {'layer': 'second',
           'material': None,
           'normal': [-0.0, -1.0, -0.0],
           'parent': None,
           'nextto': None,
           'points': [[-56.667213637101902,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [243.83278636289799,
                       173.09022834891701,
                       -1.3757642575183699e-14],
                      [243.83278636289799, 173.09022834891701, 72.75],
                      [-56.667213637101902, 173.09022834891701, 72.75]],
           'surfacedirection': 90.0}}
    