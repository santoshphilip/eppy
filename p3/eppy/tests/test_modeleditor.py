# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for modeleditor"""






from io import StringIO
from eppy import modeleditor
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal
from itertools import product
import os

import pytest

import eppy.idfreader as idfreader
import eppy.snippet as snippet
from eppy.bunch_subclass import Bunch

iddsnippet = iddcurrent.iddtxt
idfsnippet = snippet.idfsnippet

idffhandle = StringIO(idfsnippet)
iddfhandle = StringIO(iddsnippet)
bunchdt, data, commdct = idfreader.idfreader(idffhandle, iddfhandle)

# idd is read only once in this test
# if it has already been read from some other test, it will continue with
# the old reading
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_poptrailing():
    """py.test for poptrailing"""
    tdata = (
        (
            [1, 2, 3, '', 56, '', '', '', ''],
            [1, 2, 3, '', 56]
        ),  # lst, popped
        (
            [1, 2, 3, '', 56],
            [1, 2, 3, '', 56]
        ),  # lst, popped
        (
            [1, 2, 3, 56],
            [1, 2, 3, 56]
        ),  # lst, popped
    )
    for before, after in iter(tdata):
        assert modeleditor.poptrailing(before) == after


def test_extendlist():
    """py.test for extendlist"""
    tdata = (
        ([1, 2, 3], 2, 0, [1, 2, 3]),  # lst, i, value, nlst
        ([1, 2, 3], 3, 0, [1, 2, 3, 0]),  # lst, i, value, nlst
        ([1, 2, 3], 5, 0, [1, 2, 3, 0, 0, 0]),  # lst, i, value, nlst
        ([1, 2, 3], 7, 0, [1, 2, 3, 0, 0, 0, 0, 0]),  # lst, i, value, nlst
    )
    for lst, i, value, nlst in tdata:
        modeleditor.extendlist(lst, i, value=value)
        assert lst == nlst


def test_newrawobject():
    """py.test for newrawobject"""
    thedata = (
        (
            'zone'.upper(),
            [
                'ZONE', '', 0., 0., 0., 0., 1, 1, 'autocalculate',
                'autocalculate', 'autocalculate', '', '', 'Yes'
            ]
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
                'ZONE', '', '0', '0', '0', '0', '1', '1', 'autocalculate',
                'autocalculate', 'autocalculate', '', '', 'Yes'
            ]
        ),  # obj
    )
    for obj in thedata:
        key_i = data.dtls.index(obj[0].upper())
        abunch = idfreader.makeabunch(commdct, obj, key_i)
        result = modeleditor.obj2bunch(data, commdct, obj)
        assert result.__repr__() == abunch.__repr__()


def test_namebunch():
    """py.test for namebunch"""
    thedata = (
        (
            Bunch(dict(Name="", a=5)),
            "yay", "yay"
        ),  # abunch, aname, thename
        (
            Bunch(dict(Name=None, a=5)),
            "yay", None
        ),  # abunch, aname, thename
    )
    for abunch, aname, thename in thedata:
        result = modeleditor.namebunch(abunch, aname)
        assert result.Name == thename


def test_addobject():
    """py.test for addobject"""
    thedata = (
        # key, aname, fielddict
        ('ZONE', None, dict(Name="Gumby", X_Origin=50)),
        ('ZONE', 'karamba', {}),  # key, aname, fielddict
        ('ZONE', None, {}),  # key, aname, fielddict
        # key, aname, fielddict
        ('ZONE', None, dict(Name="Gumby", X_Origin=50)),
    )
    for key, aname, fielddict in thedata:
        result = modeleditor.addobject(
            bunchdt, data, commdct,
            key, aname, **fielddict)
        assert bunchdt[key][-1].key == key  # wierd, but correct :-)
        if aname:
            assert data.dt[key][-1][1] == aname
            assert bunchdt[key][-1].Name == aname
        if fielddict:
            for kkey, value in list(fielddict.items()):
                assert bunchdt[key][-1][kkey] == value


