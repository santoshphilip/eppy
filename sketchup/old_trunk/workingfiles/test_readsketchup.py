# Copyright (c) 2012 Santosh Phillip

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

import readsketchup

try:
    set
except NameError:
    from sets import Set as set

def test_readsketchup():
    """py.test for readsketchup"""
    data = readsketchup_data
    result = readsketchup.readsketchup(data.txt)
    dct = data.dct
    assert set(tuple(result.keys())) == set(tuple(dct.keys()))
    # for key in result.keys():
    #     print result[key]
    #     print dct[key]
    #     assert result[key] == dct[key]
    assert result == dct
    
def test_txt2face():
    """py.test for txt2face()"""
    data = txt2face_data
    assert readsketchup.txt2face(data.facetxt) == data.facedct

def test_samepoly():
    """py.test for samepoly()"""
    data = (
        (
            [[5, 3, 8], [6, 7, 8]],
            [[5, 3, 8], [6, 7, 8], [8, 9, 0]],
            False
        ), 
        (
            [[5, 3, 8], [6, 7, 8], [8, 9, 0]],
            [[5, 3, 8], [6, 7, 8], [8, 9, 0]],
            True
        ), 
        (
            [[5, 3, 8], [6, 7, 8], [8, 9, 0]],
            [[5, 3, 8], [6, 7, 8], [8, 1, 0]],
            False
        ), 
        (
            [[5, 3, 8], [6, 7, 8], [8, 9, 0]],
            [[8, 9, 0], [6, 7, 8], [5, 3, 8]],
            True
        ), 
    )  
    for poly1, poly2, result in data:
        assert readsketchup.samepoly(poly1, poly2) == result

def test_duplicatewindows():
    """py.test for duplicatewindows()"""    
    data = DuplicateWindow_data
    result = readsketchup.duplicatewindows(data.dct1)
    newdct = data.result1
    # assert set(tuple(result.keys())) == set(tuple(newdct.keys()))
    # for key in result.keys():
    #     assert set((result[key].keys())) == set(tuple(newdct[key].keys()))
    #     for kkey in result[key].keys():
    #         print result[key][kkey]
    #         print newdct[key][kkey]
    #         assert result[key][kkey] == newdct[key][kkey]
    assert result == newdct

def test_striptxt():
    """test.py for striptxt"""
    txt = """    layer:second
    points:4
        -800 298 104
        -800 1103 104
        -1116 1103 104
        -1116 298 104
    normal:0.0 0.0 1.0
    material:newstuff-1
    parent:None
"""
    stripped = """layer:second
points:4
-800 298 104
-800 1103 104
-1116 1103 104
-1116 298 104
normal:0.0 0.0 1.0
material:newstuff-1
parent:None"""
    assert readsketchup.stripped(txt) == stripped


def test_inch2meters():
    """py.test for inch2meters()"""
    data = Inch2Meters_Data
    assert readsketchup.inch2meters(data.dct) == data.meters_dct 

class txt2face_data(object):
    facetxt = """    layer:second
    points:4
        -800 298 104
        -800 1103 104
        -1116 1103 104
        -1116 298 104
    normal:0.0 0.0 1.0
    surfacedirection:55
    material:newstuff-1
    parent:None
"""
    facedct = {'layer': 'second',
     'material': 'newstuff-1',
     'normal': [0.0, 0.0, 1.0],
     'surfacedirection':55,
     'parent': None,
     'points': [[-800.0, 298.0, 104.0],
      [-800.0, 1103.0, 104.0],
      [-1116.0, 1103.0, 104.0],
      [-1116.0, 298.0, 104.0]]
     }
    

    
    
class readsketchup_data(object):
    txt = """face:1
        layer:second
        points:4
            -800 298 104
            -800 1103 104
            -1116 1103 104
            -1116 298 104
        normal:0.0 0.0 1.0
        surfacedirection:135
        material:newstuff-1
        parent:None
    face:2
        layer:first
        points:4
            -800 298 104
            -800 1103 104
            -1116 1103 104
            -1116 298 104
        normal:-0.0 -0.0 1.0
        surfacedirection:135
        material:None
        parent:1
    """
    dct = {'1': {'layer': 'second',
           'material': 'newstuff-1',
           'normal': [0.0, 0.0, 1.0],
           'surfacedirection': 135,
           'parent': None,
           'points':[[-800, 298, 104],
            [-800, 1103, 104],
            [-1116, 1103, 104],
            [-1116, 298, 104]]},
     '2': {'layer': 'first',
           'material': None,
           'normal': [-0.0, -0.0, 1.0],
           'surfacedirection': 135,
           'parent': '1',
           'points':[[-800, 298, 104],
           [-800, 1103, 104],
           [-1116, 1103, 104],
           [-1116, 298, 104]]}
           }
    
