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

"""use epbunch"""

from EPlusInterfaceFunctions import readidf
import bunchhelpers
from bunch_subclass import EpBunch
from bunch_subclass import fieldnames, fieldvalues, GetRange, CheckRange
import iddgaps
import function_helpers as fh

def iddversiontuple(afile):
    """given the idd file or filehandle, return the version handle"""
    def versiontuple(v):
        return tuple(map(int, (v.split("."))))
    if type(afile) == str:
        fhandle = open(afile, 'r')
    else:
        fhandle = afile
    line1 = fhandle.readline()
    line = line1.strip()
    if line1 == '':
        return (0, )
    v = line.split()[-1]
    return versiontuple(v)
    

def makeabunch(commdct, obj, obj_i):
    """make a bunch from the object"""
    objidd = commdct[obj_i]
    objfields = [comm.get('field') for comm in commdct[obj_i]]
    objfields[0] = ['key']
    objfields = [field[0] for field in objfields]
    obj_fields = [bunchhelpers.makefieldname(field) for field in objfields]
    bobj = EpBunch(obj, obj_fields, objidd)
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
            # if obj[0] == "Construction:WindowDataFile":
            #     print obj
            bobj = makeabunch(commdct, obj, obj_i)
            bunchdt[key].append(bobj)
    return bunchdt

def convertfields(key_comm, obj):
    """convert the float and interger fields"""
    def apass(a):
        return a
    typefunc = dict(integer=int, real=float)
    # types = [comm.get('type', [None])[0] for comm in key_comm]
    types = []
    for comm in key_comm:
        types.append(comm.get('type', [None])[0])
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
            
def addfunctions(dtls, bunchdt):
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
                    'height':fh.height, # not working correctly
                    'width':fh.width, # not working correctly
                    'azimuth':fh.azimuth,
                    'tilt':fh.tilt,
                    'coords':fh.getcoords, # needed for debugging
                    } 
    # add common functions
    # for name in dtls:
    #     for idfobject in bunchdt[name]:
    #         # idfobject.__functions 
    #         idfobject['__functions']['fieldnames'] = fieldnames
    #         idfobject['__functions']['fieldvalues'] = fieldvalues
    #         idfobject['__functions']['getrange'] = GetRange(idfobject)
    #         idfobject['__functions']['checkrange'] = CheckRange(idfobject)
        
            

def idfreader(fname, iddfile, conv=True):
    """read idf file and reutrn bunches"""
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
    if conv:
        convertallfields(data, commdct)
    # fill gaps in idd
    dt, dtls = data.dt, data.dtls
    # skiplist = ["TABLE:MULTIVARIABLELOOKUP"]
    nofirstfields = iddgaps.missingkeys_standard(commdct, dtls, 
                skiplist=["TABLE:MULTIVARIABLELOOKUP"]) 
    iddgaps.missingkeys_nonstandard(commdct, dtls, nofirstfields)
    bunchdt = makebunches(data, commdct)
    # TODO : add functions here.
    # - 
    addfunctions(dtls, bunchdt)
    # - 
    return bunchdt, data, commdct

def idfreader1(fname, iddfile, conv=True, commdct=None, block=None):
    """read idf file and reutrn bunches"""
    versiontuple = iddversiontuple(iddfile)
    block, data, commdct = readidf.readdatacommdct1(fname,
                                iddfile=iddfile, commdct=commdct, block=block)
    if conv:
        convertallfields(data, commdct)
    # fill gaps in idd
    dt, dtls = data.dt, data.dtls
    if versiontuple < (8, ):
        skiplist = ["TABLE:MULTIVARIABLELOOKUP"]
    else:
        skiplist = None
    nofirstfields = iddgaps.missingkeys_standard(commdct, dtls, 
                skiplist=skiplist) 
    iddgaps.missingkeys_nonstandard(commdct, dtls, nofirstfields)
    bunchdt = makebunches(data, commdct)
    # TODO : add functions here.
    # - 
    addfunctions(dtls, bunchdt)
    # - 
    return bunchdt, block, data, commdct

# class IIDF0(object):
#     iddname = None
#     def __init__(self, idfname):
#         self.idfname = idfname
#         self.read()
#     @classmethod
#     def setiddname(cls, arg):
#         if cls.iddname == None:
#             cls.iddname = arg
#             cls.idd_info = None
#             cls.block = None
#     @classmethod
#     def setidd(cls, iddinfo, block):
#         cls.idd_info = iddinfo
#         cls.block = block
#     def read(self):
#         """read the idf file"""
#         # TODO unit test
#         # TODO : thow an exception if iddname = None
#         readout = idfreader1(self.idfname, self.iddname,
#                                 commdct=self.idd_info, block=self.block)
#         self.idfobjects, block, self.model, idd_info = readout
#         self.__class__.setidd(idd_info, block)
#     def save(self):
#         # TODO unit test
#         s = str(self.model)
#         open(self.idfname, 'w').write(s)
#     def saveas(self, filename):
#         s = str(self.model)
#         open(filename, 'w').write(s)
# 
# class IIDF1(IIDF0):
#     def __init__(self, idfname):
#         super(IIDF1, self).__init__(idfname)
#     def newidfobject(self, key, aname=''):
#         """add a new idfobject to the model"""
#         # TODO unit test
#         return addobject(self.idfobjects,
#                             self.model,
#                             self.idd_info,
#                             key, aname=aname)  
#     def addidfobject(self, idfobject):
#         """add idfobject to this model"""
#         # TODO unit test
#         addthisbunch(self.model,
#                             self.idd_info,
#                             idfobject)  
# class IIDF2(IIDF1):
#     def __init__(self, idfname):
#         super(IIDF2, self).__init__(idfname)
#     def idfstr(self):
#         # print self.model.__repr__()
#         st = ''
#         dtls = self.model.dtls
#         for objname in dtls:
#             for obj in self.idfobjects[objname]:
#                  st = st + obj.__repr__()
#         return st
#     def printidf(self):
#         """print the idf"""
#         s = self.idfstr()
#         dtls = self.model.dtls
#         for objname in dtls:
#             for obj in self.idfobjects[objname]:
#                  print obj
#     # def __repr__(self):
#     #     return self.model.__repr__()
# 
# IIDF = IIDF2

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