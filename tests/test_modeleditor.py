# Copyright (c) 2012 Santosh Philip
# Copyright (c) 2021 Jeremy Lerond
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for modeleditor"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from itertools import product
import os
import warnings
import os.path
import shutil
from pathlib import Path


import pytest
from six import StringIO
from six import string_types

from eppy import modeleditor
from eppy.bunch_subclass import Bunch
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal
import eppy.snippet as snippet


iddsnippet = iddcurrent.iddtxt
idfsnippet = snippet.idfsnippet

# idffhandle = StringIO(idfsnippet)
# iddfhandle = StringIO(iddsnippet)
# bunchdt, data, commdct, gdict = idfreader.idfreader(idffhandle, iddfhandle, None)

# idd is read only once in this test
# if it has already been read from some other test, it will continue with
# the old reading
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_poptrailing():
    """py.test for poptrailing"""
    tdata = (
        ([1, 2, 3, "", 56, "", "", "", ""], [1, 2, 3, "", 56]),  # lst, popped
        ([1, 2, 3, "", 56], [1, 2, 3, "", 56]),  # lst, popped
        ([1, 2, 3, 56], [1, 2, 3, 56]),  # lst, popped
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


def test_namebunch():
    """py.test for namebunch"""
    thedata = (
        (Bunch(dict(Name="", a=5)), "yay", "yay"),  # abunch, aname, thename
        (Bunch(dict(Name=None, a=5)), "yay", None),  # abunch, aname, thename
    )
    for abunch, aname, thename in thedata:
        result = modeleditor.namebunch(abunch, aname)
        assert result.Name == thename


def test_getnamedargs():
    """py.test for getnamedargs"""
    result = dict(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(dict(a=1, b=2, c=3))
    assert result == modeleditor.getnamedargs(dict(a=1, b=2), c=3)
    assert result == modeleditor.getnamedargs(dict(a=1), c=3, b=2)


def test_getrefnames():
    """py.test for getrefnames"""
    tdata = (
        (
            "ZONE",
            [
                "ZoneNames",
                "OutFaceEnvNames",
                "ZoneAndZoneListNames",
                "AirflowNetworkNodeAndZoneNames",
            ],
        ),  # objkey, therefs
        (
            "FluidProperties:Name".upper(),
            ["FluidNames", "FluidAndGlycolNames"],
        ),  # objkey, therefs
        ("Building".upper(), []),  # objkey, therefs
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
            "TransformerNames",
            [("ElectricLoadCenter:Distribution".upper(), "TransformerNames", [10])],
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

      Construction,
        Other Wall,           !- Name
        G01a 19mm gypsum board,  !- Outside Layer
        G01a 19mm gypsum board,  !- Layer 2
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

      Construction,
        Other Wall,           !- Name
        peanut butter,  !- Outside Layer
        peanut butter,  !- Layer 2
        peanut butter;  !- Layer 3

    """
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    result = modeleditor.rename(
        idf, "Material".upper(), "G01a 19mm gypsum board", "peanut butter"
    )
    assert result.Name == "peanut butter"
    assert idf.idfobjects["CONSTRUCTION"][0].Outside_Layer == "peanut butter"
    assert idf.idfobjects["CONSTRUCTION"][0].Layer_3 == "peanut butter"


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
    result = modeleditor.zonearea(idf, "473222")
    assert almostequal(result, 7.1938)
    result = modeleditor.zonearea_floor(idf, "473222")
    assert almostequal(result, 7.1938)
    result = modeleditor.zonearea_roofceiling(idf, "473222")
    assert almostequal(result, 7.1938)
    result = modeleditor.zone_floor2roofheight(idf, "473222")
    assert almostequal(result, 1.49)
    result = modeleditor.zoneheight(idf, "473222")
    assert almostequal(result, 1.49)
    result = modeleditor.zone_floor2roofheight(idf, "473222")
    assert almostequal(result, 1.49)
    result = modeleditor.zonevolume(idf, "473222")
    assert almostequal(result, 10.718762)
    # remove floor
    zone = idf.getobject("ZONE", "473222")
    surfs = idf.idfobjects["BuildingSurface:Detailed".upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    floors = [s for s in zone_surfs if s.Surface_Type.upper() == "FLOOR"]
    for floor in floors:
        idf.removeidfobject(floor)
    result = modeleditor.zonearea_floor(idf, "473222")
    assert almostequal(result, 0)
    result = modeleditor.zonearea_roofceiling(idf, "473222")
    assert almostequal(result, 7.1938)
    result = modeleditor.zonearea(idf, "473222")
    assert almostequal(result, 7.1938)
    result = modeleditor.zoneheight(idf, "473222")
    assert almostequal(result, 1.49)
    result = modeleditor.zonevolume(idf, "473222")
    assert almostequal(result, 10.718762)
    # reload idf and remove roof/ceiling
    idf = IDF(StringIO(idftxt))
    zone = idf.getobject("ZONE", "473222")
    surfs = idf.idfobjects["BuildingSurface:Detailed".upper()]
    zone_surfs = [s for s in surfs if s.Zone_Name == zone.Name]
    roofs = [s for s in zone_surfs if s.Surface_Type.upper() == "ROOF"]
    ceilings = [s for s in zone_surfs if s.Surface_Type.upper() == "CEILING"]
    topsurfaces = roofs + ceilings
    for surf in topsurfaces:
        idf.removeidfobject(surf)
    result = modeleditor.zonearea_roofceiling(idf, "473222")
    assert almostequal(result, 0)
    result = modeleditor.zonearea(idf, "473222")
    assert almostequal(result, 7.1938)
    result = modeleditor.zoneheight(idf, "473222")
    assert almostequal(result, 1.49)
    result = modeleditor.zonevolume(idf, "473222")
    assert almostequal(result, 10.718762)


def test_new():
    """py.test for IDF.new()"""
    idf = IDF()
    idf.new()
    # assert idf.idfobjects['building'.upper()] == Idf_MSequence()
    assert idf.idfobjects["building".upper()].list1 == []
    assert idf.idfobjects["building".upper()].list2 == []


def test_newidfobject():
    """py.test for newidfobject"""
    # make a blank idf
    # make a function for this and then continue.
    idf = IDF()
    idf.new()
    objtype = "material:airgap".upper()
    obj = idf.newidfobject(objtype, Name="Argon")
    obj = idf.newidfobject(objtype, Name="Krypton")
    obj = idf.newidfobject(objtype, Name="Xenon")
    assert idf.model.dt[objtype] == [
        ["MATERIAL:AIRGAP", "Argon"],
        ["MATERIAL:AIRGAP", "Krypton"],
        ["MATERIAL:AIRGAP", "Xenon"],
    ]
    # remove an object
    idf.popidfobject(objtype, 1)
    assert idf.model.dt[objtype] == [
        ["MATERIAL:AIRGAP", "Argon"],
        ["MATERIAL:AIRGAP", "Xenon"],
    ]
    lastobject = idf.idfobjects[objtype][-1]
    idf.removeidfobject(lastobject)
    assert idf.model.dt[objtype] == [["MATERIAL:AIRGAP", "Argon"]]
    # copyidfobject
    onlyobject = idf.idfobjects[objtype][0]
    idf.copyidfobject(onlyobject)

    assert idf.model.dt[objtype] == [
        ["MATERIAL:AIRGAP", "Argon"],
        ["MATERIAL:AIRGAP", "Argon"],
    ]
    # remove all objects
    idf.removeallidfobjects(objtype)
    assert len(idf.idfobjects[objtype]) == 0
    # test some functions
    objtype = "FENESTRATIONSURFACE:DETAILED"
    obj = idf.newidfobject(objtype, Name="A Wall")
    assert obj.coords == []
    assert obj.fieldvalues[1] == "A Wall"

    # test defaultvalues=True and defaultvalues=False
    sim_deftrue = idf.newidfobject("SimulationControl".upper(), defaultvalues=True)
    assert sim_deftrue.Do_Zone_Sizing_Calculation == "No"
    sim_deffalse = idf.newidfobject("SimulationControl".upper(), defaultvalues=False)
    assert sim_deffalse.Do_Zone_Sizing_Calculation == ""


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


# Structure of a test:
#
# 1. Arrange -> pytest fixture
# 2. Act
# 3. Assert
# 4. Cleanup -> pytest fixture


@pytest.fixture
def createidfinafolder():
    """make a temp dir and save an idf in it

    :Teardown: remove the temp dir and it'a contents"""
    # make a temp dir
    tdirname = "./atempdir1"
    abspath = os.path.abspath(tdirname)
    os.mkdir(tdirname)
    # make blank file
    idftxt = ""  # empty string
    fhandle = StringIO(idftxt)
    idf = IDF(fhandle)
    # put in some objects - building and version
    building = idf.newidfobject("building")
    building.Name = "Taj"
    idf.newidfobject("version")
    # save it in subdir1
    fname = f"{tdirname}/a.idf"
    idf.saveas(fname)

    yield idf
    # Teardown
    # remove the temp dir
    shutil.rmtree(abspath)
    # abspath ensure removal from any dir


@pytest.fixture
def changedir():
    """make a temp dir and change to that dir

    :Teardown: return to original dir and delete this temp dir"""
    # make a temp dir
    origdir = os.path.abspath(os.path.curdir)
    tdirname = "./atempdir2"
    abspath = os.path.abspath(tdirname)
    os.mkdir(tdirname)
    # change to that directory
    os.chdir(tdirname)
    yield tdirname

    # Teardown
    # remove the temp dir
    os.chdir(origdir)
    shutil.rmtree(abspath)
    # abspath ensure removal from any dir


def test_save_with_dir_change(createidfinafolder, changedir):
    """py.test of save when dir has been changed"""
    change, expected = "Mahal", "Mahal"
    # createidfinafolder creates the idf
    idf = createidfinafolder
    idfabs = idf.idfabsname
    # changedir chnages dir
    newdir = changedir
    # make a change to the idf
    building = idf.idfobjects["building"][0]
    building.Name = change
    # and save while in new dir
    idf.save()  # should save in orig dir
    # read the file again
    idf1 = IDF(idfabs)
    building1 = idf1.idfobjects["building"][0]
    assert building1.Name == expected
    # test if it works with filepath.Path
    fname_path = Path(idfabs)
    assert isinstance(fname_path, Path)
    idf2 = IDF(fname_path)
    building2 = idf2.idfobjects["building"][0]
    assert building2.Name == expected


def test_save_with_lineendings_and_encodings():
    """
    Test the IDF.save() function with combinations of encodings and line
    endings.

    """
    file_text = "Material,TestMaterial,  !- Name"
    idf = IDF(StringIO(file_text))
    lineendings = ("windows", "unix", "default")
    encodings = ("ascii", "latin-1", "UTF-8")

    for le, enc in product(lineendings, encodings):
        file_handle = StringIO()
        idf.save(file_handle, encoding=enc, lineendings=le)
        file_handle.seek(0)
        result = file_handle.read().encode(enc)
        if le == "windows":
            assert b"\r\n" in result
        elif le == "unix":
            assert b"\r\n" not in result
        elif le == "default":
            assert os.linesep.encode(enc) in result


def test_saveas():
    """Test the IDF.saveas() function."""
    file_text = "Material,TestMaterial,  !- Name"
    idf = IDF(StringIO(file_text))
    idf.idfname = "test.idf"

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
    assert idf.idfname != "test.idf"


def test_savecopy():
    """Test the IDF.savecopy() function."""
    file_text = "Material,TestMaterial,  !- Name"
    idf = IDF(StringIO(file_text))
    idf.idfname = "test.idf"

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
    assert idf.idfname == "test.idf"


def test_initread():
    """Test for IDF.initread() with filename in unicode and as python str."""
    # setup
    idf = IDF()
    idf.initreadtxt(idfsnippet)
    idf.saveas("tmp.idf")

    # test fname as unicode
    fname = "tmp.idf"
    assert isinstance(fname, string_types)
    idf = IDF()
    idf.initread(fname)
    assert idf.getobject("BUILDING", "Building")

    # test fname as str
    fname = str("tmp.idf")
    assert isinstance(fname, string_types)
    idf = IDF()
    idf.initread(fname)
    assert idf.getobject("BUILDING", "Building")

    # test that a nonexistent file raises an IOError
    fname = "notarealfilename.notreal"
    idf = IDF()
    try:
        idf.initread(fname)
        assert False  # shouldn't reach here
    except IOError:
        pass

    # teardown
    os.remove("tmp.idf")


def test_initreadtxt():
    """Test for IDF.initreadtxt()."""
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
    assert idf.getobject("MATERIAL", "G01a 19mm gypsum board")


def test_idfstr():
    """Test all outputtype options in IDF.idfstr()."""
    idf = IDF()
    idf.initreadtxt(idfsnippet)
    assert idf.outputtype == "standard"  # start with the default
    original = idf.idfstr()
    assert "!-" in original  # has comment
    assert "\n" in original  # has line break
    assert "\n\n" in original  # has empty line

    idf.outputtype = "standard"
    s = idf.idfstr()
    assert "!-" in s  # has comment
    assert "\n" in s  # has line break
    assert "\n\n" in s  # has empty line
    assert s == original  # is unchanged

    idf.outputtype = "nocomment"
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" in s  # has line break
    assert "\n\n" in s  # has empty line
    assert s != original  # is changed

    idf.outputtype = "nocomment1"
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" in s  # has line break
    assert "\n\n" in s  # has empty lines
    assert s != original  # is changed

    idf.outputtype = "nocomment2"
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" in s  # has line break
    assert "\n\n" not in s  # has no empty lines
    assert s != original  # is changed

    idf.outputtype = "compressed"
    s = idf.idfstr()
    assert "!-" not in s  # has no comments
    assert "\n" not in s  # has no line breaks
    assert "\n\n" not in s  # has no empty lines
    assert s != original  # is changed


def test_refname2key():
    """py.test for refname2key"""
    tdata = (
        (
            "TransformerNames",
            ["ElectricLoadCenter:Distribution".upper()],
        ),  # refname, key
        (
            "AllCurves",
            [
                "PUMP:VARIABLESPEED",
                "PUMP:CONSTANTSPEED",
                "BOILER:HOTWATER",
                "ENERGYMANAGEMENTSYSTEM:CURVEORTABLEINDEXVARIABLE",
            ],
        ),  # refname, key
    )
    for refname, key in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = modeleditor.refname2key(idf, refname)
        assert result == key


def test_getiddgroupdict():
    """py.test for IDF.getiddgroupdict()"""
    data = (({None: ["Lead Input", "Simulation Data"]},),)  # gdict,
    for (gdict,) in data:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = idf.getiddgroupdict()
        assert result[None] == gdict[None]


def test_idfinmsequence():
    """py.test for setting of theidf in Idf_MSequence"""
    idftxt = """Version, 6.0;"""
    # theidf set in Idf_MSequence.__init__
    idf = IDF(StringIO(idftxt))
    versions = idf.idfobjects["version".upper()]
    assert versions.theidf == idf
    assert versions[0].theidf == idf
    # theidf set in Idf_MSequence.insert()
    material = idf.newidfobject("material".upper())
    assert material.theidf == idf
    # theidf set when you pop an item
    newmaterial = idf.newidfobject("material".upper())
    materials = idf.idfobjects["material".upper()]
    material = materials.pop(0)
    assert material.theidf == None
    assert materials[0].theidf == idf


def test_idd_index():
    """py.test to see if idd_index is returned"""
    idftxt = """"""
    idf = IDF(StringIO(idftxt))
    assert idf.idd_index == {}