class DuplicateWindow_data(object):
    dct1 = {'1': {'layer': 'Layer0',
           'material': 'm1',
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[258.27876653048702,
                       352.19351548063503,
                       -7.8617205266005193e-15],
                      [258.27876653048702,
                       122.943515480635,
                       -7.8617205266005193e-15],
                      [21.778766530487498,
                       122.943515480635,
                       -7.8617205266005193e-15],
                      [21.778766530487498,
                       352.19351548063503,
                       -7.8617205266005193e-15]]},
     '2': {'layer': 'Layer0',
           'material': 'None',
           'normal': [0.0, 0.0, -1.0],
           'parent': '1',
           'points': [[86.480314491428601,
                       261.94668598708699,
                       1.4937759579490601e-14],
                      [86.480314491428601,
                       191.94668598708699,
                       1.4937759579490601e-14],
                      [166.230314491429,
                       191.94668598708699,
                       1.4937759579490601e-14],
                      [166.230314491429,
                       261.94668598708699,
                       1.4937759579490601e-14]]},
     '3': {'layer': 'Layer0',
           'material': 'None',
           'normal': [0.0, 0.0, -1.0],
           'parent': '1',
           'points': [[238.25868364550999,
                       229.99000667216501,
                       1.9278664407190699e-14],
                      [238.25868364550999,
                       280.49000667216501,
                       1.9278664407190699e-14],
                      [194.75868364550999,
                       280.49000667216501,
                       1.9278664407190699e-14],
                      [194.75868364550999,
                       229.99000667216501,
                       1.9278664407190699e-14]]},
     '4': {'layer': 'Layer0',
           'material': 'm4',
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[86.480314491428601,
                       191.94668598708699,
                       1.4937759579490601e-14],
                      [86.480314491428601,
                       261.94668598708699,
                       1.4937759579490601e-14],
                      [166.230314491429,
                       261.94668598708699,
                       1.4937759579490601e-14],
                      [166.230314491429,
                       191.94668598708699,
                       1.4937759579490601e-14]]},
     '5': {'layer': 'Layer0',
           'material': 'm5',
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[238.25868364550999,
                       280.49000667216501,
                       1.9278664407190699e-14],
                      [238.25868364550999,
                       229.99000667216501,
                       1.9278664407190699e-14],
                      [194.75868364550999,
                       229.99000667216501,
                       1.9278664407190699e-14],
                      [194.75868364550999,
                       280.49000667216501,
                       1.9278664407190699e-14]]}}
    result1 = {'1': {'layer': 'Layer0',
           'material': 'm1',
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[258.27876653048702,
                       352.19351548063503,
                       -7.8617205266005193e-15],
                      [258.27876653048702,
                       122.943515480635,
                       -7.8617205266005193e-15],
                      [21.778766530487498,
                       122.943515480635,
                       -7.8617205266005193e-15],
                      [21.778766530487498,
                       352.19351548063503,
                       -7.8617205266005193e-15]]},
     '2': {'layer': 'Layer0',
           'material': 'm4',
           'normal': [0.0, 0.0, -1.0],
           'parent': '1',
           'points': [[86.480314491428601,
                       261.94668598708699,
                       1.4937759579490601e-14],
                      [86.480314491428601,
                       191.94668598708699,
                       1.4937759579490601e-14],
                      [166.230314491429,
                       191.94668598708699,
                       1.4937759579490601e-14],
                      [166.230314491429,
                       261.94668598708699,
                       1.4937759579490601e-14]]},
     '3': {'layer': 'Layer0',
           'material': 'm5',
           'normal': [0.0, 0.0, -1.0],
           'parent': '1',
           'points': [[238.25868364550999,
                       229.99000667216501,
                       1.9278664407190699e-14],
                      [238.25868364550999,
                       280.49000667216501,
                       1.9278664407190699e-14],
                      [194.75868364550999,
                       280.49000667216501,
                       1.9278664407190699e-14],
                      [194.75868364550999,
                       229.99000667216501,
                       1.9278664407190699e-14]]}}



class Inch2Meters_Data(object):
    dct = dct = {'1': {'layer': 'first',
           'material': 'None',
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]},
     '10': {'layer': 'second',
            'material': 'None',
            'normal': [-0.0, -1.0, -0.0],
            'parent': None,
            'points': [[10, 11, 12], [13, 14, 15], [16, 17, 18], [19, 20, 21]]}}
    meters_dct =     dct = {'1': {'layer': 'first',
           'material': 'None',
           'normal': [0.0, 0.0, -1.0],
           'parent': None,
           'points': [[0.025398760499999999, 0.050797520999999998, 0.07619628149999999],
            [0.101595042, 0.1269938025, 0.15239256299999998],
            [0.17779132349999999, 0.20319008399999999, 0.2285888445],
            [0.25398760500000001, 0.27938636550000001, 0.30478512599999996]]},
     '10': {'layer': 'second',
            'material': 'None',
            'normal': [-0.0, -1.0, -0.0],
            'parent': None,
            'points': [[0.25398760500000001, 0.27938636550000001, 0.30478512599999996],
             [0.33018388649999997, 0.35558264699999997, 0.38098140749999998],
             [0.40638016799999999, 0.43177892849999999, 0.457177689],
             [0.4825764495, 0.50797521000000001, 0.53337397050000002]]}}    

         