def test_getnamedargs():
    """py.test for getnamedargs"""
    result = dict(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(dict(a=1, b=2, c=3))
    assert result == modeleditor.getnamedargs(dict(a=1, b=2), c=3)
    assert result == modeleditor.getnamedargs(dict(a=1), c=3, b=2)


def test_addobject1():
    """py.test for addobject"""
    thedata = (
        ('ZONE', {'Name': 'karamba'}),  # key, kwargs
    )
    for key, kwargs in thedata:
        result = modeleditor.addobject1(bunchdt, data, commdct, key, **kwargs)
        aname = kwargs['Name']
        assert data.dt[key][-1][1] == aname
        assert bunchdt[key][-1].Name == aname


def test_getobject():
    """py.test for getobject"""
    thedata = (
        ('ZONE', 'PLENUM-1', bunchdt['ZONE'][0]),  # key, name, theobject
        # key, name, theobject
        ('ZONE', 'PLENUM-1'.lower(), bunchdt['ZONE'][0]),
        ('ZONE', 'PLENUM-A', None),  # key, name, theobject
        ('ZONEHVAC:EQUIPMENTCONNECTIONS', 'SPACE1-1',
         bunchdt['ZONEHVAC:EQUIPMENTCONNECTIONS'][0]),  # key, name, theobject
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
            bunchdt, data, commdct,
            key, **fielddict)
        idfobject.Name = aname  # modify the name, to check for a False return
        result = modeleditor.__objecthasfields(
            bunchdt, data, commdct,
            idfobject, **fielddict)
        assert result == istrue


def test_getobjects():
    """py.test for getobjects"""
    thedata = (
        ('ZONE', {'Name': 'PLENUM-1'}, 7, bunchdt['ZONE'][0:1]),
        # key, fielddict, places, theobjects
        # ('ZONE', {'Name':'PLENUM-1', 'Volume':283.2},7,bunchdt['ZONE'][0:1]),
        # key, fielddict, places, theobjects
        # ('ZONE', {'Y_Origin':0.}, 7, bunchdt['ZONE']),
        # key, fielddict, places, theobjects
    )
    for key, fielddict, places, theobjects in thedata:
        result = modeleditor.getobjects(
            bunchdt, data, commdct,
            key, **fielddict)
        assert result == theobjects


def test_is_retaincase():
    """py.test for is_retaincase"""
    thedata = (
        ("BUILDING", 'Name', True),  # key, fieldname, case
        ("BUILDING", 'Terrain', False),  # key, fieldname, case
    )
    for key, fieldname, case in thedata:
        idfobject = bunchdt[key][0]
        result = modeleditor.is_retaincase(
            bunchdt, data, commdct,
            idfobject, fieldname)
        assert result == case


def test_isfieldvalue():
    """py.test for isfieldvalue"""
    thedata = (
        ("BUILDING", 0, 'Name', "Building", 7, True),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, 'Name', "BuildinG", 7, False),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, 'North_Axis', 30, 7, True),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, 'North_Axis', "30", 7, True),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, 'North_Axis', 30.001, 7, False),
        # key, objindex1, fieldname, value, places, isequal
        ("BUILDING", 0, 'North_Axis', 30.001, 2, True),
        # key, objindex1, fieldname, value, places, isequal
        ("ZONE", 0, 'Volume', 283.2, 2, True),
        # key, objindex1, fieldname, value, places, isequal
    )
    for key, objindex1, fieldname, value, places, isequal in thedata:
        idfobject = bunchdt[key][objindex1]
        result = modeleditor.isfieldvalue(
            bunchdt, data, commdct,
            idfobject, fieldname, value, places)
        assert result == isequal


def test_equalfield():
    """py.test for equalfield"""
    thedata = (
        ("BUILDING", 0, 1, 'Name', 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 2, 'Name', 7, False),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, 'Terrain', 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, 'Terrain', 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, 'North_Axis', 7, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 2, 'North_Axis', 2, True),
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 3, 'Maximum_Number_of_Warmup_Days', 7, True),
        ("BUILDING", 0, 3, 'Minimum_Number_of_Warmup_Days', 7, False),
        # key, objindex1, objeindex2, fieldname, places, isequal
    )
    for key, objindex1, objindex2, fieldname, places, isequal in thedata:
        idfobject1 = bunchdt[key][objindex1]
        idfobject2 = bunchdt[key][objindex2]
        result = modeleditor.equalfield(
            bunchdt, data, commdct,
            idfobject1, idfobject2, fieldname, places)
        assert result == isequal
    (key, objindex1, objeindex2,
     fieldname, places, isequal) = ("BUILDING", 0, 1, 'Name', 7, True)
    idfobject1 = bunchdt[key][objindex1]
    idfobject2 = bunchdt["ZONE"][objindex2]
    with pytest.raises(modeleditor.NotSameObjectError):
        modeleditor.equalfield(
            bunchdt, data, commdct,
            idfobject1, idfobject2, fieldname, places)


