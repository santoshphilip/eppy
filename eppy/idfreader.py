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

from itertools import chain

from eppy.EPlusInterfaceFunctions import readidf
import eppy.bunchhelpers as bunchhelpers
from eppy.EPlusInterfaceFunctions.structures import CaseInsensitiveDict
from eppy.bunch_subclass import EpBunch

# from eppy.bunch_subclass import fieldnames, fieldvalues
import eppy.iddgaps as iddgaps
import eppy.function_helpers as fh
from eppy.idf_msequence import Idf_MSequence


class NoIDDFieldsError(Exception):
    pass


def iddversiontuple(afile):
    """given the idd file or filehandle, return the version handle"""

    def versiontuple(vers):
        """version tuple"""
        return tuple([int(num) for num in vers.split(".")])

    try:
        fhandle = open(afile, "rb")
    except TypeError:
        fhandle = afile
    line1 = fhandle.readline()
    try:
        line1 = line1.decode("ISO-8859-2")
    except AttributeError:
        pass
    line = line1.strip()
    if line1 == "":
        return (0,)
    vers = line.split()[-1]
    return versiontuple(vers)


def makeabunch(commdct, obj, obj_i, debugidd=True, block=None):
    """make a bunch from the object"""
    objidd = commdct[obj_i]
    objfields = [comm.get("field") for comm in commdct[obj_i]]
    objfields[0] = ["key"]
    objfields = [field[0] for field in objfields]
    obj_fields = [bunchhelpers.makefieldname(field) for field in objfields]
    bobj = EpBunch(obj, obj_fields, objidd)
    # TODO : test for len(obj) > len(obj_fields)
    # that will be missing fields in idd file
    # do we throw an exception here ????? YES !!!!!
    if debugidd:
        if len(obj) > len(obj_fields):
            n = len(obj) - len(obj_fields)
            extlst = extension_of_extensible(commdct[obj_i], block[obj_i], n)
            errortext = "idfobject with key '{}' & first field '{}' has {} fields while the idd for '{}' has only {} fields. Add the following fields to the object '{}' in file Energy+.idd '{};'".format(
                obj[0].upper(),
                obj[1],
                len(obj) - 1,
                obj[0].upper(),
                len(obj_fields) - 1,
                obj[0].upper(),
                ", ".join(extlst),
            )
            # "idfobject with key 'TIMESTEP' & first field '44' has 2 fields while the idd for 'TIMESTEP' has only 1 fields. Add the following fields to object 'TIMESTEP' in file Energy+.idd A5, A6;'"
            # print(block[obj_i])
            # print(errortext)
            print(extlst)
            raise NoIDDFieldsError(errortext)
    return bobj


def makebunches(data, commdct):
    """make bunches with data"""
    bunchdt = CaseInsensitiveDict()
    ddtt, dtls = data.dt, data.dtls
    for obj_i, key in enumerate(dtls):
        key = key.upper()
        bunchdt[key] = []
        objs = ddtt[key]
        for obj in objs:
            bobj = makeabunch(commdct, obj, obj_i)
            bunchdt[key].append(bobj)
    return bunchdt


def makebunches_alter(data, commdct, theidf, block=None):
    """make bunches with data"""
    bunchdt = CaseInsensitiveDict()
    dt, dtls = data.dt, data.dtls
    for obj_i, key in enumerate(dtls):
        key = key.upper()
        objs = dt[key]
        list1 = []
        for obj in objs:
            bobj = makeabunch(commdct, obj, obj_i, block=block)
            list1.append(bobj)
        bunchdt[key] = Idf_MSequence(list1, objs, theidf)
    return bunchdt


class ConvInIDD(object):
    """hold the conversion function to integer, real and no_type"""

    def no_type(self, x, avar):
        if avar.startswith("N"):  # is a number if it starts with N
            try:
                return float(x)  # in case x=autosize
            except ValueError as e:
                return x
        else:
            return x  # starts with A, is not a number

    def integer(self, x, y):
        try:
            return int(x)
        except ValueError as e:
            return x

    def real(self, x, y):
        try:
            return float(x)
        except ValueError as e:
            return x

    def conv_dict(self):
        """dictionary of conversion"""
        return dict(integer=self.integer, real=self.real, no_type=self.no_type)


# remove this one
def convertfields_old(key_comm, obj, inblock=None):
    """convert the float and interger fields"""
    convinidd = ConvInIDD()
    typefunc = dict(integer=convinidd.integer, real=convinidd.real)
    types = []
    for comm in key_comm:
        types.append(comm.get("type", [None])[0])
    convs = [typefunc.get(typ, convinidd.no_type) for typ in types]
    try:
        inblock = list(inblock)
    except TypeError as e:
        inblock = ["does not start with N"] * len(obj)
    for i, (val, conv, avar) in enumerate(zip(obj, convs, inblock)):
        if i == 0:
            # inblock[0] is the key
            pass
        else:
            val = conv(val, inblock[i])
        obj[i] = val
    return obj


def convertafield(field_comm, field_val, field_iddname):
    """convert field based on field info in IDD"""
    convinidd = ConvInIDD()
    field_typ = field_comm.get("type", [None])[0]
    conv = convinidd.conv_dict().get(field_typ, convinidd.no_type)
    return conv(field_val, field_iddname)


