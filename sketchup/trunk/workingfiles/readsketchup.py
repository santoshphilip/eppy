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
Read the data that sketchup generates for energyplus
gives back the data into a dictionary
"""

try:
    set
except NameError:
    from sets import Set as set


def stripped(txt):
    """apply strip to all lines of a text file"""
    return '\n'.join([line.strip() for line in txt.splitlines()])

def readsketchup(txt):
    """read the data that sketchup generates for energyplus
    Convert it to a python dictionary"""
    lst = txt.split('face:')
    lst.pop(0)
    lst1 = [el.splitlines() for el in lst]
    [(el[0], '\n'.join(el[1:])) for el in lst1]
    dct = dict([(el[0], '\n'.join(el[1:])) for el in lst1])
    for name, val in dct.items():
        dct[name] = txt2face(val)
    return dct    

def txt2face(txt):
    """convert sketchup txt for one face to a face dictionary"""
    txt = stripped(txt)
    lst = [line.split(':') for line in txt.splitlines()]
    dct = dict([el for el in lst if len(el) == 2])
    ptslst = [el for el in lst if len(el) == 1]
    ptslst = [pt3[0].split()  for pt3 in ptslst]
    ptslst = [[float(pt) for pt in pt3] for pt3 in ptslst]
    dct['points'] = ptslst
    if dct['parent'] == 'None': 
        dct['parent'] = None
    if dct['material'] == 'None': 
        dct['material'] = None
    dct['normal'] = [float(el) for el in dct['normal'].split()]
    dct['surfacedirection'] = float(dct['surfacedirection'])
    return dct

def samepoly(p1, p2):
    """if the polygons poly1 and poly2 are identical: return True
    does not care aout the order of the points in the list
    as long as the same points are there it will return True"""
    p1 = [tuple(el) for el in p1]
    p2 = [tuple(el) for el in p2]
    s1 = set(p1)    
    s2 = set(p2) 
    return s1 == s2   

def duplicatewindows(dct):
    """remove the duplicate windows
    sketchup geneates two planes for the windows"""
    winkeys = [key for key in dct.keys() if dct[key]['parent'] != None]
    for ikey in winkeys:
        for jkey in dct.keys():
            if dct[jkey]['parent'] == None:
                if samepoly(dct[ikey]['points'], dct[jkey]['points']):
                    if dct[jkey]['material'] != None:
                        dct[ikey]['material'] = dct[jkey]['material']
                    dct.pop(jkey)
    return dct

def inch2meters(dct):
    """Sketchup dumps the dimensions in inches
    Convert it to meters"""
    converter = 0.0253987605
    for key in dct.keys():
        dct[key]['points'] = [[j * converter for j in i] for i in dct[key]['points']]
    return dct
        

    

def main():
    pass


if __name__ == '__main__':
    main()