def test_iddofobject():
    """py.test of iddofobject"""
    thedata = (
        (
            'VERSION',
            [
                {'format': ['singleLine'], 'unique-object': ['']},
                {
                    'default': ['7.0'], 'field': ['Version Identifier'],
                    'required-field': ['']
                }
            ]
        ),  # key, itsidd
    )
    for key, itsidd in thedata:
        result = modeleditor.iddofobject(data, commdct, key)
        try:
            result[0].pop('memo')  # memo is new in version 8.0.0
        except KeyError:
            pass
        assert result == itsidd


def test_removeextensibles():
    """py.test for removeextensibles"""
    thedata = (
        (
            "BuildingSurface:Detailed".upper(), "WALL-1PF",
            [
                "BuildingSurface:Detailed", "WALL-1PF", "WALL",
                "WALL-1", "PLENUM-1",
                "Outdoors", "", "SunExposed", "WindExposed", 0.50000, '4',
            ]
        ),  # key, objname, rawobject
    )
    for key, objname, rawobject in thedata:
        result = modeleditor.removeextensibles(
            bunchdt, data, commdct, key,
            objname)
        assert result.obj == rawobject


def test_getrefnames():
    """py.test for getrefnames"""
    tdata = (
        (
            'ZONE',
            [
                'ZoneNames', 'OutFaceEnvNames', 'ZoneAndZoneListNames',
                'AirflowNetworkNodeAndZoneNames'
            ]
        ),  # objkey, therefs
        (
            'FluidProperties:Name'.upper(),
            ['FluidNames', 'FluidAndGlycolNames']
        ),  # objkey, therefs
        ('Building'.upper(), []),  # objkey, therefs
    )
    for objkey, therefs in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = modeleditor.getrefnames(idf, objkey)
        assert result == therefs


def test_getallobjlists():
    """py.test for getallobjlists"""
    tdata = (
        (
            'TransformerNames',
            [
                (
                    'ElectricLoadCenter:Distribution'.upper(),
                    'TransformerNames',
                    [10, ]
                ),
            ],
        ),  # refname, objlists
    )
    for refname, objlists in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = modeleditor.getallobjlists(idf, refname)
        assert result == objlists


def test_rename():
    """py.test for rename"""
    idftxt = """Material,
      G01a 19mm gypsum board,  !- Name
      MediumSmooth,            !- Roughness
      0.019,                   !- Thickness {m}
      0.16,                    !- Conductivity {W/m-K}
      800,                     !- Density {kg/m3}
      1090;                    !- Specific Heat {J/kg-K}

      Construction,
        Interior Wall,           !- Name
        G01a 19mm gypsum board,  !- Outside Layer
        F04 Wall air space resistance,  !- Layer 2
        G01a 19mm gypsum board;  !- Layer 3

    """
    ridftxt = """Material,
      peanut butter,  !- Name
      MediumSmooth,            !- Roughness
      0.019,                   !- Thickness {m}
      0.16,                    !- Conductivity {W/m-K}
      800,                     !- Density {kg/m3}
      1090;                    !- Specific Heat {J/kg-K}

      Construction,
        Interior Wall,           !- Name
        peanut butter,  !- Outside Layer
        F04 Wall air space resistance,  !- Layer 2
        peanut butter;  !- Layer 3

    """
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    result = modeleditor.rename(
        idf,
        'Material'.upper(),
        'G01a 19mm gypsum board', 'peanut butter')
    assert result.Name == 'peanut butter'
    assert idf.idfobjects['CONSTRUCTION'][0].Outside_Layer == 'peanut butter'
    assert idf.idfobjects['CONSTRUCTION'][0].Layer_3 == 'peanut butter'


