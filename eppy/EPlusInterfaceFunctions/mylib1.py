# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Legacy code from EPlusInterface"""
def write_str2file(pathname, astr):
    """writes a string to file"""
    fname = pathname
    fhandle = open(fname, 'wb')
    fhandle.write(astr)
    fhandle.close()

def readfile(pathname):
    """retrun the data in the file"""
    fhandle = open(pathname, 'rb')
    data = fhandle.read()
    try:
        data = data.decode('ISO-8859-2')
    except AttributeError:
        pass
    fhandle.close()
    return data

def readfileasmac():
    """docstring for readfileasmac"""
    return None