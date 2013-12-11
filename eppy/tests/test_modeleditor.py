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

"""py.test for modeleditor"""
import pytest
from eppy.pytest_helpers import almostequal

import bunch
import eppy.idfreader as idfreader
import eppy.modeleditor as modeleditor
import eppy.snippet as snippet
from eppy.modeleditor import IDF

from eppy.iddcurrent import iddcurrent
iddsnippet = iddcurrent.iddtxt

idfsnippet = snippet.idfsnippet

from StringIO import StringIO
idffhandle = StringIO(idfsnippet)
iddfhandle = StringIO(iddsnippet)
bunchdt, data, commdct = idfreader.idfreader(idffhandle, iddfhandle)

# idd is read only once in this test
# if it has already been read from some other test, it will continue with the old reading
from eppy.iddcurrent import iddcurrent
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_poptrailing():
    """py.test for poptrailing"""
    data = (([1, 2, 3, '', 56, '', '', '', ''], 
        [1, 2, 3, '', 56]), # lst, poped
        ([1, 2, 3, '', 56], 
        [1, 2, 3, '', 56]), # lst, poped
        ([1, 2, 3, 56], 
        [1, 2, 3, 56]), # lst, poped
    )

def test_extendlist():
    """py.test for extendlist"""
    data = (([1,2,3], 2, 0, [1,2,3]), # lst, i, value, nlst
    ([1,2,3], 3, 0, [1,2,3,0]), # lst, i, value, nlst
    ([1,2,3], 5, 0, [1,2,3,0,0,0]), # lst, i, value, nlst
    ([1,2,3], 7, 0, [1,2,3,0,0,0,0,0]), # lst, i, value, nlst
    )
    for lst, i, value, nlst in data:
        modeleditor.extendlist(lst, i, value=value)
        assert lst == nlst

def test_newrawobject():
    """py.test for newrawobject"""
    thedata = (('zone'.upper(), 
        ['ZONE', '', 0., 0., 0., 0., 1, 1, 'autocalculate', 
            'autocalculate', 'autocalculate', '', '', 'Yes']), # key, obj
    )
    for key, obj in thedata:
        result = modeleditor.newrawobject(data, commdct, key)
        assert result == obj
        
def test_obj2bunch():
    """py.test for obj2bunch"""
    thedata = ((['ZONE', '', '0', '0', '0', '0', '1', '1', 'autocalculate', 
        'autocalculate', 'autocalculate', '', '', 'Yes']), # obj
    )
    for obj in thedata:
        key_i = data.dtls.index(obj[0].upper())
        abunch = idfreader.makeabunch(commdct, obj, key_i)
        result = modeleditor.obj2bunch(data, commdct, obj)
        assert result.__repr__() == abunch.__repr__()
    
def test_namebunch():
    """py.test for namebunch"""
    thedata = ((bunch.Bunch(dict(Name="", a=5)), 
        "yay", "yay"), # abunch, aname, thename
        (bunch.Bunch(dict(Name=None, a=5)), 
            "yay", None), # abunch, aname, thename
    )
    for abunch, aname, thename in thedata:
        result = modeleditor.namebunch(abunch, aname)
        assert result.Name == thename
        
def test_addobject():
    """py.test for addobject"""
    thedata = (
    ('ZONE', None, dict(Name="Gumby", X_Origin=50)), # key, aname, fielddict
    ('ZONE', 'karamba', {}), # key, aname, fielddict
    ('ZONE', None, {}), # key, aname, fielddict
    ('ZONE', None, dict(Name="Gumby", X_Origin=50)), # key, aname, fielddict
    )
    for key, aname, fielddict in thedata:
        result = modeleditor.addobject(bunchdt, data, commdct, 
            key, aname, **fielddict)
        assert bunchdt[key][-1].key == key # wierd, but correct :-)
        if aname:
            assert data.dt[key][-1][1] == aname
            assert bunchdt[key][-1].Name == aname
        if fielddict:
            for k, v in fielddict.items():
                assert bunchdt[key][-1][k] == v
        
