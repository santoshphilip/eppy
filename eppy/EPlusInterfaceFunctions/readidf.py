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
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""just read the idf file"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals



import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd
import eppy.EPlusInterfaceFunctions.eplusdata as eplusdata

# from EPlusInterfaceFunctions import parse_idd
# from EPlusInterfaceFunctions import eplusdata

def readidf(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return data


def readiddidf(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return theidd, data

def readiddstuff(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return block, commlst, commdct



def readdatacommlst(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return data, commlst

def readdatacommdct(idfname, iddfile='Energy+.idd', commdct=None):
    """read the idf file"""
    if not commdct:
        block, commlst, commdct = parse_idd.extractidddata(iddfile)
        theidd = eplusdata.Idd(block, 2)
    else:
        theidd = iddfile
    data = eplusdata.Eplusdata(theidd, idfname)
    return data, commdct

def readdatacommdct1(
        idfname, iddfile='Energy+.idd',
        commdct=None, block=None):
    """read the idf file"""
    if not commdct:
        block, commlst, commdct = parse_idd.extractidddata(iddfile)
        theidd = eplusdata.Idd(block, 2)
    else:
        theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return block, data, commdct
