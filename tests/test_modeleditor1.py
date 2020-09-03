# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for some functions of modeleditor"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import StringIO
import pytest
from eppy import modeleditor
import eppy.idfreader as idfreader
import eppy.snippet as snippet
from eppy.iddcurrent import iddcurrent

idfsnippet = snippet.idfsnippet
iddsnippet = iddcurrent.iddtxt
idffhandle = StringIO(idfsnippet)
iddfhandle = StringIO(iddsnippet)
bunchdt, data, commdct, idd_index = idfreader.idfreader(idffhandle, iddfhandle, None)


def test_addobject():
    """py.test for addobject"""
    thedata = (
        # key, aname, fielddict
        ("ZONE", None, dict(Name="Gumby", X_Origin=50)),
        ("ZONE", "karamba", {}),  # key, aname, fielddict
        ("ZONE", None, {}),  # key, aname, fielddict
        # key, aname, fielddict
        ("ZONE", None, dict(Name="Gumby", X_Origin=50)),
    )
    for key, aname, fielddict in thedata:
        result = modeleditor.addobject(
            bunchdt, data, commdct, key, None, aname, **fielddict
        )
        assert bunchdt[key][-1].key == key  # wierd, but correct :-)
        if aname:
            assert data.dt[key][-1][1] == aname
            assert bunchdt[key][-1].Name == aname
        if fielddict:
            for kkey, value in fielddict.items():
                assert bunchdt[key][-1][kkey] == value


def test_addobject1():
    """py.test for addobject"""
    thedata = (("ZONE", {"Name": "karamba"}),)  # key, kwargs
    for key, kwargs in thedata:
        result = modeleditor.addobject1(bunchdt, data, commdct, key, **kwargs)
        aname = kwargs["Name"]
        assert data.dt[key][-1][1] == aname
        assert bunchdt[key][-1].Name == aname


def test_getobject():
    """py.test for getobject"""
    thedata = (
        ("ZONE", "PLENUM-1", bunchdt["ZONE"][0]),  # key, name, theobject
        # key, name, theobject
        ("ZONE", "PLENUM-1".lower(), bunchdt["ZONE"][0]),
        ("ZONE", "PLENUM-A", None),  # key, name, theobject
        (
            "ZONEHVAC:EQUIPMENTCONNECTIONS",
            "SPACE1-1",
            bunchdt["ZONEHVAC:EQUIPMENTCONNECTIONS"][0],
        ),  # key, name, theobject
    )
    for key, name, theobject in thedata:
        result = modeleditor.getobject(bunchdt, key, name)
        assert result == theobject


def test___objecthasfields():
    """py.test for __objecthasfields"""
    thedata = (
        ("ZONE", dict(Name="testzone", X_Origin=32), "testzone", True),
        # key, fielddict, aname, istrue
        ("ZONE", dict(Name="testzone", X_Origin=32), "testzone1", False),
        # key, fielddict, aname, istrue
    )
    for key, fielddict, aname, istrue in thedata:
        idfobject = modeleditor.addobject(
            bunchdt, data, commdct, key, None, **fielddict
        )
        idfobject.Name = aname  # modify the name, to check for a False return
        result = modeleditor.__objecthasfields(
            bunchdt, data, commdct, idfobject, **fielddict
        )
        assert result == istrue


def test_getobjects():
    """py.test for getobjects"""
    thedata = (
        ("ZONE", {"Name": "PLENUM-1"}, 7, bunchdt["ZONE"][0:1]),
        # key, fielddict, places, theobjects
        # ('ZONE', {'Name':'PLENUM-1', 'Volume':283.2},7,bunchdt['ZONE'][0:1]),
        # key, fielddict, places, theobjects
        # ('ZONE', {'Y_Origin':0.}, 7, bunchdt['ZONE']),
        # key, fielddict, places, theobjects
    )
    for key, fielddict, places, theobjects in thedata:
        result = modeleditor.getobjects(bunchdt, data, commdct, key, **fielddict)
        assert result == theobjects


def test_is_retaincase():
    """py.test for is_retaincase"""
    thedata = (
        ("BUILDING", "Name", True),  # key, fieldname, case
        ("BUILDING", "Terrain", False),  # key, fieldname, case
    )
    for key, fieldname, case in thedata:
        idfobject = bunchdt[key][0]
        result = modeleditor.is_retaincase(bunchdt, data, commdct, idfobject, fieldname)
        assert result == case


