# Copyright (c) 2012, 2020, 2022 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# Copyright (c) 2020 Cheng Cui
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Sub class Bunch to represent an IDF object.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import itertools

from munch import Munch as Bunch

from eppy.bunchhelpers import matchfieldnames, scientificnotation, makefieldname
import eppy.function_helpers as fh
import eppy.ext_field_functions as extff


class BadEPFieldError(AttributeError):
    """An Exception"""

    pass


class RangeError(ValueError):
    """An Exception"""

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


def somevalues(ddtt):
    """returns some values"""
    return ddtt.Name, ddtt.Construction_Name, ddtt.obj


def extendlist(lst, i, value=""):
    """extend the list so that you have i-th value"""
    if i < len(lst):
        pass
    else:
        lst.extend([value] * (i - len(lst) + 1))


def return42(self, *args, **kwargs):
    # proof of concept - to be removed
    return 42


def addfunctions(abunch):
    """add functions to epbunch"""

    key = abunch.obj[0].upper()

    # -----------------
    # TODO : alternate strategy to avoid listing the objkeys in snames
    # check if epbunch has field "Zone_Name" or "Building_Surface_Name"
    # and is in group u'Thermal Zones and Surfaces'
    # then it is likely to be a surface.
    # of course we need to recode for surfaces that do not have coordinates :-(
    # or we can filter those out since they do not have
    # the field "Number_of_Vertices"
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
            "true_azimuth": fh.true_azimuth,
            "tilt": fh.tilt,
            "coords": fh.getcoords,  # needed for debugging
        }
        abunch.__functions.update(func_dict)

    # -----------------
    # print(abunch.getfieldidd )
    names = [
        "CONSTRUCTION",
        "MATERIAL",
        "MATERIAL:AIRGAP",
        "MATERIAL:INFRAREDTRANSPARENT",
        "MATERIAL:NOMASS",
        "MATERIAL:ROOFVEGETATION",
        "WINDOWMATERIAL:BLIND",
        "WINDOWMATERIAL:GLAZING",
        "WINDOWMATERIAL:GLAZING:REFRACTIONEXTINCTIONMETHOD",
        "WINDOWMATERIAL:GAP",
        "WINDOWMATERIAL:GAS",
        "WINDOWMATERIAL:GASMIXTURE",
        "WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC",
        "WINDOWMATERIAL:SCREEN",
        "WINDOWMATERIAL:SHADE",
        "WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM",
    ]
    if key in names:
        func_dict = {
            "rvalue": fh.rvalue,
            "ufactor": fh.ufactor,
            "rvalue_ip": fh.rvalue_ip,  # quick fix for Santosh. Needs to thought thru
            "ufactor_ip": fh.ufactor_ip,  # quick fix for Santosh. Needs to thought thru
            "heatcapacity": fh.heatcapacity,
        }
        abunch.__functions.update(func_dict)

    names = [
        "FAN:CONSTANTVOLUME",
        "FAN:VARIABLEVOLUME",
        "FAN:ONOFF",
        "FAN:ZONEEXHAUST",
        "FANPERFORMANCE:NIGHTVENTILATION",
    ]
    if key in names:
        func_dict = {
            "f_fanpower_bhp": fh.fanpower_bhp,
            "f_fanpower_watts": fh.fanpower_watts,
            "f_fan_maxcfm": fh.fan_maxcfm,
        }
        abunch.__functions.update(func_dict)
    # =====
    # code for references
    # -----------------
    # add function zonesurfaces
    if key == "ZONE":
        func_dict = {"zonesurfaces": fh.zonesurfaces}
        abunch.__functions.update(func_dict)

    # -----------------
    # add function subsurfaces
    # going to cheat here a bit
    # check if epbunch has field "Zone_Name"
    # and is in group u'Thermal Zones and Surfaces'
    # then it is likely to be a surface attached to a zone
    fields = abunch.fieldnames
    try:
        group = abunch.getfieldidd("key")["group"]
    except KeyError as e:  # some pytests don't have group
        group = None
    if group == "Thermal Zones and Surfaces":
        if "Zone_Name" in fields:
            func_dict = {"subsurfaces": fh.subsurfaces}
            abunch.__functions.update(func_dict)

    return abunch


