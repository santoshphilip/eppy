# Copyright (c) 2022, 2024 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test to test extending extensible fields beyond what is in the IDD file"""

from io import StringIO

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF


def setup_module(module):
    """
    idd is read only once in this module
    if it has already been read from some other module, it will continue
    without reading it again

    pytest run this before running the module
    """
    from eppy.iddcurrent import iddcurrent

    iddfhandle = StringIO(iddcurrent.iddtxt)
    if IDF.getiddname() == None:
        IDF.setiddname(iddfhandle)


def test_read_overextended():
    """py.test when reading an IDD that has more fields than the IDD"""
    astr = """
    Version,
        9.6;                      !- Version Identifier

    WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC,
        Gumby,                    !- Name
        55,
        G1,"""

    # nn = 5000
    nn = 50
    extfields = ",".join([f"{i}, G{i}" for i in range(nn)])
    newstr = f"{astr} {extfields};"

    fhandle = StringIO(newstr)
    idf = IDF(fhandle)
    wm = idf.idfobjects["WINDOWMATERIAL:GLAZINGGROUP:THERMOCHROMIC"]
    assert wm[0][f"Optical_Data_Temperature_{nn + 1}"] == nn - 1
    assert wm[0][f"Window_Material_Glazing_Name_{nn + 1}"] == f"G{nn - 1}"
    


def test_newidfobject_overextend():
    """py.test when idf.newidfobject creates an object with more fields than avaliable in the IDD"""
    idf = IDF(StringIO(""))
    n = 2000
    d1 = dict(Name="Gumby")
    d2 = {f"Optical_Data_Temperature_{i}": i for i in range(1, n + 1)}
    d3 = {f"Window_Material_Glazing_Name_{i}": f"G{i}" for i in range(1, n + 1)}
    kwargs = dict()
    kwargs.update(d1)
    kwargs.update(d2)
    kwargs.update(d3)
    d4 = {"Window_Material_Glazing_Name_2010": "G2010"}  # skip some numbers
    kwargs.update(d4)
    wm = idf.newidfobject("WindowMaterial:GlazingGroup:Thermochromic", **kwargs)
    assert wm.Optical_Data_Temperature_2000 == 2000
    assert wm.Window_Material_Glazing_Name_2000 == "G2000"
    assert wm.Window_Material_Glazing_Name_2010 == "G2010"  # test after skiping
    assert wm.Window_Material_Glazing_Name_2005 == ""  # test the skipped fields


def test_getset_overextended():
    """pytest when idfobject.fieldname and idfobject['fieldname'] is an overextended field"""
    idf = IDF(StringIO(""))
    wm = idf.newidfobject("WindowMaterial:GlazingGroup:Thermochromic", Name="Gumby")
    wm.Optical_Data_Temperature_2000 = 2000  # test __setattr__
    assert wm.Optical_Data_Temperature_2000 == 2000
    wm["Optical_Data_Temperature_2001"] = 2001  # rest __setitem__
    assert wm.Optical_Data_Temperature_2001 == 2001
    assert wm.Optical_Data_Temperature_2002 == ""  # test __getattr__
    assert wm["Optical_Data_Temperature_2003"] == ""  # test __getitem__

# test from fixing issue #444 
# issue #444
# 
# :Problem: Extensible fields not expanding automatically in IDD for WINDOWSHADINGCONTROL 
# :Solution: fixed how Extensible fields were identified
# 
# eppy was using the presence of an integer in the extensible field to identify it as extensible. Some non-extensible fields have integers in them. Now eppy identifies the Extensible field by key-words such as begin-extensible
# 
# Below are the tests specific to this issue

def test_read_overextended_issue444():
    """py.test when reading an IDD that has more fields than the IDD. Testing for the fix of issue #444"""
    # # test for fix of issue #444
    # WindowShadingControl has a field called "SetPoint 2" that was messing
    # the extensible fields generation
    astr = """
    Version, 9.6;                               !- Version Identifier

    WindowShadingControl,61013,                       
    BLOC85:RDCCLSSCNTRLC11X3,                      
    ,                                             
    InteriorBlind,                                
    Vitrage_externe_Ecole_De_Lagord - 2013,       
    OnIfScheduleAllows,                            
    PRESENCE_ClasseCentrale,                       
    ,                                              
    Yes,                                           
    No,                                            
    ,                                            
    FixedSlatAngle,                              
    ,                                            
    0,                                           
    ,                                            
    Group,                                         
    FedSurfName1, """

    # nn = 5000
    nn = 50
    extfields = ",".join([f"FedSurfName1{i}" for i in range(nn)])
    newstr = f"{astr} {extfields};"

    fhandle = StringIO(newstr)
    idf = IDF(fhandle)
    wm = idf.idfobjects["WINDOWSHADINGCONTROL"]
    assert wm[0][f"Fenestration_Surface_{nn + 1}_Name"] == f"FedSurfName1{nn - 1}"

def test_newidfobject_overextend_issue444():
    """py.test when idf.newidfobject creates an object with more fields than avaliable in the IDD. Testing for the fix of issue #444"""
    idf = IDF(StringIO(""))
    n = 2000
    d1 = dict(Name="Gumby")
    d2 = {f"Fenestration_Surface_{i}_Name": f"G{i}" for i in range(1, n + 1)}
    kwargs = dict()
    kwargs.update(d1)
    kwargs.update(d2)
    d4 = {"Fenestration_Surface_2010_Name": "G2010"}  # skip some numbers
    kwargs.update(d4)
    wm = idf.newidfobject("WindowShadingControl", **kwargs)
    assert wm.Fenestration_Surface_2000_Name == "G2000"
    assert wm.Fenestration_Surface_2010_Name  == "G2010"  # test after skiping
    assert wm.Fenestration_Surface_2005_Name == ""  # test the skipped fields

def test_getset_overextended_issue444():
    """pytest when idfobject.fieldname and idfobject['fieldname'] is an overextended field. Testing for the fix of issue #444"""
    idf = IDF(StringIO(""))
    wm = idf.newidfobject("WindowShadingControl", Name="Gumby")
    wm.Fenestration_Surface_2000_Name = 2000  # test __setattr__
    assert wm.Fenestration_Surface_2000_Name == 2000
    wm["Fenestration_Surface_2001_Name"] = 2001  # rest __setitem__
    assert wm.Fenestration_Surface_2001_Name == 2001
    assert wm.Fenestration_Surface_2002_Name == ""  # test __getattr__
    assert wm["Fenestration_Surface_2002_Name"] == ""  # test __getitem__


