# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""just read the idf file"""
import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd
import eppy.EPlusInterfaceFunctions.eplusdata as eplusdata


def readidf(idfname):
    """read the idf file"""
    iddfile = 'Energy+.idd'
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block)
    data = eplusdata.Eplusdata(theidd, idfname)
    return data


def readiddidf(idfname):
    """read the idf file"""
    iddfile = 'Energy+.idd'
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block)
    data = eplusdata.Eplusdata(theidd, idfname)
    return theidd, data


def readiddstuff(idfname):
    """read the idf file"""
    iddfile = 'Energy+.idd'
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block)
    data = eplusdata.Eplusdata(theidd, idfname)
    return block, commlst, commdct


def readdatacommlst(idfname):
    """read the idf file"""
    iddfile = 'Energy+.idd'
    block, commlst, commdct = parse_idd.extractidddata(iddfile)

    theidd = eplusdata.Idd(block)
    data = eplusdata.Eplusdata(theidd, idfname)
    return data, commlst


def readdatacommdct(idfname, iddfile='Energy+.idd', commdct=None, idd_index=None):
    """read the idf file"""
    if not commdct:
        block, commlst, commdct, idd_index = parse_idd.extractidddata(iddfile)
        theidd = eplusdata.Idd(block)
    else:
        theidd = iddfile
    data = eplusdata.Eplusdata(theidd, idfname)
    return data, commdct, idd_index


def readdatacommdct1(idfname, iddfile='Energy+.idd', commdct=None, block=None, idd_index=None):
    """read the idf file"""
    if not commdct:
        block, commlst, commdct, idd_index = parse_idd.extractidddata(iddfile)
        theidd = eplusdata.Idd(block)
    else:
        theidd = eplusdata.Idd(block)
    data = eplusdata.Eplusdata(theidd, idfname)
    return block, data, commdct, idd_index
