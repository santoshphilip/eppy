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

"""do a type conversion for all variables in data.dt"""
from EPlusInterfaceFunctions import readidf

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
 
def convertfields(key_comm, obj):
    """convert the float and interger fields"""
    def apass(a):
        return a
    typefunc = dict(integer=int, real=float)
    types = [comm.get('type', [None])[0] for comm in key_comm]
    convs = [typefunc.get(typ, apass) for typ in types]
    for i, (val, conv) in enumerate(zip(obj, convs)):
        try:
            val = conv(val)
            obj[i] = val
        except ValueError, e:
            pass
    return obj
    
def convertallfields(data, commdct):
    """docstring for convertallfields"""
    for key in data.dt.keys():
        objs = data.dt[key]
        for i, obj in enumerate(objs):
            key_i = data.dtls.index(key)
            key_comm = commdct[key_i]
            obj = convertfields(key_comm, obj)
            objs[i] = obj

def test_convertfields():
    """py.test for convertfields"""
    obj = ['Zone', 'PLENUM-1', "0.0", "0.0", "0.0", "0.0", "1", "1", "0.5", 
        "280"]
    newobj = ['Zone', 'PLENUM-1', 0.0, 0.0, 0.0, 0.0, 1, 1, 0.5, 
        280.0]
    dt = data.dt
    dtls = data.dtls
    key = 'zone'.upper()
    key_i = dtls.index(key)
    key_comm = commdct[key_i]
    obj = convertfields(key_comm, obj)
    assert newobj == obj
    
    
txt = str(data)
open('a.txt', 'w').write(txt)
convertallfields(data, commdct)
txt = str(data)
open('b.txt', 'w').write(txt)
