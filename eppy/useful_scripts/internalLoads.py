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
# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.

"""
I change the value and input method of internal load objects,
To specify a value of watts/SF for lighting or equipment
"""

import argparse
import sys


pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy.modeleditor import IDF

if __name__    == '__main__':
    # do the argparse stuff
    parser = argparse.ArgumentParser(usage=None, description=__doc__)
    parser.add_argument('idd', action='store', 
        help='location of idd file = ./somewhere/eplusv8-0-1.idd')
    parser.add_argument('simfile', action='store', 
        help='location of first with idf files = ./somewhere/f1.idf')
    nspace = parser.parse_args()
    iddfile = nspace.idd
    idffile = nspace.simfile
    # read the contents of the simulation file for manipulation
    IDF.setiddname(iddfile)
    idfcnts = IDF(idffile)
    idfobjs = idfcnts.idfobjects
    print idfobjs