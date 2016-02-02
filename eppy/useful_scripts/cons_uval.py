# Copyright (c) 2015 Eric Youngson

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
# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.

"""
Select a construction and find the overall U-Vale
"""

import argparse

from eppy import modeleditor
from eppy.modeleditor import IDF
import redict_subclass

import pprint
import re
import itertools


def select_cons(simfile, construction):
    try:
        IDF.setiddname('/Applications/EnergyPlus-8-1-0/Energy+.idd')
    except modeleditor.IDDAlreadySetError as e:
        pass

    simFile = IDF(simfile)
    
    idfObjs = simFile.idfobjects
    idfRedict = redict(idfObjs)
    regexMatsLst = [objls for objls in [objtyp for objtyp in
                    idfRedict[r'^MATERIAL.*']] if objls]
    regexMats = list(itertools.chain.from_iterable(regexMatsLst))
    cns = idfObjs[construction]
    
    keys = [cn.Name for cn in cns]
    
    values = [cn for cn in cns]
    cnsDct = dict(zip(keys, values ))
    
    nonres_ext_wall_CNS = cnsDct['90.1-2007 Nonres 4B Ext Wall Steel-Framed']
    nonres_ext_wall_LYRs = nonres_ext_wall_CNS.fieldvalues[2:]
    nonres_ext_wall_MATs = [mat for mat in regexMats if mat.Name in
                            nonres_ext_wall_LYRs]
    
    return nonres_ext_wall_MATs