def test_zonearea_zonevolume():
    """py.test for zonearea and zonevolume"""
    idftxt = """Zone, 473222, 0.0, 0.0, 0.0, 0.0, , 1;
        BuildingSurface:Detailed, F7289B, Floor, Exterior Floor, 473222,
        Ground, ,
        NoSun, NoWind, , 4, 2.23, 2.56, 0.0, 2.23, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        2.56, 0.0;  BuildingSurface:Detailed, F3659B, Wall, Exterior Wall,
        473222, Outdoors, , SunExposed, WindExposed, , 4, 2.23, 2.56, 1.49,
        2.23, 2.56, 0.0, 0.0, 2.56, 0.0, 0.0, 2.56, 1.49;
        BuildingSurface:Detailed, 46C6C9, Wall, Exterior Wall, 473222,
        Outdoors, , SunExposed, WindExposed, , 4, 2.23, 0.0, 1.49, 2.23,
        0.0, 0.0, 2.23, 1.02548139464, 0.0, 2.23, 1.02548139464, 1.49;
        BuildingSurface:Detailed, 4287DD, Wall, Exterior Wall, 473222,
        Outdoors, , SunExposed, WindExposed, , 4, 0.0, 2.56, 1.49, 0.0,
        2.56, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.49;
        BuildingSurface:Detailed, 570C2E, Wall, Exterior Wall, 473222,
        Outdoors, , SunExposed, WindExposed, , 4, 0.0, 0.0, 1.49, 0.0, 0.0,
        0.0, 2.23, 0.0, 0.0, 2.23, 0.0, 1.49;  BuildingSurface:Detailed,
        BAEA99, Roof, Exterior Roof, 473222, Outdoors, , SunExposed,
        WindExposed, , 4, 0.0, 2.56, 1.49, 0.0, 0.0, 1.49, 2.23, 0.0, 1.49,
        2.23, 2.56, 1.49;  BuildingSurface:Detailed, C879FE, Floor,
        Exterior Floor, 473222, Ground, , NoSun, NoWind, , 4, 3.22,
        2.52548139464, 0.0, 3.22, 1.02548139464, 0.0, 2.23,
        1.02548139464, 0.0, 2.23, 2.52548139464, 0.0;
        BuildingSurface:Detailed, 25B601, Wall, Exterior Wall, 473222,
        Outdoors, , SunExposed, WindExposed, , 4, 2.23,
        1.02548139464, 1.49, 2.23, 1.02548139464, 0.0, 2.23, 2.52548139464,
        0.0, 2.23, 2.52548139464, 1.49;  BuildingSurface:Detailed, F5EADC,
        Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, ,
        4, 2.23, 1.02548139464, 1.49, 2.23, 1.02548139464, 0.0, 3.22,
        1.02548139464, 0.0, 3.22, 1.02548139464, 1.49;
        BuildingSurface:Detailed, D0AABE, Wall, Exterior Wall, 473222,
        Outdoors, , SunExposed, WindExposed, , 4, 3.22, 1.02548139464,
        1.49, 3.22, 1.02548139464, 0.0, 3.22, 2.52548139464, 0.0, 3.22,
        2.52548139464, 1.49;  BuildingSurface:Detailed, B0EA02, Wall,
        Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, ,
        4, 3.22, 2.52548139464, 1.49, 3.22, 2.52548139464, 0.0, 2.23,
        2.52548139464, 0.0, 2.23, 2.52548139464, 1.49;
        BuildingSurface:Detailed, E6DF3B, Roof, Exterior Roof, 473222,
        Outdoors, , SunExposed, WindExposed, , 4, 2.23, 2.52548139464, 1.49,
        2.23, 1.02548139464, 1.49, 3.22, 1.02548139464, 1.49, 3.22,
        2.52548139464, 1.49;  BuildingSurface:Detailed, 4F8681, Wall,
        Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4,
        2.23, 2.52548139464, 1.49, 2.23, 2.52548139464, 0.0, 2.23, 2.56,
        0.0, 2.23, 2.56, 1.49;  """
    idf = IDF(StringIO(idftxt))
    result = modeleditor.zonearea(idf, '473222')
    assert almostequal(result, 7.1938)
    result = modeleditor.zonearea_floor(idf, '473222')
    assert almostequal(result, 7.1938)
    result = modeleditor.zonearea_roofceiling(idf, '473222')
    assert almostequal(result, 7.1938)
    result = modeleditor.zone_floor2roofheight(idf, '473222')
    assert almostequal(result, 1.49)
    result = modeleditor.zoneheight(idf, '473222')
    assert almostequal(result, 1.49)
    result = modeleditor.zone_floor2roofheight(idf, '473222')
    assert almostequal(result, 1.49)
    result = modeleditor.zonevolume(idf, '473222')
    assert almostequal(result, 10.718762)
    # remove floor
    zone = idf.getobject('ZONE', '473222')
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == 'FLOOR']
    for floor in floors:
        idf.removeidfobject(floor)
    result = modeleditor.zonearea_floor(idf, '473222')
    assert almostequal(result, 0)
    result = modeleditor.zonearea_roofceiling(idf, '473222')
    assert almostequal(result, 7.1938)
    result = modeleditor.zonearea(idf, '473222')
    assert almostequal(result, 7.1938)
    result = modeleditor.zoneheight(idf, '473222')
    assert almostequal(result, 1.49)
    result = modeleditor.zonevolume(idf, '473222')
    assert almostequal(result, 10.718762)
    # reload idf and remove roof/ceiling
    idf = IDF(StringIO(idftxt))
    zone = idf.getobject('ZONE', '473222')
    surfs = idf.idfobjects['BuildingSurface:Detailed'.upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == 'ROOF']
    ceilings = [s for s in zone_surfs if s.Surface_Type.upper() == 'CEILING']
    topsurfaces = roofs + ceilings
    for surf in topsurfaces:
        idf.removeidfobject(surf)
    result = modeleditor.zonearea_roofceiling(idf, '473222')
    assert almostequal(result, 0)
    result = modeleditor.zonearea(idf, '473222')
    assert almostequal(result, 7.1938)
    result = modeleditor.zoneheight(idf, '473222')
    assert almostequal(result, 1.49)
    result = modeleditor.zonevolume(idf, '473222')
    assert almostequal(result, 10.718762)