def test_getnamedargs():
    """py.test for getnamedargs"""
    result = dict(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(dict(a=1, b=2, c=3))
    assert result == modeleditor.getnamedargs(dict(a=1, b=2), c=3)
    assert result == modeleditor.getnamedargs(dict(a=1), c=3, b=2)
    
def test_addobject1():
    """py.test for addobject"""
    thedata = (('ZONE', {'Name':'karamba'}), # key, kwargs
    )
    for key, kwargs in thedata:
        result = modeleditor.addobject1(bunchdt, data, commdct, key, **kwargs)
        aname = kwargs['Name']
        assert data.dt[key][-1][1] == aname
        assert bunchdt[key][-1].Name == aname        
        
def test_getobject():
    """py.test for getobject"""
    thedata = (
        ('ZONE', 'PLENUM-1', 
            bunchdt['ZONE'][0]), # key, name, theobject
        ('ZONE', 'PLENUM-1'.lower(), 
            bunchdt['ZONE'][0]), # key, name, theobject
        ('ZONE', 'PLENUM-A', 
            None), # key, name, theobject
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
        idfobject = modeleditor.addobject(bunchdt, data, commdct, 
            key, **fielddict)
        idfobject.Name = aname # modify the name, to check for a False return
        result = modeleditor.__objecthasfields(bunchdt, data, commdct, 
            idfobject, **fielddict)
        assert result == istrue


def test_getobjects():
    """py.test for getobjects"""
    thedata = (
    ('ZONE', {'Name':'PLENUM-1'}, 7, bunchdt['ZONE'][0:1]), 
    # key, fielddict, places, theobjects
    # ('ZONE', {'Name':'PLENUM-1', 'Volume':283.2}, 7, bunchdt['ZONE'][0:1]), 
    # # key, fielddict, places, theobjects
    # ('ZONE', {'Y_Origin':0.}, 7, bunchdt['ZONE']), 
    # # key, fielddict, places, theobjects
    )
    for key, fielddict, places, theobjects in thedata:
        result = modeleditor.getobjects(bunchdt, data, commdct, 
            key, **fielddict)
        assert result == theobjects

def test_is_retaincase():
    """py.test for is_retaincase"""
    thedata = (
    ("BUILDING", 'Name', True), # key, fieldname, case
    ("BUILDING", 'Terrain', False), # key, fieldname, case
    )    
    for key, fieldname, case in thedata:
        idfobject = bunchdt[key][0]
        result = modeleditor.is_retaincase(bunchdt, data, commdct, 
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
        result = modeleditor.isfieldvalue(bunchdt, data, commdct, 
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
        result = modeleditor.equalfield(bunchdt, data, commdct, 
            idfobject1, idfobject2, fieldname, places)
        assert result == isequal
    (key, objindex1, objeindex2, 
        fieldname, places, isequal) = ("BUILDING", 0, 1, 'Name', 7, True)
    idfobject1 = bunchdt[key][objindex1]
    idfobject2 = bunchdt["ZONE"][objindex2]
    with pytest.raises(modeleditor.NotSameObjectError):
        modeleditor.equalfield(bunchdt, data, commdct, 
            idfobject1, idfobject2, fieldname, places)
            
def test_iddofobject():
    """py.test of iddofobject"""
    thedata = (('VERSION', 
                [{'format': ['singleLine'], 'unique-object': ['']},
                {'default': ['7.0'], 'field': ['Version Identifier'], 
                'required-field': ['']}]), # key, itsidd
    )
    for key, itsidd in thedata:
        result = modeleditor.iddofobject(data, commdct, key)
        result[0].pop('memo') # memo is new in version 8.0.0
        assert result == itsidd


def test_removeextensibles():
    """py.test for removeextensibles"""
    thedata = (("BuildingSurface:Detailed".upper(), "WALL-1PF",
    ["BuildingSurface:Detailed", "WALL-1PF", "WALL", "WALL-1", "PLENUM-1", 
    "Outdoors","", "SunExposed", "WindExposed", 0.50000, '4',] ), # key, objname, rawobject
    )
    for key, objname, rawobject in thedata:
        result = modeleditor.removeextensibles(bunchdt, data, commdct, key, 
                                                objname)
        assert result.obj == rawobject
        
        
def test_addthisbunch():
    """py.test for addthisbunch"""
    obj1 = ['ZONE', 'weird zone', '0', '0', '0', '0', '1', '1', 'autocalculate', 
        'autocalculate', 'autocalculate', '', '', 'Yes']
    thisbunch = modeleditor.obj2bunch(data, commdct, obj1)
    modeleditor.addthisbunch(bunchdt, data, commdct, thisbunch)
    print data.dt["ZONE"][-1]
    assert data.dt["ZONE"][-1] == obj1
    
def test_getrefnames():
    """py.test for getrefnames"""
    tdata = (
    ('ZONE', 
    ['ZoneNames', 'OutFaceEnvNames', 'ZoneAndZoneListNames', 
    'AirflowNetworkNodeAndZoneNames']), # objkey, therefs
    ('FluidProperties:Name'.upper(), 
    ['FluidNames', 'FluidAndGlycolNames']), # objkey, therefs
    ('Building'.upper(), 
    []), # objkey, therefs
    )
    for objkey, therefs in tdata:
        fhandle = StringIO("")
        idf = IDF(fhandle)
        result = modeleditor.getrefnames(idf, objkey)
        assert result == therefs

def test_getallobjlists():
    """py.test for getallobjlists"""
    tdata = (
    ('TransformerNames', 
    [('ElectricLoadCenter:Distribution'.upper(), 
    'TransformerNames',
    [10, ]
    ), ],
    ), # refname, objlists
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
    result = modeleditor.rename(idf, 
            'Material'.upper(), 
            'G01a 19mm gypsum board', 'peanut butter')
    assert result.Name == 'peanut butter'
    assert idf.idfobjects['CONSTRUCTION'][0].Outside_Layer == 'peanut butter'                       
    assert idf.idfobjects['CONSTRUCTION'][0].Layer_3 == 'peanut butter'        
    
def test_zonearea_zonevolume():
    """py.test for zonearea and zonevolume"""
    idftxt = "Zone, 473222, 0.0, 0.0, 0.0, 0.0, , 1;  BuildingSurface:Detailed, F7289B, Floor, Exterior Floor, 473222, Ground, , NoSun, NoWind, , 4, 2.23, 2.56, 0.0, 2.23, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.56, 0.0;  BuildingSurface:Detailed, F3659B, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 2.23, 2.56, 1.49, 2.23, 2.56, 0.0, 0.0, 2.56, 0.0, 0.0, 2.56, 1.49;  BuildingSurface:Detailed, 46C6C9, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 2.23, 0.0, 1.49, 2.23, 0.0, 0.0, 2.23, 1.02548139464, 0.0, 2.23, 1.02548139464, 1.49;  BuildingSurface:Detailed, 4287DD, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 0.0, 2.56, 1.49, 0.0, 2.56, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.49;  BuildingSurface:Detailed, 570C2E, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 0.0, 0.0, 1.49, 0.0, 0.0, 0.0, 2.23, 0.0, 0.0, 2.23, 0.0, 1.49;  BuildingSurface:Detailed, BAEA99, Roof, Exterior Roof, 473222, Outdoors, , SunExposed, WindExposed, , 4, 0.0, 2.56, 1.49, 0.0, 0.0, 1.49, 2.23, 0.0, 1.49, 2.23, 2.56, 1.49;  BuildingSurface:Detailed, C879FE, Floor, Exterior Floor, 473222, Ground, , NoSun, NoWind, , 4, 3.22, 2.52548139464, 0.0, 3.22, 1.02548139464, 0.0, 2.23, 1.02548139464, 0.0, 2.23, 2.52548139464, 0.0;  BuildingSurface:Detailed, 25B601, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 2.23, 1.02548139464, 1.49, 2.23, 1.02548139464, 0.0, 2.23, 2.52548139464, 0.0, 2.23, 2.52548139464, 1.49;  BuildingSurface:Detailed, F5EADC, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 2.23, 1.02548139464, 1.49, 2.23, 1.02548139464, 0.0, 3.22, 1.02548139464, 0.0, 3.22, 1.02548139464, 1.49;  BuildingSurface:Detailed, D0AABE, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 3.22, 1.02548139464, 1.49, 3.22, 1.02548139464, 0.0, 3.22, 2.52548139464, 0.0, 3.22, 2.52548139464, 1.49;  BuildingSurface:Detailed, B0EA02, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 3.22, 2.52548139464, 1.49, 3.22, 2.52548139464, 0.0, 2.23, 2.52548139464, 0.0, 2.23, 2.52548139464, 1.49;  BuildingSurface:Detailed, E6DF3B, Roof, Exterior Roof, 473222, Outdoors, , SunExposed, WindExposed, , 4, 2.23, 2.52548139464, 1.49, 2.23, 1.02548139464, 1.49, 3.22, 1.02548139464, 1.49, 3.22, 2.52548139464, 1.49;  BuildingSurface:Detailed, 4F8681, Wall, Exterior Wall, 473222, Outdoors, , SunExposed, WindExposed, , 4, 2.23, 2.52548139464, 1.49, 2.23, 2.52548139464, 0.0, 2.23, 2.56, 0.0, 2.23, 2.56, 1.49;  "
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
        