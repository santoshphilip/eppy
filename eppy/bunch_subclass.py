# Copyright (c) 2012, 2020, 2022, 2026 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# Copyright (c) 2020 Cheng Cui
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Sub-class of Bunch that represents a single EnergyPlus IDF object.

This module provides the ``EpBunch`` class (a dict-like object that also
supports attribute access) together with a collection of helper
functions that operate on ``EpBunch`` instances.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
import itertools

from munch import Munch as Bunch
from epconversions import epconversions as epc

from eppy.bunchhelpers import matchfieldnames, scientificnotation, makefieldname
import eppy.function_helpers as fh
import eppy.ext_field_functions as extff


class BadEPFieldError(AttributeError):
    """Raised when an unknown or illegal field name is accessed on an EpBunch."""

    pass


class RangeError(ValueError):
    """Raised when a field value lies outside the range defined in the IDD."""

    pass


def almostequal(first, second, places=7, printit=True):
    """Test whether two numeric values are equal to a given number of places.

    This implementation is based on the corresponding method in Python’s
    ``unittest`` module and may therefore be covered by the Python licence.

    Parameters
    ----------
    first : float or int
        First value to compare.
    second : float or int
        Second value to compare.
    places : int, optional
        Number of decimal places to which the values must agree
        (default is 7).
    printit : bool, optional
        If ``True`` (default) print a diagnostic message when the values
        are not almost equal.

    Returns
    -------
    bool
        ``True`` if the values agree to the requested number of places,
        ``False`` otherwise.
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
    """Return a tuple of a few commonly-used fields from an EpBunch.

    Parameters
    ----------
    ddtt : EpBunch
        The object from which the values are taken.

    Returns
    -------
    tuple
        ``(Name, Construction_Name, obj)``.
    """
    return ddtt.Name, ddtt.Construction_Name, ddtt.obj


def extendlist(lst, i, value=""):
    """Extend a list so that index ``i`` becomes a valid index.

    If ``i`` is already inside the list nothing is done; otherwise the
    list is padded with ``value`` up to (and including) index ``i``.

    Parameters
    ----------
    lst : list
        The list to be extended (modified in-place).
    i : int
        Desired index that must become valid.
    value : object, optional
        Fill value used for the new elements (default is the empty string).

    Returns
    -------
    None
    """
    if i < len(lst):
        pass
    else:
        lst.extend([value] * (i - len(lst) + 1))


def return42(self, *args, **kwargs):
    """Proof-of-concept stub that always returns 42 (to be removed)."""
    # proof of concept - to be removed
    return 42


def addfunctions(abunch):
    """Attach specialised helper methods to an EpBunch instance.

    Depending on the object type (surface, material, fan, zone, …)
    the appropriate calculation functions (area, r-value, fan power,
    etc.) are added to the instance’s ``__functions`` dictionary.

    Parameters
    ----------
    abunch : EpBunch
        The object that will receive the extra methods.

    Returns
    -------
    EpBunch
        The same object, now with additional functions attached.
    """
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
    """Dict-like container for a single EnergyPlus IDF object.

    Fields, values and the corresponding IDD metadata are stored so that
    they can be accessed both by key and by attribute.  A number of
    convenience methods for range checking, unit conversion, object
    references, etc. are also provided.
    """

    def __init__(self, obj, objls, objidd, *args, **kwargs):
        """Initialise an EpBunch.

        Parameters
        ----------
        obj : list
            Field values (the first element is the object type).
        objls : list of str
            Field names that correspond one-to-one with ``obj``.
        objidd : list of dict
            IDD metadata dictionaries for each field.
        *args, **kwargs
            Passed through to the underlying Bunch constructor.
        """
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
        """List of field names (friendly alias for ``objls``).

        Returns
        -------
        list of str
        """
        return self.objls

    @property
    def fieldvalues(self):
        """List of field values (friendly alias for ``obj``).

        Returns
        -------
        list
        """
        return self.obj

    def checkrange(self, fieldname):
        """Check whether the current value of a field lies inside its IDD range.

        Parameters
        ----------
        fieldname : str
            Name of the field to validate.

        Returns
        -------
        object
            The field value itself (unchanged).

        Raises
        ------
        RangeError
            If the value is outside the allowed range.
        """
        return checkrange(self, fieldname)

    def getrange(self, fieldname):
        """Return the numeric range constraints defined for a field in the IDD.

        Parameters
        ----------
        fieldname : str
            Name of the field.

        Returns
        -------
        dict
            Dictionary containing the keys ``maximum``, ``minimum``,
            ``maximum<``, ``minimum>`` and ``type`` (or ``None`` when a
            constraint is not present).
        """
        return getrange(self, fieldname)

    def getunits(self, fieldname):
        """Return the SI unit string of a field, or ``None`` if none is defined.

        Parameters
        ----------
        fieldname : str
            Name of the field.

        Returns
        -------
        str or None
        """
        return getunits(self, fieldname)

    def set_ipvalue(self, fieldname, ipvalue):
        """Convert an IP value to SI and store it in the field.

        The field’s SI unit is obtained with ``getunits``.  The matching
        default IP unit is obtained with ``epconversions.defaultipunit``.
        The conversion itself is performed by ``epconversions.convert2si``.

        Parameters
        ----------
        fieldname : str
            Name of the IDF field (e.g. ``"Thickness"``).
        ipvalue : float or int
            Numeric value expressed in the default IP unit that corresponds
            to the field’s SI unit.

        Notes
        -----
        - If the field has no units the value is stored unchanged.
        - If the conversion cannot be performed the original ``ipvalue``
          is stored unchanged (same graceful fallback used by ``print_ip``).
        """
        siunit = self.getunits(fieldname)
        if siunit is None:
            self[fieldname] = ipvalue
            return

        try:
            ipunit = epc.defaultipunit(siunit)
            sivalue = epc.convert2si(float(ipvalue), ipunit, siunit, unitstr=False)
            self[fieldname] = sivalue
        except (KeyError, AttributeError, TypeError, ValueError):
            # unit unknown or value non-numeric → leave as-is
            self[fieldname] = ipvalue

    def get_ipvalue(self, fieldname):
        """Return the value of the field converted to IP units.

        Parameters
        ----------
        fieldname : str
            Name of the field.

        Returns
        -------
        float, int or original type
            The value expressed in the corresponding IP unit, or the
            original value when conversion is not possible.
        """
        val = self[fieldname]
        unit = self.getunits(fieldname)

        if unit is None:
            return val

        try:
            fval = float(val)
            ip_val = epc.convert2ip(fval, unit, unitstr=False)

            # Prefer a clean integer when the converted value is integral
            try:
                ival = int(ip_val)
                if ival == ip_val:
                    return ival
            except (ValueError, TypeError):
                pass

            return ip_val
        except (ValueError, TypeError, KeyError, AttributeError):
            # non-numeric value or unit that cannot be converted
            return val

    def getfieldidd(self, fieldname):
        """Return the complete IDD metadata dictionary for a field.

        Parameters
        ----------
        fieldname : str
            Name of the field.

        Returns
        -------
        dict
            The IDD dictionary for the field, or an empty dict if the
            field does not exist.
        """
        return getfieldidd(self, fieldname)

    def getfieldidd_item(self, fieldname, iddkey):
        """Return a single item from a field’s IDD dictionary.

        Parameters
        ----------
        fieldname : str
            Name of the IDF field.
        iddkey : str
            Key inside the field’s IDD dictionary
            (e.g. ``"units"``, ``"type"``, ``"minimum"``, ``"retaincase"``).

        Returns
        -------
        list
            The value stored under ``iddkey`` (normally a list), or an
            empty list if the field or the key does not exist.
        """
        return getfieldidd_item(self, fieldname, iddkey)

    def get_retaincase(self, fieldname):
        """Return whether the field should retain case in comparisons.

        Parameters
        ----------
        fieldname : str
            Name of the field.

        Returns
        -------
        bool
            ``True`` if the IDD entry for the field contains the key
            ``retaincase``, ``False`` otherwise.
        """
        return get_retaincase(self, fieldname)

    def isequal(self, fieldname, value, places=7):
        """Test whether a field is equal to a given value.

        String comparisons respect the ``retaincase`` flag; numeric
        comparisons use a tolerance of ``places`` decimal places.

        Parameters
        ----------
        fieldname : str
            Name of the field.
        value : object
            Value to compare against.
        places : int, optional
            Decimal places used for real/integer comparison (default 7).

        Returns
        -------
        bool
        """
        return isequal(self, fieldname, value, places=places)

    def getreferingobjs(self, iddgroups=None, fields=None):
        """Return a list of objects that refer to this object.

        Parameters
        ----------
        iddgroups : list of str, optional
            Restrict the search to objects belonging to these IDD groups.
        fields : list of str, optional
            Restrict the search to these field names.

        Returns
        -------
        list of EpBunch
            All objects that contain a reference to the current object.
        """
        return getreferingobjs(self, iddgroups=iddgroups, fields=fields)

    def get_referenced_object(self, fieldname):
        """Return the object that is referenced by a field of this object.

        For example, a Construction layer field points to a Material;
        this method returns that Material object.

        Parameters
        ----------
        fieldname : str
            Name of the field that holds the reference.

        Returns
        -------
        EpBunch or None
            The first matching referenced object, or ``None`` if none is
            found.  (More than one match indicates a malformed IDF.)
        """
        return get_referenced_object(self, fieldname)

    def __setattr__(self, name, value):
        """Set an attribute / field value on the EpBunch."""
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
        """Get an attribute / field value from the EpBunch."""
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
        """Get an item by key (supports both special keys and field names)."""
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
        """Set an item by key (supports both special keys and field names)."""
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
        """Return a string representation of the object as an IDF snippet."""
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
        justcomments = [comm.replace("_", " ") for comm in self.objls]
        units = [self.getunits(comm) for comm in self.objls]
        comments = [
            f"{justcomment} {{{unit}}}" if unit else justcomment
            for justcomment, unit in zip(justcomments, units)
        ]
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
        """Return the same string as ``__repr__`` (needed when YAML is installed)."""
        # needed if YAML is installed. See issue 67
        # unit test
        return self.__repr__()

    def __dir__(self):
        """Return a list of valid attributes (including field names and functions)."""
        fnames = self.fieldnames
        func_names = list(self["__functions"].keys())
        return super(EpBunch, self).__dir__() + fnames + func_names

    def print_ip(self):
        """Print the object as an IDF snippet with all values converted to IP units.

        Uses ``getunits`` and ``epconversions.convert2ip``.  Fields without
        units or non-numeric values are left unchanged; empty fields still
        show the appropriate IP unit in the comment.
        """
        lines = []
        for val in self.obj:
            try:
                value = int(val)
                if value != val:
                    value = val
            except (ValueError, TypeError):
                value = val
            lines.append(value)

        justcomments = [comm.replace("_", " ") for comm in self.objls]
        units = [self.getunits(comm) for comm in self.objls]

        ip_lines = []
        ip_comments = []
        for val, unit, justcomment in zip(lines, units, justcomments):
            if unit is None:
                # no units at all
                ip_lines.append(val)
                ip_comments.append(justcomment)
                continue

            # We have an SI unit. Decide what IP unit (and value) to show.
            empty = val in ("", None)

            if empty:
                # no value → keep empty, but show the default IP unit
                try:
                    ip_unit = epc.defaultipunit(unit)
                except (KeyError, AttributeError, TypeError):
                    ip_unit = unit  # fallback if unit is not convertible
                ip_lines.append(val)
                ip_comments.append(f"{justcomment} {{{ip_unit}}}")
                continue

            # value present → try to convert
            try:
                ip_val, ip_unit = epc.convert2ip(float(val), unit)
                # prefer clean integer representation when possible
                try:
                    ival = int(ip_val)
                    if ival == ip_val:
                        ip_val = ival
                except (ValueError, TypeError):
                    pass
                ip_lines.append(ip_val)
                ip_comments.append(f"{justcomment} {{{ip_unit}}}")
            except (ValueError, TypeError, KeyError, AttributeError):
                # conversion failed → keep original value, still try for IP unit
                try:
                    ip_unit = epc.defaultipunit(unit)
                except (KeyError, AttributeError, TypeError):
                    ip_unit = unit
                ip_lines.append(val)
                ip_comments.append(f"{justcomment} {{{ip_unit}}}")

        # Format exactly like __repr__
        ip_lines[0] = "%s," % (ip_lines[0],)
        for i, line in enumerate(ip_lines[1:-1]):
            line = scientificnotation(line, width=18)
            ip_lines[i + 1] = "    %s," % (line,)
        ip_lines[-1] = "    %s;" % (ip_lines[-1],)
        ip_lines = ip_lines[:1] + [line.ljust(26) for line in ip_lines[1:]]

        filler = "%s    !- %s"
        nlines = [
            filler % (line, comm) for line, comm in zip(ip_lines[1:], ip_comments[1:])
        ]
        nlines.insert(0, ip_lines[0])
        astr = "\n".join(nlines)
        print("\n%s\n" % (astr,))


def getrange(bch, fieldname):
    """Return the numeric range constraints for a field (see EpBunch.getrange).

    Parameters
    ----------
    bch : EpBunch
        The EnergyPlus object that contains the field.
    fieldname : str
        Name of the field.

    Returns
    -------
    dict
        Dictionary containing the keys ``maximum``, ``minimum``,
        ``maximum<``, ``minimum>`` and ``type`` (or ``None`` when a
        constraint is not present).
    """
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


def getunits(bch, fieldname):
    """Return the SI unit string of a field, or ``None`` if the field has no units.

    Parameters
    ----------
    bch : EpBunch
        The EnergyPlus object that contains the field.
    fieldname : str
        Name of the field.

    Returns
    -------
    str or None
    """
    units = getfieldidd_item(bch, fieldname, "units")
    if units:
        return units[0]
    return None


def checkrange(bch, fieldname):
    """Validate that a field value lies inside its IDD range (see EpBunch.checkrange).

    Parameters
    ----------
    bch : EpBunch
        The EnergyPlus object that contains the field.
    fieldname : str
        Name of the field to validate.

    Returns
    -------
    object
        The field value itself (unchanged).

    Raises
    ------
    RangeError
        If the value is outside the allowed limits.
    """
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


def getfieldidd(bch, fieldname):
    """Return the IDD metadata dictionary for a field (see EpBunch.getfieldidd).

    Parameters
    ----------
    bch : EpBunch
        The EnergyPlus object that contains the field.
    fieldname : str
        Name of the field.

    Returns
    -------
    dict
        The IDD dictionary for the field, or an empty dict if the
        field does not exist.
    """
    # print(bch)
    try:
        fieldindex = bch.objls.index(fieldname)
    except ValueError as e:
        return {}  # the fieldname does not exist
        # so there is no idd
    fieldidd = bch.objidd[fieldindex]
    return fieldidd


def getfieldidd_item(bch, fieldname, iddkey):
    """Return a single item from a field’s IDD dictionary
    (see EpBunch.getfieldidd_item).

    Parameters
    ----------
    bch : EpBunch
        The EnergyPlus object that contains the field.
    fieldname : str
        Name of the IDF field.
    iddkey : str
        Key inside the field’s IDD dictionary
        (e.g. ``"units"``, ``"type"``, ``"minimum"``, ``"retaincase"``).

    Returns
    -------
    list
        The value stored under ``iddkey`` (normally a list), or an
        empty list if the field or the key does not exist.
    """
    fieldidd = getfieldidd(bch, fieldname)
    try:
        return fieldidd[iddkey]
    except KeyError as e:
        return []


def get_retaincase(bch, fieldname):
    """Return whether the field should retain case (see EpBunch.get_retaincase).

    Parameters
    ----------
    bch : EpBunch
        The EnergyPlus object that contains the field.
    fieldname : str
        Name of the field.

    Returns
    -------
    bool
        ``True`` if the IDD entry for the field contains the key
        ``retaincase``, ``False`` otherwise.
    """
    fieldidd = bch.getfieldidd(fieldname)
    return "retaincase" in fieldidd


def isequal(bch, fieldname, value, places=7):
    """Test whether a field equals a value (see EpBunch.isequal).

    Parameters
    ----------
    bch : EpBunch
        The EnergyPlus object that contains the field.
    fieldname : str
        Name of the field.
    value : object
        Value to compare against.
    places : int, optional
        Decimal places used for real/integer comparison (default 7).

    Returns
    -------
    bool
    """

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
    """Return objects that refer to ``referedobj``
    (see EpBunch.getreferingobjs).

    Parameters
    ----------
    referedobj : EpBunch
        The object that is being referred to.
    iddgroups : list of str, optional
        Restrict the search to objects belonging to these IDD groups.
    fields : list of str, optional
        Restrict the search to these field names.

    Returns
    -------
    list of EpBunch
        All objects that contain a reference to ``referedobj``.
    """
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
    """Return the object referenced by a field of ``referring_object``
    (see EpBunch.get_referenced_object).

    For example an object of type Construction has fields for each layer, each
    of which refers to a Material. This functions allows the object
    representing a Material to be fetched using the name of the layer.

    Returns the first item found since if there is more than one matching item,
    it is a malformed IDF.

    Parameters
    ----------
    referring_object : EpBunch
        The object which contains a reference to another object.
    fieldname : str
        The name of the field in the referring object which contains the
        reference to another object.

    Returns
    -------
    EpBunch or None
        The first matching referenced object, or ``None`` if none is found.
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