def test_new():
    """py.test for IDF.new()"""
    idf = IDF()
    idf.new()
    # assert idf.idfobjects['building'.upper()] == Idf_MSequence()
    assert idf.idfobjects['building'.upper()].list1 == []
    assert idf.idfobjects['building'.upper()].list2 == []


def test_newidfobject():
    """py.test for newidfobject"""
    # make a blank idf
    # make a function for this and then continue.
    idf = IDF()
    idf.new()
    objtype = 'material:airgap'.upper()
    obj = idf.newidfobject(objtype, Name='Argon')
    obj = idf.newidfobject(objtype, Name='Krypton')
    obj = idf.newidfobject(objtype, Name='Xenon')
    assert idf.model.dt[objtype] == [['MATERIAL:AIRGAP', 'Argon'],
                                     ['MATERIAL:AIRGAP', 'Krypton'],
                                     ['MATERIAL:AIRGAP', 'Xenon'],
                                     ]
    # remove an object
    idf.popidfobject(objtype, 1)
    assert idf.model.dt[objtype] == [['MATERIAL:AIRGAP', 'Argon'],
                                     ['MATERIAL:AIRGAP', 'Xenon'],
                                     ]
    lastobject = idf.idfobjects[objtype][-1]
    idf.removeidfobject(lastobject)
    assert idf.model.dt[objtype] == [['MATERIAL:AIRGAP', 'Argon'], ]
    # copyidfobject
    onlyobject = idf.idfobjects[objtype][0]
    idf.copyidfobject(onlyobject)

    assert idf.model.dt[objtype] == [['MATERIAL:AIRGAP', 'Argon'],
                                     ['MATERIAL:AIRGAP', 'Argon'],
                                     ]


def test_save():
    """
    Test the IDF.save() function using a filehandle to avoid external effects.
    """
    file_text = "Material,TestMaterial,  !- Name"
    idf = IDF(StringIO(file_text))
    # test save with just a filehandle
    file_handle = StringIO()
    idf.save(file_handle)
    expected = "TestMaterial"
    file_handle.seek(0)
    result = file_handle.read()
    # minimal test that TestMaterial is being written to the file handle
    assert expected in result


def test_save_with_lineendings_and_encodings():
    """
    Test the IDF.save() function with combinations of encodings and line 
    endings.

    """
    file_text = "Material,TestMaterial,  !- Name"
    idf = IDF(StringIO(file_text))
    lineendings = ('windows', 'unix', 'default')
    encodings = ('ascii', 'latin-1', 'UTF-8')

    for le, enc in product(lineendings, encodings):
        file_handle = StringIO()
        idf.save(file_handle, encoding=enc, lineendings=le)
        file_handle.seek(0)
        result = file_handle.read().encode(enc)
        if le == 'windows':
            assert b'\r\n' in result
        elif le == 'unix':
            assert b'\r\n' not in result
        elif le == 'default':
            assert os.linesep.encode(enc) in result


