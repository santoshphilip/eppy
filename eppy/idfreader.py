# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""use epbunch"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from eppy.EPlusInterfaceFunctions import readidf
import eppy.bunchhelpers as bunchhelpers
from eppy.bunch_subclass import EpBunch
# from eppy.bunch_subclass import fieldnames, fieldvalues
import eppy.iddgaps as iddgaps
import eppy.function_helpers as fh
from eppy.idf_msequence import Idf_MSequence


def iddversiontuple(afile):
    """given the idd file or filehandle, return the version handle"""
    def versiontuple(vers):
        """version tuple"""
        return tuple([int(num) for num in vers.split(".")])
    try:
        fhandle = open(afile, 'rb')
    except TypeError:
        fhandle = afile
    line1 = fhandle.readline()
    try:
        line1 = line1.decode('ISO-8859-2')
    except AttributeError:
        pass
    line = line1.strip()
    if line1 == '':
        return (0,)
    vers = line.split()[-1]
    return versiontuple(vers)


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
    ddtt, dtls = data.dt, data.dtls
    for obj_i, key in enumerate(dtls):
        key = key.upper()
        bunchdt[key] = []
        objs = ddtt[key]
        for obj in objs:
            # if obj[0] == "Construction:WindowDataFile":
            #     print obj
            bobj = makeabunch(commdct, obj, obj_i)
            bunchdt[key].append(bobj)
    return bunchdt


def makebunches_alter(data, commdct, theidf):
    """make bunches with data"""
    bunchdt = {}
    dt, dtls = data.dt, data.dtls
    for obj_i, key in enumerate(dtls):
        key = key.upper()
        objs = dt[key]
        list1 = []
        for obj in objs:
            bobj = makeabunch(commdct, obj, obj_i)
            list1.append(bobj)
        bunchdt[key] = Idf_MSequence(list1, objs, theidf)
        # print "id(objs)", id(objs)
        # print "id(dt[key])", id(dt[key])
        # print "id(bunchdt[key].list2)", id(bunchdt[key].list2)
    return bunchdt


def convertfields(key_comm, obj):
    """convert the float and interger fields"""
    def apass(aaa):
        """pass thru"""
        return aaa
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
        except ValueError:
            pass
    return obj


def convertallfields(data, commdct):
    """docstring for convertallfields"""
    # import pdbdb; pdb.set_trace()
    for key in list(data.dt.keys()):
        objs = data.dt[key]
        for i, obj in enumerate(objs):
            key_i = data.dtls.index(key)
            key_comm = commdct[key_i]
            obj = convertfields(key_comm, obj)
            objs[i] = obj


def addfunctions(dtls, bunchdt):
    """add functions to the objects"""
    snames = [
        "BuildingSurface:Detailed",
        "Wall:Detailed",
        "RoofCeiling:Detailed",
        "Floor:Detailed",
        "FenestrationSurface:Detailed",
        "Shading:Site:Detailed",
        "Shading:Building:Detailed",
        "Shading:Zone:Detailed", ]
    for sname in snames:
        if sname.upper() in bunchdt:
            surfaces = bunchdt[sname.upper()]
            for surface in surfaces:
                func_dict = {
                    'area': fh.area,
                    'height': fh.height,  # not working correctly
                    'width': fh.width,  # not working correctly
                    'azimuth': fh.azimuth,
                    'tilt': fh.tilt,
                    'coords': fh.getcoords,  # needed for debugging
                }
                try:
                    surface.__functions.update(func_dict)
                except KeyError as e:
                    surface.__functions = func_dict
    # add common functions
    # for name in dtls:
    #     for idfobject in bunchdt[name]:
    # idfobject.__functions
    #         idfobject['__functions']['fieldnames'] = fieldnames
    #         idfobject['__functions']['fieldvalues'] = fieldvalues
    #         idfobject['__functions']['getrange'] = GetRange(idfobject)
    #         idfobject['__functions']['checkrange'] = CheckRange(idfobject)

def addfunctions2new(abunch, key):
    """add functions to a new bunch/munch object"""
    snames = [
        "BuildingSurface:Detailed",
        "Wall:Detailed",
        "RoofCeiling:Detailed",
        "Floor:Detailed",
        "FenestrationSurface:Detailed",
        "Shading:Site:Detailed",
        "Shading:Building:Detailed",
        "Shading:Zone:Detailed", ]
    snames = [sname.upper() for sname in snames]
    if key in snames:
        func_dict = {
            'area': fh.area,
            'height': fh.height,  # not working correctly
            'width': fh.width,  # not working correctly
            'azimuth': fh.azimuth,
            'tilt': fh.tilt,
            'coords': fh.getcoords,  # needed for debugging
        }
        try:
            abunch.__functions.update(func_dict)
        except KeyError as e:
            abunch.__functions = func_dict
    return abunch


def idfreader(fname, iddfile, conv=True):
    """read idf file and return bunches"""
    data, commdct, idd_index = readidf.readdatacommdct(fname, iddfile=iddfile)
    if conv:
        convertallfields(data, commdct)
    # fill gaps in idd
    ddtt, dtls = data.dt, data.dtls
    # skiplist = ["TABLE:MULTIVARIABLELOOKUP"]
    nofirstfields = iddgaps.missingkeys_standard(
        commdct, dtls,
        skiplist=["TABLE:MULTIVARIABLELOOKUP"])
    iddgaps.missingkeys_nonstandard(None, commdct, dtls, nofirstfields)
    bunchdt = makebunches(data, commdct)
    return bunchdt, data, commdct, idd_index


def idfreader1(fname, iddfile, theidf, conv=True, commdct=None, block=None):
    """read idf file and return bunches"""
    versiontuple = iddversiontuple(iddfile)
    # import pdb; pdb.set_trace()
    block, data, commdct, idd_index = readidf.readdatacommdct1(
        fname,
        iddfile=iddfile,
        commdct=commdct,
        block=block)
    if conv:
        convertallfields(data, commdct)
    # fill gaps in idd
    ddtt, dtls = data.dt, data.dtls
    if versiontuple < (8,):
        skiplist = ["TABLE:MULTIVARIABLELOOKUP"]
    else:
        skiplist = None
    nofirstfields = iddgaps.missingkeys_standard(
        commdct, dtls,
        skiplist=skiplist)
    iddgaps.missingkeys_nonstandard(block, commdct, dtls, nofirstfields)
    # bunchdt = makebunches(data, commdct)
    bunchdt = makebunches_alter(data, commdct, theidf)
    return bunchdt, block, data, commdct, idd_index, versiontuple