def convertfields(key_comm, obj, inblock=None):
    """convert based on float, integer, and A1, N1"""
    # f_ stands for field_
    convinidd = ConvInIDD()
    if not inblock:
        inblock = ["does not start with N"] * len(obj)
    for i, (f_comm, f_val, f_iddname) in enumerate(zip(key_comm, obj, inblock)):
        if i == 0:
            # inblock[0] is the iddobject key. No conversion here
            pass
        else:
            obj[i] = convertafield(f_comm, f_val, f_iddname)
    return obj


def convertallfields(data, commdct, block=None):
    """docstring for convertallfields"""
    # import pdbdb; pdb.set_trace()
    for key in list(data.dt.keys()):
        objs = data.dt[key]
        for i, obj in enumerate(objs):
            key_i = data.dtls.index(key)
            key_comm = commdct[key_i]
            try:
                inblock = block[key_i]
            except TypeError as e:
                inblock = None
            obj = convertfields(key_comm, obj, inblock)
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
        "Shading:Zone:Detailed",
    ]
    for sname in snames:
        if sname.upper() in bunchdt:
            surfaces = bunchdt[sname.upper()]
            for surface in surfaces:
                func_dict = {
                    "area": fh.area,
                    "height": fh.height,  # not working correctly
                    "width": fh.width,  # not working correctly
                    "azimuth": fh.azimuth,
                    "tilt": fh.tilt,
                    "coords": fh.getcoords,  # needed for debugging
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
        "Shading:Zone:Detailed",
    ]
    snames = [sname.upper() for sname in snames]
    if key in snames:
        func_dict = {
            "area": fh.area,
            "height": fh.height,  # not working correctly
            "width": fh.width,  # not working correctly
            "azimuth": fh.azimuth,
            "tilt": fh.tilt,
            "coords": fh.getcoords,  # needed for debugging
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
        commdct, dtls, skiplist=["TABLE:MULTIVARIABLELOOKUP"]
    )
    iddgaps.missingkeys_nonstandard(None, commdct, dtls, nofirstfields)
    bunchdt = makebunches(data, commdct)
    return bunchdt, data, commdct, idd_index


def idfreader1(fname, iddfile, theidf, conv=True, commdct=None, block=None):
    """read idf file and return bunches"""
    versiontuple = iddversiontuple(iddfile)
    # import pdb; pdb.set_trace()
    block, data, commdct, idd_index = readidf.readdatacommdct1(
        fname, iddfile=iddfile, commdct=commdct, block=block
    )
    if conv:
        convertallfields(data, commdct, block)
    # fill gaps in idd
    ddtt, dtls = data.dt, data.dtls
    if versiontuple < (8,):
        skiplist = ["TABLE:MULTIVARIABLELOOKUP"]
    else:
        skiplist = None
    nofirstfields = iddgaps.missingkeys_standard(commdct, dtls, skiplist=skiplist)
    iddgaps.missingkeys_nonstandard(block, commdct, dtls, nofirstfields)
    # bunchdt = makebunches(data, commdct)
    bunchdt = makebunches_alter(data, commdct, theidf, block)
    return bunchdt, block, data, commdct, idd_index, versiontuple


def getextensible(objidd):
    """return the extensible from the idd"""
    keys = objidd[0].keys()
    extkey = [key for key in keys if key.startswith("extensible")]
    if extkey:
        extens = extkey[0].split(":")[-1]
        return int(extens)
    else:
        return None


def endof_extensible(extensible, thisblock):
    """get the vars from where extension happens"""
    return thisblock[-extensible:]


def extension_of_extensible(objidd, objblock, n):
    """generate the list of new vars needed to extend by n"""
    ext = getextensible(objidd)
    print(n, type(n), ext, type(ext))
    # n = int(n / ext)
    n = n // ext
    print(n, type(n))
    lastvars = endof_extensible(ext, objblock)
    print("ext, lastvars", ext, lastvars)
    alpha_lastvars = [i[0] for i in lastvars]
    int_lastvars = [int(i[1:]) for i in lastvars]
    lst = []
    for alpha, start in zip(alpha_lastvars, int_lastvars):
        step = alpha_lastvars.count(alpha)
        rng = range(start + step, start + 1 + n * step, step)
        lst.append(["{}{}".format(alpha, item) for item in rng])

    from itertools import chain

    return list(chain(*zip(*lst)))


# complete -- remove this junk below
# working code - working on it now.
# N3, A4, M8, A5
#
# N3, A4, M8, A5
# N4, A6, M9, A7
# N5, A8, M10, A9
# N6, A10, M11, A11


# ref = idf1.newidfobject("Refrigeration:WalkIn".upper())
# lastvars = ["N3", "A4", "M8", "A5"]
# lastvars = [u'A18',
#  u'N29',
#  u'N30',
#  u'N31',
#  u'N32',
#  u'N33',
#  u'A19',
#  u'N34',
#  u'N35',
#  u'N36',
#  u'A20',
#  u'A21']
# alpha_lastvars = [i[0] for i in lastvars]
# int_lastvars = [int(i[1:]) for i in lastvars]
#
#
#
# n = 2
#
# lst = []
# for alpha, start in zip(alpha_lastvars, int_lastvars):
#     step = alpha_lastvars.count(alpha)
#     rng = range(start +1, start + 1 + n * step, step)
#     lst.append(["{}{}".format(alpha, item) for item in rng])
#
# from itertools import chain
# c = list(chain(*zip(*lst)))
#
#