class EpBunch(Bunch):
    """
    Fields, values, and descriptions of fields in an EnergyPlus IDF object
    stored in a `bunch` which is a `dict` extended to allow access to dict
    fields as attributes as well as by keys.

    """

    def __init__(self, obj, objls, objidd, *args, **kwargs):
        super(EpBunch, self).__init__(*args, **kwargs)
        self.obj = obj  # field names
        self.objls = objls  # field values
        self.objidd = objidd  # field metadata (minimum, maximum, type, etc.)
        self.theidf = None  # pointer to the idf this epbunch belongs to
        # This is None if there is no idf - a standalone epbunch
        # This will be set by Idf_MSequence
        self["__functions"] = {}  # initialize the functions
        addfunctions(self)

    @property
    def fieldnames(self):
        """Friendly name for objls."""
        return self.objls

    @property
    def fieldvalues(self):
        """Friendly name for obj."""
        return self.obj

    def checkrange(self, fieldname):
        """Check if the value for a field is within the allowed range."""
        return checkrange(self, fieldname)

    def getrange(self, fieldname):
        """Get the allowed range of values for a field."""
        return getrange(self, fieldname)

    def getfieldidd(self, fieldname):
        """get the idd dict for this field
        Will return {} if the fieldname does not exist"""
        return getfieldidd(self, fieldname)

    def getfieldidd_item(self, fieldname, iddkey):
        """return an item from the fieldidd, given the iddkey
        will return and empty list if it does not have the iddkey
        or if the fieldname does not exist"""
        return getfieldidd_item(self, fieldname, iddkey)

    def get_retaincase(self, fieldname):
        """check if the field should retain case"""
        return get_retaincase(self, fieldname)

    def isequal(self, fieldname, value, places=7):
        """return True if the field == value
        Will retain case if get_retaincase == True
        for real value will compare to decimal 'places'
        """
        return isequal(self, fieldname, value, places=places)

    def getreferingobjs(self, iddgroups=None, fields=None):
        """Get a list of objects that refer to this object"""
        return getreferingobjs(self, iddgroups=iddgroups, fields=fields)

    def get_referenced_object(self, fieldname):
        """
        Get an object referred to by a field in another object.

        For example an object of type Construction has fields for each layer, each
        of which refers to a Material. This functions allows the object
        representing a Material to be fetched using the name of the layer.

        Returns the first item found since if there is more than one matching item,
        it is a malformed IDF.

        Parameters
        ----------
        referring_object : EpBunch
            The object which contains a reference to another object,
        fieldname : str
            The name of the field in the referring object which contains the
            reference to another object.

        Returns
        -------
        EpBunch

        """
        return get_referenced_object(self, fieldname)

    def __setattr__(self, name, value):
        try:
            origname = self["__functions"][name]
            # TODO: unit test never hits here so what is it for?
            self[origname] = value
        except KeyError:
            pass

        try:
            name = self["__aliases"][name]  # get original name of the alias
        except KeyError:
            pass

        if name in ("__functions", "__aliases"):  # just set the new value
            self[name] = value
            return None
        elif name in ("obj", "objls", "objidd", "theidf"):  # let Bunch handle it
            super(EpBunch, self).__setattr__(name, value)
            return None
        elif name in self.fieldnames:  # set the value, extending if needed
            i = self.fieldnames.index(name)
            try:
                self.fieldvalues[i] = value
            except IndexError:
                extendlist(self.fieldvalues, i)
                self.fieldvalues[i] = value
        # elif name_is_extensible(name):
        #     # do one field at a time - mto start with
        #     extendinIDD
        #     do the previous elif
        elif extff.getextensible(self.objidd):  # idfobject has extensible fields
            if extff.islegalextensiblefield(
                self.objidd, name
            ):  # is the field a legal extensible field
                # What is the integer on that field
                name_int = extff.extfieldint(name)
                # get the int in the last extensible field
                last_extfield = self.objidd[-1]["field"][0]
                last_extfield_int = extff.extfieldint(last_extfield, sep=" ")
                # calculate the number of new field sets to be generated
                newextensibles = name_int - last_extfield_int
                # generate the new fileds in eppy's IDD
                key_i = self.theidf.model.dtls.index(self.key)
                mult = extff.getextensible(self.objidd)
                extff.increaseIDDfields(
                    self.theidf.block,
                    self.theidf.idd_info,
                    key_i,
                    self.key,
                    newextensibles * mult,
                )
                # need to update objls and objidd here
                self.objidd = self.theidf.idd_info[key_i]

                objfields = [comm.get("field") for comm in self.objidd]
                objfields[0] = ["key"]
                objfields = [field[0] for field in objfields]
                obj_fields = [makefieldname(field) for field in objfields]
                self.objls = obj_fields
                if name in self.fieldnames:  # set the value, extending if needed
                    i = self.fieldnames.index(name)
                    try:
                        self.fieldvalues[i] = value
                    except IndexError:
                        extendlist(self.fieldvalues, i)
                        self.fieldvalues[i] = value
                else:
                    pass
            else:
                astr = "unable to find field %s" % (name,)
                raise BadEPFieldError(astr)  # TODO: could raise AttributeError
        else:
            astr = "unable to find field %s" % (name,)
            raise BadEPFieldError(astr)  # TODO: could raise AttributeError

    def __getattr__(self, name):
        try:
            func = self["__functions"][name]
            return func(self)
        except KeyError:
            pass

        try:
            name = self["__aliases"][name]
        except KeyError:
            pass

        if name == "__functions":
            return self["__functions"]
        elif name in ("__aliases", "obj", "objls", "objidd", "theidf"):
            # unit test
            return super(EpBunch, self).__getattr__(name)
        elif name in self.fieldnames:
            i = self.fieldnames.index(name)
            try:
                return self.fieldvalues[i]
            except IndexError:
                return ""
        elif extff.getextensible(self.objidd):  # idfobject has extensible fields
            if extff.islegalextensiblefield(
                self.objidd, name
            ):  # is the field a legal extensible field
                # no point creating a field
                return ""
            else:
                astr = "unable to find field %s" % (name,)
                raise BadEPFieldError(astr)  # TODO: could raise AttributeError
                astr = "unable to find field %s" % (name,)
                raise BadEPFieldError(astr)
        else:
            astr = "unable to find field %s" % (name,)
            raise BadEPFieldError(astr)

    def __getitem__(self, key):
        if key in ("obj", "objls", "objidd", "__functions", "__aliases", "theidf"):
            return super(EpBunch, self).__getitem__(key)
        elif key in self.fieldnames:
            i = self.fieldnames.index(key)
            try:
                return self.fieldvalues[i]
            except IndexError:
                return ""
        elif extff.getextensible(self.objidd):  # idfobject has extensible fields
            if extff.islegalextensiblefield(
                self.objidd, key
            ):  # is the field a legal extensible field
                # no point creating a field
                return ""
            else:
                astr = "unable to find field %s" % (key,)
                raise BadEPFieldError(astr)
        else:
            # TODO: Do similar strategy as in __getattr__
            astr = "unknown field %s" % (key,)
            raise BadEPFieldError(astr)

    def __setitem__(self, key, value):
        if key in ("obj", "objls", "objidd", "__functions", "__aliases", "theidf"):
            super(EpBunch, self).__setitem__(key, value)
            return None
        elif key in self.fieldnames:
            i = self.fieldnames.index(key)
            try:
                self.fieldvalues[i] = value
            except IndexError:
                extendlist(self.fieldvalues, i)
                self.fieldvalues[i] = value
        elif extff.getextensible(self.objidd):  # idfobject has extensible fields
            if extff.islegalextensiblefield(
                self.objidd, key
            ):  # is the field a legal extensible field
                # What is the integer on that field
                name_int = extff.extfieldint(key)
                # get the int in the last extensible field
                last_extfield = self.objidd[-1]["field"][0]
                last_extfield_int = extff.extfieldint(last_extfield, sep=" ")
                # calculate the number of new fields to be generated
                newextensibles = name_int - last_extfield_int
                # generate the new fileds in eppy's IDD
                key_i = self.theidf.model.dtls.index(self.key)
                mult = extff.getextensible(self.objidd)
                extff.increaseIDDfields(
                    self.theidf.block,
                    self.theidf.idd_info,
                    key_i,
                    self.key,
                    newextensibles * mult,
                )
                # need to update objls and objidd here
                self.objidd = self.theidf.idd_info[key_i]

                objfields = [comm.get("field") for comm in self.objidd]
                objfields[0] = ["key"]
                objfields = [field[0] for field in objfields]
                obj_fields = [makefieldname(field) for field in objfields]
                self.objls = obj_fields
                if key in self.fieldnames:  # set the value, extending if needed
                    i = self.fieldnames.index(key)
                    try:
                        self.fieldvalues[i] = value
                    except IndexError:
                        extendlist(self.fieldvalues, i)
                        self.fieldvalues[i] = value
                else:
                    pass
            else:
                astr = "unknown field %s" % (key,)
                raise BadEPFieldError(astr)
        else:
            astr = "unknown field %s" % (key,)
            raise BadEPFieldError(astr)

    def __repr__(self):
        """print this as an idf snippet"""
        # lines = [str(val) for val in self.obj]
        # replace the above line with code that will print an integer without decimals
        lines = []
        for val in self.obj:
            try:
                value = int(val)
                if value != val:
                    value = val
            except ValueError as e:
                value = val
            lines.append(value)
        # ------------
        comments = [comm.replace("_", " ") for comm in self.objls]
        lines[0] = "%s," % (lines[0],)  # comma after first line
        for i, line in enumerate(lines[1:-1]):
            line = scientificnotation(
                line, width=18
            )  # E+ cannot read wide numbers, convert to 1e+3
            lines[i + 1] = "    %s," % (line,)  # indent and comma
        lines[-1] = "    %s;" % (lines[-1],)  # ';' after last line
        lines = lines[:1] + [line.ljust(26) for line in lines[1:]]  # ljsut the lines
        filler = "%s    !- %s"
        nlines = [
            filler % (line, comm) for line, comm in zip(lines[1:], comments[1:])
        ]  # adds comments to line
        nlines.insert(0, lines[0])  # first line without comment
        astr = "\n".join(nlines)
        return "\n%s\n" % (astr,)

    def __str__(self):
        """same as __repr__"""
        # needed if YAML is installed. See issue 67
        # unit test
        return self.__repr__()

    def __dir__(self):
        fnames = self.fieldnames
        func_names = list(self["__functions"].keys())
        return super(EpBunch, self).__dir__() + fnames + func_names


