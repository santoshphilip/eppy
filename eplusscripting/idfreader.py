# Copyright (c) 2012 Santosh Phillip

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

"""use epbunch"""

from EPlusInterfaceFunctions import readidf
import bunchhelpers
from bunch_subclass import EpBunch
import iddgaps
import function_helpers as fh

def makeabunch(commdct, obj, obj_i):
    """make a bunch from the object"""
    objfields = [comm.get('field') for comm in commdct[obj_i]]
    objfields[0] = ['key']
    objfields = [field[0] for field in objfields]
    obj_fields = [bunchhelpers.makefieldname(field) for field in objfields]
    bobj = EpBunch(obj, obj_fields)
    return bobj

def makebunches(data, commdct):
    """make bunches with data"""
    bunchdt = {}
    dt, dtls = data.dt, data.dtls
    for obj_i, key in enumerate(dtls):
        key = key.upper()
        bunchdt[key] = []
        objs = dt[key]
        for obj in objs:
            bobj = makeabunch(commdct, obj, obj_i)
            bunchdt[key].append(bobj)
    return bunchdt

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
            
def addfunctions(bunchdt):
    """add functions to the objects"""
    snames = ["BuildingSurface:Detailed",
    "Wall:Detailed",
    "RoofCeiling:Detailed",
    "Floor:Detailed",
    "FenestrationSurface:Detailed",
    "Shading:Site:Detailed",
    "Shading:Building:Detailed",
    "Shading:Zone:Detailed",]
    for sname in snames:
        if bunchdt.has_key(sname.upper()):
            surfaces = bunchdt[sname.upper()]
            for surface in surfaces:
                surface.__functions = {'area':fh.area,
                    # 'height':fh.height, # not working correctly
                    # 'width':fh.width, # not working correctly
                    'azimuth':fh.azimuth,
                    'tilt':fh.tilt,
                    # 'coords':fh.getcoords, # needed for debugging
                    } 
            

def idfreader(fname, iddfile, conv=True):
    """read idf file and reutrn bunches"""
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
    if conv:
        convertallfields(data, commdct)
    # fill gaps in idd
    dt, dtls = data.dt, data.dtls
    nofirstfields = iddgaps.missingkeys_standard(commdct, dtls, 
                skiplist=["TABLE:MULTIVARIABLELOOKUP"]) 
    iddgaps.missingkeys_nonstandard(commdct, dtls, nofirstfields)
    bunchdt = makebunches(data, commdct)
    # TODO : add functions here.
    # - 
    addfunctions(bunchdt)
    # - 
    return bunchdt, data, commdct

class IDF0(object):
    iddname = None
    def __init__(self, idfname):
        self.idfname = idfname
        self.read()
    @classmethod
    def setiddname(cls, arg):
        if cls.iddname == None:
            cls.iddname = arg
    def read(self):
        """read the idf file"""
        # TODO : thow an exception if iddname = None
        self.objects, model, idd_info = idfreader(self.idfname, self.iddname)

class IDF1(IDF0):
    def __init__(self, idfname):
        super(IDF, self).__init__(idfname)
        
# read code
# iddfile = "../iddfiles/Energy+V6_0.idd"
# fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # small file with only surfaces
# bunchdt, data, commdct = idfreader(fname, iddfile)
# 
# zones = bunchdt['zone'.upper()]
# surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()]
# currentobjs = [key for key in bunchdt.keys() if len(bunchdt[key]) > 0]
# 
# print data