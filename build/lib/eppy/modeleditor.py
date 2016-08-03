# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""functions to edit the E+ model"""






from io import StringIO
import copy
from eppy.iddcurrent import iddcurrent
from eppy.idfreader import idfreader1
from eppy.idfreader import makeabunch
import itertools
import os
import platform

from py._log import warning

import eppy.function_helpers as function_helpers


class NoObjectError(Exception):

    """Exception Object"""
    pass


class NotSameObjectError(Exception):

    """Exception Object"""
    pass


class IDDNotSetError(Exception):

    """Exception Object"""
    pass


class IDDAlreadySetError(Exception):

    """Exception Object"""
    pass


def almostequal(first, second, places=7, printit=True):
    """
    Test if two values are equal to a given number of places.
    This is based on python's unittest so may be covered by Python's 
    license.

    """
    if first == second:
        return True

    if round(abs(second - first), places) != 0:
        if printit:
            print(round(abs(second - first), places))
            print("notalmost: %s != %s to %i places" % (first, second, places))
        return False
    else:
        return True


def poptrailing(lst):
    """Remove trailing blank items from lst.
    """
    while lst and lst[-1] == '':
        lst.pop()
    return lst


def extendlist(lst, i, value=''):
    """extend the list so that you have i-th value"""
    if i == None:
        pass
    elif i < len(lst):
        pass
    else:
        lst.extend([value, ] * (i - len(lst) + 1))


def newrawobject(data, commdct, key):
    """Make a new object for the given key.

    Parameters
    ----------
    data : Eplusdata object
        Data dictionary and list of objects for the entire model.
    commdct : list of dicts
        Comments from the IDD file describing each item type in `data`.
    key : str
        Object type of the object to add (in ALL_CAPS).

    Returns
    -------
    list
        A list of field values for the new object.

    """
    dtls = data.dtls
    key = key.upper()

    key_i = dtls.index(key)
    key_comm = commdct[key_i]
    # set default values
    obj = [comm.get('default', [''])[0] for comm in key_comm]
    for i, comm in enumerate(key_comm):
        typ = comm.get('type', [''])[0]
        if typ in ('real', 'integer'):
            func_select = dict(real=float, integer=int)
            try:
                obj[i] = func_select[typ](obj[i])
            except IndexError:
                break
            except ValueError:  # if value = autocalculate
                continue
    obj[0] = key
    obj = poptrailing(obj)  # remove the blank items in a repeating field.
    return obj


def addthisbunch(bunchdt, data, commdct, thisbunch):
    """add a bunch to model.
    abunch usually comes from another idf file
    or it can be used to copy within the idf file"""
    key = thisbunch.key.upper()
    obj = copy.copy(thisbunch.obj)
    abunch = obj2bunch(data, commdct, obj)
    bunchdt[key].append(abunch)
    return abunch


def obj2bunch(data, commdct, obj):
    """make a new bunch object using the data object"""
    dtls = data.dtls
    key = obj[0].upper()
    key_i = dtls.index(key)
    abunch = makeabunch(commdct, obj, key_i)
    return abunch


def namebunch(abunch, aname):
    """give the bunch object a name, if it has a Name field"""
    if abunch.Name == None:
        pass
    else:
        abunch.Name = aname
    return abunch


def addobject(bunchdt, data, commdct, key, aname=None, **kwargs):
    """add an object to the eplus model"""
    obj = newrawobject(data, commdct, key)
    abunch = obj2bunch(data, commdct, obj)
    if aname:
        namebunch(abunch, aname)
    data.dt[key].append(obj)
    bunchdt[key].append(abunch)
    for key, value in list(kwargs.items()):
        abunch[key] = value
    return abunch


def getnamedargs(*args, **kwargs):
    """allows you to pass a dict and named args
    so you can pass ({'a':5, 'b':3}, c=8) and get
    dict(a=5, b=3, c=8)"""
    adict = {}
    for arg in args:
        if isinstance(arg, dict):
            adict.update(arg)
    adict.update(kwargs)
    return adict