def getrange(bch, fieldname):
    """get the ranges for this field"""
    keys = ["maximum", "minimum", "maximum<", "minimum>", "type"]
    index = bch.objls.index(fieldname)
    fielddct_orig = bch.objidd[index]
    fielddct = copy.deepcopy(fielddct_orig)
    therange = {}
    for key in keys:
        therange[key] = fielddct.setdefault(key, None)
    if therange["type"]:
        therange["type"] = therange["type"][0]
    if therange["type"] == "real":
        for key in keys[:-1]:
            if therange[key]:
                therange[key] = float(therange[key][0])
    if therange["type"] == "integer":
        for key in keys[:-1]:
            if therange[key]:
                therange[key] = int(therange[key][0])
    return therange


def checkrange(bch, fieldname):
    """throw exception if the out of range"""
    fieldvalue = bch[fieldname]
    therange = bch.getrange(fieldname)
    if therange["maximum"] != None:
        if fieldvalue > therange["maximum"]:
            astr = "Value %s is not less or equal to the 'maximum' of %s"
            astr = astr % (fieldvalue, therange["maximum"])
            raise RangeError(astr)
    if therange["minimum"] != None:
        if fieldvalue < therange["minimum"]:
            astr = "Value %s is not greater or equal to the 'minimum' of %s"
            astr = astr % (fieldvalue, therange["minimum"])
            raise RangeError(astr)
    if therange["maximum<"] != None:
        if fieldvalue >= therange["maximum<"]:
            astr = "Value %s is not less than the 'maximum<' of %s"
            astr = astr % (fieldvalue, therange["maximum<"])
            raise RangeError(astr)
    if therange["minimum>"] != None:
        if fieldvalue <= therange["minimum>"]:
            astr = "Value %s is not greater than the 'minimum>' of %s"
            astr = astr % (fieldvalue, therange["minimum>"])
            raise RangeError(astr)
    return fieldvalue
    """get the idd dict for this field
    Will return {} if the fieldname does not exist"""