def test_isfieldvalue():
    """py.test for isfieldvalue"""
    thedata = (
        ("BUILDING", 0, "Name", "Building", 7, True),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, "Name", "BuildinG", 7, False),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, "North_Axis", 30, 7, True),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, "North_Axis", "30", 7, True),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, "North_Axis", 30.001, 7, False),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, "North_Axis", 30.001, 2, True),
        # key, objindex1, fieldname, value, places, isequal
        ("ZONE", 0, "Volume", 283.2, 2, True),
        # key, objindex1, fieldname, value, places, isequal
    )
    for key, objindex1, fieldname, value, places, isequal in thedata:
        idfobject = bunchdt[key][objindex1]
        result = modeleditor.isfieldvalue(
            bunchdt, data, commdct, idfobject, fieldname, value, places
        )
        assert result == isequal


def test_equalfield():
    """py.test for equalfield"""
    thedata = (
        ("BUILDING", 0, 1, "Name", 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 2, "Name", 7, False),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, "Terrain", 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, "Terrain", 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, "North_Axis", 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 2, "North_Axis", 2, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 3, "Maximum_Number_of_Warmup_Days", 7, True),
        ("BUILDING", 0, 3, "Minimum_Number_of_Warmup_Days", 7, False),
        # key, objindex1, objeindex2, fieldname, places, isequal
    )
    for key, objindex1, objindex2, fieldname, places, isequal in thedata:
        idfobject1 = bunchdt[key][objindex1]
        idfobject2 = bunchdt[key][objindex2]
        result = modeleditor.equalfield(
            bunchdt, data, commdct, idfobject1, idfobject2, fieldname, places
        )
        assert result == isequal
    (key, objindex1, objeindex2, fieldname, places, isequal) = (
        "BUILDING",
        0,
        1,
        "Name",
        7,
        True,
    )
    idfobject1 = bunchdt[key][objindex1]
    idfobject2 = bunchdt["ZONE"][objindex2]
    with pytest.raises(modeleditor.NotSameObjectError):
        modeleditor.equalfield(
            bunchdt, data, commdct, idfobject1, idfobject2, fieldname, places
        )


def test_removeextensibles():
    """py.test for removeextensibles"""
    thedata = (
        (
            "BuildingSurface:Detailed".upper(),
            "WALL-1PF",
            [
                "BuildingSurface:Detailed",
                "WALL-1PF",
                "WALL",
                "WALL-1",
                "PLENUM-1",
                "Outdoors",
                "",
                "SunExposed",
                "WindExposed",
                "0.50000",
                "4",
            ],
        ),  # key, objname, rawobject
    )
    for key, objname, rawobject in thedata:
        result = modeleditor.removeextensibles(bunchdt, data, commdct, key, objname)
        assert result.obj == rawobject


def test_newrawobject():
    """py.test for newrawobject"""
    thedata = (
        (
            "zone",
            [
                "ZONE",
                "",
                0.0,
                0.0,
                0.0,
                0.0,
                1,
                1,
                "autocalculate",
                "autocalculate",
                "autocalculate",
                "",
                "",
                "Yes",
            ],
        ),  # key, obj
    )
    for key, obj in thedata:
        result = modeleditor.newrawobject(data, commdct, key)
        assert result == obj


def test_obj2bunch():
    """py.test for obj2bunch"""
    thedata = (
        (
            [
                "ZONE",
                "",
                "0",
                "0",
                "0",
                "0",
                "1",
                "1",
                "autocalculate",
                "autocalculate",
                "autocalculate",
                "",
                "",
                "Yes",
            ]
        ),  # obj
    )
    for obj in thedata:
        key_i = data.dtls.index(obj[0].upper())
        abunch = idfreader.makeabunch(commdct, obj, key_i)
        result = modeleditor.obj2bunch(data, commdct, obj)
        assert result.__repr__() == abunch.__repr__()


def test_iddofobject():
    """py.test of iddofobject"""
    thedata = (
        (
            "VERSION",
            [
                {
                    "idfobj": "Version",
                    "group": "Simulation Parameters",
                    "format": ["singleLine"],
                    "unique-object": [""],
                },
                {
                    "default": ["7.0"],
                    "field": ["Version Identifier"],
                    "required-field": [""],
                },
            ],
        ),  # key, itsidd
    )
    for key, itsidd in thedata:
        result = modeleditor.iddofobject(data, commdct, key)
        try:
            result[0].pop("memo")  # memo is new in version 8.0.0
        except KeyError:
            pass
        assert result == itsidd
