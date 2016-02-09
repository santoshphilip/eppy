# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""legacy code from EPlusInterface"""








DOSSEP = '\r\n'
MACSEP = '\r'
UNIXSEP = '\n'

def getlinesep(astr):
    """returns the line seperators used in the string astr
    mac is '\r'
    dos is '\r\n'
    unix is '\n'"""
    lsep = None
    if len(astr) == 0:
        lsep = None
    # rcount = string.count(astr,'\r')
    rcount = astr.count('\r')
    # ncount = string.count(astr,'\n')
    ncount = astr.count('\n')
    # print("ncount, rcount", ncount, rcount)
    if ncount == rcount == 0:
        lsep = None
    if ncount == 0:
        lsep = '\r'
    if rcount == 0:
        lsep = '\n'
    if ncount == rcount:
        lsep = '\r\n'
    return lsep