def getfieldidd(bch, fieldname):
    """get the idd dict for this field
    Will return {} if the fieldname does not exist"""
    # print(bch)
    try:
        fieldindex = bch.objls.index(fieldname)
    except ValueError as e:
        return {}  # the fieldname does not exist
        # so there is no idd
    fieldidd = bch.objidd[fieldindex]
    return fieldidd


def getfieldidd_item(bch, fieldname, iddkey):
    """return an item from the fieldidd, given the iddkey
    will return and empty list if it does not have the iddkey
    or if the fieldname does not exist"""
    fieldidd = getfieldidd(bch, fieldname)
    try:
        return fieldidd[iddkey]
    except KeyError as e:
        return []


def get_retaincase(bch, fieldname):
    """Check if the field should retain case"""
    fieldidd = bch.getfieldidd(fieldname)
    return "retaincase" in fieldidd


def isequal(bch, fieldname, value, places=7):
    """return True if the field is equal to value"""

    def equalalphanumeric(bch, fieldname, value):
        if bch.get_retaincase(fieldname):
            return bch[fieldname] == value
        else:
            return bch[fieldname].upper() == value.upper()

    fieldidd = bch.getfieldidd(fieldname)
    try:
        ftype = fieldidd["type"][0]
        if ftype in ["real", "integer"]:
            return almostequal(bch[fieldname], float(value), places=places)
        else:
            return equalalphanumeric(bch, fieldname, value)
    except KeyError as e:
        return equalalphanumeric(bch, fieldname, value)