def addobject1(bunchdt, data, commdct, key, **kwargs):
    """add an object to the eplus model"""
    obj = newrawobject(data, commdct, key)
    abunch = obj2bunch(data, commdct, obj)
    data.dt[key].append(obj)
    bunchdt[key].append(abunch)
    # adict = getnamedargs(*args, **kwargs)
    for kkey, value in kwargs.items():
        abunch[kkey] = value
    return abunch


def getobject(bunchdt, key, name):
    """get the object if you have the key and the name
    returns a list of objects, in case you have more than one
    You should not have more than one"""
    # TODO : throw exception if more than one object, or return more objects
    idfobjects = bunchdt[key]
    if idfobjects:
        # second item in list is a unique ID
        unique_id = idfobjects[0].objls[1]
    theobjs = [idfobj for idfobj in idfobjects if
               idfobj[unique_id].upper() == name.upper()]
    try:
        return theobjs[0]
    except IndexError:
        return None


def __objecthasfields(bunchdt, data, commdct, idfobject, places=7, **kwargs):
    """test if the idf object has the field values in kwargs"""
    for key, value in list(kwargs.items()):
        if not isfieldvalue(
                bunchdt, data, commdct,
                idfobject, key, value, places=places):
            return False
    return True


def getobjects(bunchdt, data, commdct, key, places=7, **kwargs):
    """get all the objects of key that matches the fields in **kwargs"""
    idfobjects = bunchdt[key]
    allobjs = []
    for obj in idfobjects:
        if __objecthasfields(
                bunchdt, data, commdct,
                obj, places=places, **kwargs):
            allobjs.append(obj)
    return allobjs


def iddofobject(data, commdct, key):
    """from commdct, return the idd of the object key"""
    dtls = data.dtls
    i = dtls.index(key)
    return commdct[i]


def getextensibleindex(bunchdt, data, commdct, key, objname):
    """get the index of the first extensible item"""
    theobject = getobject(bunchdt, key, objname)
    if theobject == None:
        return None
    theidd = iddofobject(data, commdct, key)
    extensible_i = [
        i for i in range(len(theidd)) if 'begin-extensible' in theidd[i]]
    try:
        extensible_i = extensible_i[0]
    except IndexError:
        return theobject


def removeextensibles(bunchdt, data, commdct, key, objname):
    """remove the extensible items in the object"""
    theobject = getobject(bunchdt, key, objname)
    if theobject == None:
        return theobject
    theidd = iddofobject(data, commdct, key)
    extensible_i = [
        i for i in range(len(theidd)) if 'begin-extensible' in theidd[i]]
    try:
        extensible_i = extensible_i[0]
    except IndexError:
        return theobject
    while True:
        try:
            popped = theobject.obj.pop(extensible_i)
        except IndexError:
            break
    return theobject


def getfieldcomm(bunchdt, data, commdct, idfobject, fieldname):
    """get the idd comment for the field"""
    key = idfobject.obj[0].upper()
    keyi = data.dtls.index(key)
    fieldi = idfobject.objls.index(fieldname)
    thiscommdct = commdct[keyi][fieldi]
    return thiscommdct


def is_retaincase(bunchdt, data, commdct, idfobject, fieldname):
    """test if case has to be retained for that field"""
    thiscommdct = getfieldcomm(bunchdt, data, commdct, idfobject, fieldname)
    return 'retaincase' in thiscommdct


def isfieldvalue(bunchdt, data, commdct, idfobj, fieldname, value, places=7):
    """test if idfobj.field == value"""
    # do a quick type check
    # if type(idfobj[fieldname]) != type(value):
    # return False # takes care of autocalculate and real
    # check float
    thiscommdct = getfieldcomm(bunchdt, data, commdct, idfobj, fieldname)
    if 'type' in thiscommdct:
        if thiscommdct['type'][0] in ('real', 'integer'):
            # test for autocalculate
            try:
                if idfobj[fieldname].upper() == 'AUTOCALCULATE':
                    if value.upper() == 'AUTOCALCULATE':
                        return True
            except AttributeError:
                pass
            return almostequal(float(idfobj[fieldname]), float(value), places, False)
    # check retaincase
    if is_retaincase(bunchdt, data, commdct, idfobj, fieldname):
        return idfobj[fieldname] == value
    else:
        return idfobj[fieldname].upper() == value.upper()


