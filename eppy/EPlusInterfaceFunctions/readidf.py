# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""just read the idf file"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd
import eppy.EPlusInterfaceFunctions.eplusdata as eplusdata
import eppy.EPlusInterfaceFunctions.iddgroups as iddgroups

# from EPlusInterfaceFunctions import parse_idd
# from EPlusInterfaceFunctions import eplusdata


def readidf(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = "Energy+.idd"
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, "r").read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return data


def readiddidf(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = "Energy+.idd"
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, "r").read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return theidd, data


def readiddstuff(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = "Energy+.idd"
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, "r").read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return block, commlst, commdct


def readdatacommlst(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = "Energy+.idd"
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, "r").read()
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block, 2)
    data = eplusdata.Eplusdata(theidd, idfname)
    return data, commlst


def readdatacommdct(idfname, iddfile="Energy+.idd", commdct=None):
    """read the idf file"""
    if not commdct:
        block, commlst, commdct, idd_index = parse_idd.extractidddata(iddfile)
        theidd = eplusdata.Idd(block, 2)
    else:
        theidd = iddfile
    data = eplusdata.Eplusdata(theidd, idfname)
    return data, commdct, idd_index


def readdatacommdct1(idfname, iddfile="Energy+.idd", commdct=None, block=None):
    """read the idf file"""
    if not commdct:
        block, commlst, commdct, idd_index = parse_idd.extractidddata(iddfile)
        theidd = eplusdata.Idd(block, 2)
    else:
        theidd = eplusdata.Idd(block, 2)
        idd_index = {}  # it should not get here :-(
    data = eplusdata.Eplusdata(theidd, idfname)
    return block, data, commdct, idd_index