def getreferingobjs(referedobj, iddgroups=None, fields=None):
    """Get a list of objects that refer to this object"""
    # pseudocode for code below
    # referringobjs = []
    # referedobj has: -> Name
    #                 -> reference
    # for each obj in idf:
    # [optional filter -> objects in iddgroup]
    #     each field of obj:
    #     [optional filter -> field in fields]
    #         has object-list [refname]:
    #             if refname in reference:
    #                 if Name = field value:
    #                     referringobjs.append()
    referringobjs = []
    idf = referedobj.theidf
    referedidd = referedobj.getfieldidd("Name")
    try:
        references = referedidd["reference"]
    except KeyError as e:
        return referringobjs
    idfobjs = idf.idfobjects.values()
    idfobjs = list(itertools.chain.from_iterable(idfobjs))  # flatten list
    if iddgroups:  # optional filter
        idfobjs = [
            anobj for anobj in idfobjs if anobj.getfieldidd("key")["group"] in iddgroups
        ]
    for anobj in idfobjs:
        if not fields:
            thefields = anobj.objls
        else:
            thefields = fields
        for field in thefields:
            try:
                itsidd = anobj.getfieldidd(field)
            except ValueError as e:
                continue
            if "object-list" in itsidd:
                refname = itsidd["object-list"][0]
                if refname in references:
                    if referedobj.isequal("Name", anobj[field]):
                        referringobjs.append(anobj)
    return referringobjs


def get_referenced_object(referring_object, fieldname):
    """
    Get an object referred to by a field in another object.

    For example an object of type Construction has fields for each layer, each
    of which refers to a Material. This functions allows the object
    representing a Material to be fetched using the name of the layer.

    Returns the first item found since if there is more than one matching item,
    it is a malformed IDF.

    Parameters
    ----------
    referring_object : EpBunch
        The object which contains a reference to another object,
    fieldname : str
        The name of the field in the referring object which contains the
        reference to another object.

    Returns
    -------
    EpBunch

    """
    idf = referring_object.theidf
    object_list = referring_object.getfieldidd_item(fieldname, "object-list")
    for obj_type in idf.idfobjects:
        for obj in idf.idfobjects[obj_type]:
            valid_object_lists = obj.getfieldidd_item("Name", "reference")
            if set(object_list).intersection(set(valid_object_lists)):
                referenced_obj_name = referring_object[fieldname]
                if obj.Name == referenced_obj_name:
                    return obj