def equalfield(bunchdt, data, commdct, idfobj1, idfobj2, fieldname, places=7):
    """returns true if the two fields are equal
    will test for retaincase
    places is used if the field is float/real"""
    # TODO test if both objects are of same type
    key1 = idfobj1.obj[0].upper()
    key2 = idfobj2.obj[0].upper()
    if key1 != key2:
        raise NotSameObjectError
    vee2 = idfobj2[fieldname]
    return isfieldvalue(
        bunchdt, data, commdct,
        idfobj1, fieldname, vee2, places=places)


def getrefnames(idf, objname):
    """get the reference names for this object"""
    iddinfo = idf.idd_info
    dtls = idf.model.dtls
    index = dtls.index(objname)
    fieldidds = iddinfo[index]
    for fieldidd in fieldidds:
        if 'field' in fieldidd:
            if fieldidd['field'][0].endswith('Name'):
                if 'reference' in fieldidd:
                    return fieldidd['reference']
                else:
                    return []


def getallobjlists(idf, refname):
    """get all object-list fields for refname
    return a list:
    [('OBJKEY', refname, fieldindexlist), ...] where
    fieldindexlist = index of the field where the object-list = refname
    """
    dtls = idf.model.dtls
    objlists = []
    for i, fieldidds in enumerate(idf.idd_info):
        indexlist = []
        for j, fieldidd in enumerate(fieldidds):
            if 'object-list' in fieldidd:
                if fieldidd['object-list'][0].upper() == refname.upper():
                    indexlist.append(j)
        if indexlist != []:
            objkey = dtls[i]
            objlists.append((objkey, refname, indexlist))
    return objlists


def rename(idf, objkey, objname, newname):
    """rename all the refrences to this objname"""
    refnames = getrefnames(idf, objkey)
    for refname in refnames:
        objlists = getallobjlists(idf, refname)
        # [('OBJKEY', refname, fieldindexlist), ...]
        for refname in refnames:
            for robjkey, refname, fieldindexlist in objlists:
                idfobjects = idf.idfobjects[robjkey]
                for idfobject in idfobjects:
                    for findex in fieldindexlist:  # for each field
                        if idfobject[idfobject.objls[findex]] == objname:
                            idfobject[idfobject.objls[findex]] = newname
    theobject = idf.getobject(objkey, objname)
    fieldname = [item for item in theobject.objls if item.endswith('Name')][0]
    theobject[fieldname] = newname
    return theobject


def zonearea(idf, zonename, debug=False):
    """zone area"""
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    if debug:
        print(len(floors))
        print([floor.area for floor in floors])
    # area = sum([floor.area for floor in floors])
    if floors != []:
        area = zonearea_floor(idf, zonename)
    else:
        area = zonearea_roofceiling(idf, zonename)
    return area


def zonearea_floor(idf, zonename, debug=False):
    """zone area - floor"""
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    if debug:
        print(len(floors))
        print([floor.area for floor in floors])
    area = sum([floor.area for floor in floors])
    return area


def zonearea_roofceiling(idf, zonename, debug=False):
    """zone area - roof, ceiling"""
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs
              if s.Surface_Type.upper() in ['ROOF', 'CEILING']]
    if debug:
        print(len(floors))
        print([floor.area for floor in floors])
    area = sum([floor.area for floor in floors])
    return area


def zone_height_min2max(idf, zonename, debug=False):
    """zone height = max-min"""
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    surf_xyzs = [function_helpers.getcoords(s) for s in zone_surfs]
    surf_xyzs = list(itertools.chain(*surf_xyzs))
    surf_zs = [z for x, y, z in surf_xyzs]
    topz = max(surf_zs)
    botz = min(surf_zs)
    height = topz - botz
    return height


def zoneheight(idf, zonename, debug=False):
    """zone height"""
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == 'ROOF']
    if floors == [] or roofs == []:
        height = zone_height_min2max(idf, zonename)
    else:
        height = zone_floor2roofheight(idf, zonename)
    return height


