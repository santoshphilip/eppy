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



"""testing to see in what order the points in sketchup are given
Results: Right hand corkscrew in the direction of the normal"""

from Scientific.Geometry import Vector
import readsketchup
import geometry

txt = open('e.txt', 'r').read()
dct = readsketchup.readsketchup(txt)
for key in dct.keys():
    plane = dct[key]['points']
    normal = Vector(dct[key]['normal'])
    calcnormal = geometry.facenormal(plane)
    # print normal
    # print calcnormal
    print normal.angle(calcnormal)
    print
    