def test_saveas():
    """Test the IDF.saveas() function.
    """
    file_text = "Material,TestMaterial,  !- Name"
    idf = IDF(StringIO(file_text))
    idf.idfname = 'test.idf'

    try:
        idf.saveas()  # this should raise an error as no filename is passed
        assert False
    except TypeError:
        pass

    file_handle = StringIO()
    idf.saveas(file_handle)  # save with a filehandle
    expected = "TestMaterial"
    file_handle.seek(0)
    result = file_handle.read()
    assert expected in result

    # test the idfname attribute has been changed
    assert idf.idfname != 'test.idf'


def test_savecopy():
    """Test the IDF.savecopy() function.
    """
    file_text = "Material,TestMaterial,  !- Name"
    idf = IDF(StringIO(file_text))
    idf.idfname = 'test.idf'

    try:
        idf.savecopy()  # this should raise an error as no filename is passed
        assert False
    except TypeError:
        pass

    file_handle = StringIO()
    idf.savecopy(file_handle)  # save a copy with a different filename
    expected = "TestMaterial"
    file_handle.seek(0)
    result = file_handle.read()
    assert expected in result

    # test the idfname attribute has not been changed
    assert idf.idfname == 'test.idf'


def test_initread():
    """Test for IDF.initread() with filename in unicode and as python str.
    """
    # setup
    idf = IDF()
    idf.initreadtxt(idfsnippet)
    idf.saveas('tmp.idf')

    # test fname as unicode
    fname = str('tmp.idf')
    assert type(fname) == str
    idf = IDF()
    idf.initread(fname)
    assert idf.getobject('BUILDING', 'Building')

    # test fname as str
    fname = str('tmp.idf')
    assert type(fname) == str
    idf = IDF()
    idf.initread(fname)
    assert idf.getobject('BUILDING', 'Building')

    # test that a nonexistent file raises an IOError
    fname = "notarealfilename.notreal"
    idf = IDF()
    try:
        idf.initread(fname)
        assert False  # shouldn't reach here
    except IOError:
        pass

    # teardown
    os.remove('tmp.idf')


def test_initreadtxt():
    """Test for IDF.initreadtxt().
    """
    idftxt = """
        Material,
          G01a 19mm gypsum board,  !- Name
          MediumSmooth,            !- Roughness
          0.019,                   !- Thickness {m}
          0.16,                    !- Conductivity {W/m-K}
          800,                     !- Density {kg/m3}
          1090;                    !- Specific Heat {J/kg-K}
        
        Construction,
          Interior Wall,           !- Name
          G01a 19mm gypsum board,  !- Outside Layer
          F04 Wall air space resistance,  !- Layer 2
          G01a 19mm gypsum board;  !- Layer 3
        """
    idf = IDF()
    idf.initreadtxt(idftxt)
    assert idf.getobject('MATERIAL', 'G01a 19mm gypsum board')


def test_idfstr():
    """Test all outputtype options in IDF.idfstr().
    """
    idf = IDF()
    idf.initreadtxt(idfsnippet)
    assert idf.outputtype == 'standard'  # start with the default
    original = idf.idfstr()
    assert "!-" in original  # has comment
    assert "\n" in original  # has line break
    assert "\n\n" in original  # has empty line

    idf.outputtype = 'standard'
    s = idf.idfstr()
    assert "!-" in s  # has comment
    assert "\n" in s  # has line break
    assert "\n\n" in s  # has empty line
    assert s == original  # is unchanged

    idf.outputtype = 'nocomment'
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" in s  # has line break
    assert "\n\n" in s  # has empty line
    assert s != original  # is changed

    idf.outputtype = 'nocomment1'
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" in s  # has line break
    assert "\n\n" in s  # has empty lines
    assert s != original  # is changed

    idf.outputtype = 'nocomment2'
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" in s  # has line break
    assert "\n\n" not in s  # has no empty lines
    assert s != original  # is changed

    idf.outputtype = 'compressed'
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" not in s  # has no line breaks
    assert "\n\n" not in s  # has no empty lines
    assert s != original  # is changed