def zone_floor2roofheight(idf, zonename, debug=False):
    """zone floor to roof height"""
    zone = idf.getobject('ZONE', zonename)
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == 'ROOF']
    ceilings = [s for s in zone_surfs if s.Surface_Type.upper() == 'CEILING']
    topsurfaces = roofs + ceilings

    topz = []
    for topsurface in topsurfaces:
        for coord in topsurface.coords:
            topz.append(coord[-1])
    topz = max(topz)

    botz = []
    for floor in floors:
        for coord in floor.coords:
            botz.append(coord[-1])
    botz = min(botz)
    height = topz - botz

    return height


def zonevolume(idf, zonename):
    """zone volume"""
    area = zonearea(idf, zonename)
    height = zoneheight(idf, zonename)
    volume = area * height

    return volume


class IDF(object):

    """
    The IDF class holds all the information about an EnergyPlus IDF. 

    Class attributes
    ---------------
    iddname : str
        Name of the IDD currently being used by eppy. As a class attribute, this
        is set for all IDFs which are currently being processed and cannot be 
        changed for an individual IDF.
    iddinfo : list
        Comments and metadata about fields in the IDD.
    block : list
        Field names in the IDD.

    Instance attributes
    -------------------
    idfname : str
        Path to the IDF file.
    idfobjects : list
        List of EpBunch objects in the IDF.
    model : Eplusdata object
        Data dictionary and list of objects for the entire model.
    outputtype : str
        How to format the output of IDF.print or IDF.save, IDF.saveas or
        IDF.savecopy. The options are: 'standard', 'nocomment', 'nocomment1',
        'nocomment2', and 'compressed'.

    """
    iddname = None
    idd_info = None
    block = None

    def __init__(self, idfname=None):
        """
        Parameters
        ----------
        idf_name : str, optional
            Path to an IDF file (which does not have to exist yet).

        """
        if idfname != None:
            self.idfname = idfname
            self.read()
        self.outputtype = "standard"

    """ Methods to set up the IDD."""
    @classmethod
    def setiddname(cls, iddname, testing=False):
        """
        Set the path to the EnergyPlus IDD for the version of EnergyPlus which
        is to be used by eppy.

        Parameters
        ----------
        iddname : str
            Path to the IDD file.
        testing : bool
            Flag to use if running tests since we may want to ignore the
            `IDDAlreadySetError`.

        Raises
        ------
        IDDAlreadySetError

        """
        if cls.iddname == None:
            cls.iddname = iddname
            cls.idd_info = None
            cls.block = None
        elif cls.iddname == iddname:
            pass
        else:
            if testing == False:
                errortxt = "IDD file is set to: %s" % (cls.iddname, )
                raise IDDAlreadySetError(errortxt)

    @classmethod
    def getiddname(cls):
        """Get the name of the current IDD used by eppy.

        Returns
        -------
        str

        """
        return cls.iddname

    @classmethod
    def setidd(cls, iddinfo, block):
        """Set the IDD to be used by eppy.

        Parameters
        ----------
        iddinfo : list
            Comments and metadata about fields in the IDD.
        block : list
            Field names in the IDD.

        """
        cls.idd_info = iddinfo
        cls.block = block

    """Methods to do with reading an IDF."""

    def initread(self, idfname):
        """
        Use the current IDD and read an IDF from file. If the IDD has not yet
        been initialised then this is done first.

        Parameters
        ----------
        idf_name : str
            Path to an IDF file.

        """
        with open(idfname, 'r') as _:
            # raise nonexistent file error early if idfname doesn't exist
            pass
        iddfhandle = StringIO(iddcurrent.iddtxt)
        if self.getiddname() == None:
            self.setiddname(iddfhandle)
        self.idfname = idfname
        self.read()

    def initreadtxt(self, idftxt):
        """
        Use the current IDD and read an IDF from text data. If the IDD has not
        yet been initialised then this is done first.

        Parameters
        ----------
        idftxt : str
            Text representing an IDF file.

        """
        iddfhandle = StringIO(iddcurrent.iddtxt)
        if self.getiddname() == None:
            self.setiddname(iddfhandle)
        idfhandle = StringIO(idftxt)
        self.idfname = idfhandle
        self.read()

    def read(self):
        """
        Read the IDF file and the IDD file. If the IDD file had already been
        read, it will not be read again.

        Read populates the following data structures:

        - idfobjects : list
        - model : list
        - idd_info : list

        """
        if self.getiddname() == None:
            errortxt = ("IDD file needed to read the idf file. "
                        "Set it using IDF.setiddname(iddfile)")
            raise IDDNotSetError(errortxt)
        readout = idfreader1(
            self.idfname, self.iddname,
            commdct=self.idd_info, block=self.block)
        self.idfobjects, block, self.model, idd_info = readout
        self.__class__.setidd(idd_info, block)

    """Methods to do with creating a new blank IDF object."""

    def new(self, fname=None):
        """Create a blank new idf file. Filename is optional.

        Parameters
        ----------
        fname : str, optional
            Path to an IDF. This does not need to be set at this point.

        """
        self.initnew(fname)

    def initnew(self, fname):
        """
        Use the current IDD and create a new empty IDF. If the IDD has not yet
        been initialised then this is done first.

        Parameters
        ----------
        fname : str, optional
            Path to an IDF. This does not need to be set at this point.

        """
        iddfhandle = StringIO(iddcurrent.iddtxt)
        if self.getiddname() == None:
            self.setiddname(iddfhandle)
        idfhandle = StringIO('')
        self.idfname = idfhandle
        self.read()
        if fname:
            self.idfname = fname

    """Methods to do with manipulating the objects in an IDF object."""

    def newidfobject(self, key, aname='', **kwargs):
        """
        Add a new idfobject to the model. If you don't specify a value for a
        field, the default value will be set.

        For example ::

            newidfobject("CONSTRUCTION")
            newidfobject("CONSTRUCTION",
                Name='Interior Ceiling_class',
                Outside_Layer='LW Concrete',
                Layer_2='soundmat')

        Parameters
        ----------
        key : str
            The type of IDF object. This must be in ALL_CAPS.
        aname : str, deprecated
            This parameter is not used. It is left there for backward 
            compatibility.
        **kwargs
            Keyword arguments in the format `field=value` used to set the value
            of fields in the IDF object when it is created. 

        Returns
        -------
        EpBunch object

        """
        obj = newrawobject(self.model, self.idd_info, key)
        abunch = obj2bunch(self.model, self.idd_info, obj)
        if aname:
            warning.warn("The aname parameter should no longer be used.")
            namebunch(abunch, aname)
        self.idfobjects[key].append(abunch)
        for k, v in list(kwargs.items()):
            abunch[k] = v
        return abunch

    def popidfobject(self, key, index):
        """Pop an IDF object from the IDF.

        Parameters
        ----------
        key : str
            The type of IDF object. This must be in ALL_CAPS.
        index : int
            The index of the object to pop.

        Returns
        -------
        EpBunch object.

        """
        return self.idfobjects[key].pop(index)

    def removeidfobject(self, idfobject):
        """Remove an IDF object from the IDF.

        Parameters
        ----------
        idfobject : EpBunch object
            The IDF object to remove.

        """
        key = idfobject.key.upper()
        self.idfobjects[key].remove(idfobject)

    def copyidfobject(self, idfobject):
        """Add an IDF object to the IDF.

        Parameters
        ----------
        idfobject : EpBunch object
            The IDF object to remove. This usually comes from another idf file,
            or it can be used to copy within this idf file.

        """
        addthisbunch(self.idfobjects,
                     self.model,
                     self.idd_info,
                     idfobject)

    def getobject(self, key, name):
        """Fetch an IDF object given key and name.

        Parameters
        ----------
        key : str
            The type of IDF object. This must be in ALL_CAPS.
        name : str
            The name of the object to fetch.

        Returns
        -------
        EpBunch object.

        """
        return getobject(self.idfobjects, key, name)

    def getextensibleindex(self, key, name):
        """
        Get the index of the first extensible item.

        Only for internal use. # TODO : hide this

        Parameters
        ----------
        key : str
            The type of IDF object. This must be in ALL_CAPS.
        name : str
            The name of the object to fetch.

        Returns
        -------
        int

        """
        return getextensibleindex(
            self.idfobjects, self.model, self.idd_info,
            key, name)

    def removeextensibles(self, key, name):
        """
        Remove extensible items in the object of key and name.

        Only for internal use. # TODO : hide this

        Parameters
        ----------
        key : str
            The type of IDF object. This must be in ALL_CAPS.
        name : str
            The name of the object to fetch.

        Returns
        -------
        EpBunch object

        """
        return removeextensibles(
            self.idfobjects, self.model, self.idd_info,
            key, name)

    """Methods to do with outputting an IDF."""

    def printidf(self):
        """Print the IDF.
        """
        print(self.idfstr())

    def idfstr(self):
        """String representation of the IDF.

        Returns
        -------
        str

        """
        if self.outputtype == 'standard':
            astr = ''
        else:
            astr = self.model.__repr__()

        if self.outputtype == 'standard':
            astr = ''
            dtls = self.model.dtls
            for objname in dtls:
                for obj in self.idfobjects[objname]:
                    astr = astr + obj.__repr__()
        elif self.outputtype == 'nocomment':
            return astr
        elif self.outputtype == 'nocomment1':
            slist = astr.split('\n')
            slist = [item.strip() for item in slist]
            astr = '\n'.join(slist)
        elif self.outputtype == 'nocomment2':
            slist = astr.split('\n')
            slist = [item.strip() for item in slist]
            slist = [item for item in slist if item != '']
            astr = '\n'.join(slist)
        elif self.outputtype == 'compressed':
            slist = astr.split('\n')
            slist = [item.strip() for item in slist]
            astr = ' '.join(slist)
        else:
            raise ValueError("%s is not a valid outputtype" % self.outputtype)
        return astr

    def save(self, filename=None, lineendings='default', encoding='latin-1'):
        """ 
        Save the IDF as a text file with the optional filename passed, or with
        the current idfname of the IDF.

        Parameters
        ----------
        filename : str, optional
            Filepath to save the file. If None then use the IDF.idfname
            parameter. Also accepts a file handle.

        lineendings : str, optional
            Line endings to use in the saved file. Options are 'default',
            'windows' and 'unix' the default is 'default' which uses the line
            endings for the current system.

        encoding : str, optional
            Encoding to use for the saved file. The default is 'latin-1' which
            is compatible with the EnergyPlus IDFEditor.

        """
        if filename is None:
            filename = self.idfname
        s = self.idfstr()
        if lineendings == 'default':
            system = platform.system()
            s = '!- {} Line endings \n'.format(system) + s
            slines = s.splitlines()
            s = os.linesep.join(slines)
        elif lineendings == 'windows':
            s = '!- Windows Line endings \n' + s
            slines = s.splitlines()
            s = '\r\n'.join(slines)
        elif lineendings == 'unix':
            s = '!- Unix Line endings \n' + s
            slines = s.splitlines()
            s = '\n'.join(slines)

        s = s.encode(encoding)
        try:
            with open(filename, 'wb') as idf_out:
                idf_out.write(s)
        except TypeError:  # in the case that filename is a file handle
            try:
                filename.write(s)
            except TypeError:
                filename.write(s.decode(encoding))

    def saveas(self, filename, lineendings='default', encoding='latin-1'):
        """ Save the IDF as a text file with the filename passed.

        Parameters
        ----------
        filename : str
            Filepath to to set the idfname attribute to and save the file as.

        lineendings : str, optional
            Line endings to use in the saved file. Options are 'default',
            'windows' and 'unix' the default is 'default' which uses the line
            endings for the current system.

        encoding : str, optional
            Encoding to use for the saved file. The default is 'latin-1' which
            is compatible with the EnergyPlus IDFEditor.

        """
        self.idfname = filename
        self.save(filename, lineendings, encoding)

    def savecopy(self, filename, lineendings='default', encoding='latin-1'):
        """Save a copy of the file with the filename passed.

        Parameters
        ----------
        filename : str
            Filepath to save the file.

        lineendings : str, optional
            Line endings to use in the saved file. Options are 'default',
            'windows' and 'unix' the default is 'default' which uses the line
            endings for the current system.

        encoding : str, optional
            Encoding to use for the saved file. The default is 'latin-1' which
            is compatible with the EnergyPlus IDFEditor.

        """
        self.save(filename, lineendings, encoding)
