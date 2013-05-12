"""just read the idf file"""

import sys
import getopt
import parse_idd
import eplusdata
# from EPlusInterfaceFunctions import parse_idd
# from EPlusInterfaceFunctions import eplusdata

def readidf(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block,commlst,commdct=parse_idd.extractidddata(iddfile)

    theidd=eplusdata.idd(block,2)
    data = eplusdata.eplusdata(theidd,idfname)
    return data


def readiddidf(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block,commlst,commdct=parse_idd.extractidddata(iddfile)

    theidd=eplusdata.idd(block,2)
    data = eplusdata.eplusdata(theidd,idfname)
    return theidd, data

def readiddstuff(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block,commlst,commdct=parse_idd.extractidddata(iddfile)

    theidd=eplusdata.idd(block,2)
    data = eplusdata.eplusdata(theidd,idfname)
    return block,commlst,commdct
    
    

def readdatacommlst(idfname):
    """read the idf file"""
    # iddfile = sys.path[0] + '/EplusCode/Energy+.idd'
    iddfile = 'Energy+.idd'
    # iddfile = './EPlusInterfaceFunctions/E1.idd' # TODO : can the path name be not hard coded
    iddtxt = open(iddfile, 'r').read()
    block,commlst,commdct=parse_idd.extractidddata(iddfile)

    theidd=eplusdata.idd(block,2)
    data = eplusdata.eplusdata(theidd,idfname)
    return data, commlst
    
def readdatacommdct(idfname, iddfile='Energy+.idd', commdct=None):
    """read the idf file"""
    if not commdct:
        block,commlst,commdct=parse_idd.extractidddata(iddfile)
        theidd=eplusdata.idd(block,2)
    else:
        theidd = iddfile
    data = eplusdata.eplusdata(theidd,idfname)
    return data, commdct
    
def readdatacommdct1(idfname, iddfile='Energy+.idd',
                                    commdct=None, block=None):
    """read the idf file"""
    if not commdct:
        block,commlst,commdct=parse_idd.extractidddata(iddfile)
        theidd=eplusdata.idd(block,2)
    else:
        theidd = eplusdata.idd(block,2)
    data = eplusdata.eplusdata(theidd,idfname)
    return block, data, commdct
