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

"""py.test for eplus_functions.py"""

from StringIO import StringIO
import sys
sys.path.append('../EPlusInputcode')

import iddV6_0
from EPlusCode.EPlusInterfaceFunctions import readidf
from EPlusCode.EPlusInterfaceFunctions import parse_idd

import eplus_functions
import idd_fields
import pytest

def test_rename_name():
    """py.test for rename_name"""
    thedata = (("""Zone,SPACE1__1,0,0,0,0,1,1,2.438400269,239.247360229;People,SPACE1__1_People_1,SPACE1__1,OCCUPY__1,people,11,,,0.3,,ActSchd;""",
"ZONE", "SPACE1__1", "LOBBY" ,   
"""Zone,LOBBY,0,0,0,0,1,1,2.438400269,239.247360229;People,SPACE1__1_People_1,LOBBY,OCCUPY__1,people,11,,,0.3,,ActSchd;"""    ),# idftxt, objkey, oldname, newname, newidf
    )
    for idftxt, objkey, oldname, newname, newidf in thedata:
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddfile=iddV6_0.theidd,
                                    commdct=iddV6_0.commdct)
        idd = eplus_functions.Idd(iddV6_0.commdct, iddV6_0.commlst, 
                                    iddV6_0.theidd, iddV6_0.block)
        idfw = eplus_functions.IdfWrapper(data, idd)
        result = eplus_functions.rename_name(idfw, objkey, oldname, newname)
        data = idfw.idf
        txt = `data`
        lst = txt.split()
        rtxt = ''.join(lst)
        print rtxt
        print newidf
        assert rtxt == newidf
    
def test_makeanobject():
    """py.test for makeanobject"""
    thedata = (('LEAD INPUT', "aname", ['LEAD INPUT']), 
        # objkey, objname, anobject
    ('PLANTLOOP', "aname", ['PLANTLOOP', 'aname', 'Water', '', '', '', '', 
        '', '0.0', 'Autocalculate', '', '', '', '', '', '', '', '',
        'Sequential', '', 'SingleSetpoint', 'None', 
        'None']), # more complex object
    ('BRANCH', "aname",     ['BRANCH', 'aname', '0', '', 
        '', '', '', '', ''] ), # for an extensible object    
    )
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    for objkey, objname, anobject in thedata:
        result = eplus_functions.makeanobject(data, theidd, 
                        commdct, objkey, objname)
        assert result == anobject
        
def test_getobjfieldnames():
    """py.test for getobjfieldnames"""
    thedata = (("SHADOWCALCULATION",
        [None, 'Calculation Frequency', 
        'Maximum Figures in Shadow Overlap Calculations']
    ), # objkey, fields
    )        
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    for objkey, fields in thedata:
        result = eplus_functions.getobjfieldnames(data, commdct, objkey)
        assert result == fields
        
def test_getfieldindex():
    """py.test for getfieldindex"""
    thedata = (("plantloop".upper(), "Plant Side Inlet Node Name", 
                        10), # objkey, fielddescp, findex
    )
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    for objkey, fielddescp, findex in thedata:
        result = eplus_functions.getfieldindex(data, commdct, objkey,
            fielddescp)
        assert result == findex
    thedata = (("OUTPUT:VARIABLE".upper(), "Name", 
                eplus_functions.NoSuchFieldError), # objkey, fielddescp, excep
    )
    for objkey, fielddescp, excep in thedata:
        with pytest.raises(excep):
            eplus_functions.getfieldindex(data, commdct, objkey, fielddescp)
        
def test_getextensiblesize():
    """py.test for getextensiblesize"""
    thedata = (("branchlist".upper(), 1), # objkey, extensiblesize
        ("branch".upper(), 5), # objkey, extensiblesize
        ("SimulationControl".upper(), None), # objkey, extensiblesize
    )        
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    for objkey, extensiblesize in thedata:
        result = eplus_functions.getextensiblesize(data, commdct, objkey)
        assert result == extensiblesize
        
def test_getextensibleposition():
    """py.test for getextensibleposition"""
    thedata = (("branchlist".upper(), 2), # objkey, extpos
        ("branch".upper(), 4), # objkey, extpos
        ("SimulationControl".upper(), None), # objkey, extpos
    )      
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    for objkey, extpos in thedata:
        result = eplus_functions.getextensibleposition(data, commdct, objkey)
        assert result == extpos

def test_getobject():
    """py.test for getobject"""
    thedata = (({"PLANTLOOP":[["PLANTLOOP", "ploop1",""], 
                    ["PLANTLOOP", "ploop2", "yahoo"]],
                    "BRANCH":[]},
                    "PLANTLOOP", "ploop2", 
                    ["PLANTLOOP", "ploop2", "yahoo"]), 
                    # data_dt, objkey, objname, obj
    )
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    for data_dt, objkey, objname, obj in thedata:
        data.dt = data_dt
        result = eplus_functions.getobject(data, commdct, objkey, objname)
        assert result == obj
        
def test_getobjlist():
    """py.test for getobjlist"""
    thedata = (("""Zone, PLENUM__1, 0, 0, 0, 0, 1, 1, 0.609600067, 283.2;
    Zone, SPACE1__1, 0, 0, 0, 0, 1, 1, 2.438400269, 239.247360229;
    Zone, SPACE2__1, 0, 0, 0, 0, 1, 1, 2.438400269, 103.311355591;
    Zone, SPACE3__1, 0, 0, 0, 0, 1, 1, 2.438400269, 239.247360229;
    Zone, SPACE4__1, 0, 0, 0, 0, 1, 1, 2.438400269, 103.311355591;
    Zone, SPACE5__1, 0, 0, 0, 0, 1, 1, 2.438400269, 447.682556152;
    Lights, SPACE1__1_Lights_1, SPACE1__1, LIGHTS__1, LightingLevel, 1584, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE2__1_Lights_1, SPACE2__1, LIGHTS__1, LightingLevel, 684, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE3__1_Lights_1, SPACE3__1, LIGHTS__1, LightingLevel, 1584, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE4__1_Lights_1, SPACE4__1, LIGHTS__1, LightingLevel, 684, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE5__1_Lights_1, SPACE5__1, LIGHTS__1, LightingLevel, 2964, , , 0, 0.59, 0.2, 0, GeneralLights;
    """,
    'lights'.upper(), 0, 2,
    ["PLENUM__1", "SPACE1__1", "SPACE2__1", "SPACE3__1", "SPACE4__1", "SPACE5__1"] ), 
    # idftxt, objkey, objid, fieldid, theobjlist
    ("""Zone, PLENUM__1, 0, 0, 0, 0, 1, 1, 0.609600067, 283.2;
    Zone, SPACE1__1, 0, 0, 0, 0, 1, 1, 2.438400269, 239.247360229;
    Zone, SPACE2__1, 0, 0, 0, 0, 1, 1, 2.438400269, 103.311355591;
    Zone, SPACE3__1, 0, 0, 0, 0, 1, 1, 2.438400269, 239.247360229;
    Zone, SPACE4__1, 0, 0, 0, 0, 1, 1, 2.438400269, 103.311355591;
    Zone, SPACE5__1, 0, 0, 0, 0, 1, 1, 2.438400269, 447.682556152;
    Lights, SPACE1__1_Lights_1, SPACE1__1, LIGHTS__1, LightingLevel, 1584, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE2__1_Lights_1, SPACE2__1, LIGHTS__1, LightingLevel, 684, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE3__1_Lights_1, SPACE3__1, LIGHTS__1, LightingLevel, 1584, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE4__1_Lights_1, SPACE4__1, LIGHTS__1, LightingLevel, 684, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE5__1_Lights_1, SPACE5__1, LIGHTS__1, LightingLevel, 2964, , , 0, 0.59, 0.2, 0, GeneralLights;
    """,
    'lights'.upper(), 0, 1,
    [] ), 
    # idftxt, objkey, objid, fieldid, theobjlist
    ("""Zone, PLENUM__1, 0, 0, 0, 0, 1, 1, 0.609600067, 283.2;
    Zone, SPACE1__1, 0, 0, 0, 0, 1, 1, 2.438400269, 239.247360229;
    Zone, SPACE2__1, 0, 0, 0, 0, 1, 1, 2.438400269, 103.311355591;
    Zone, SPACE3__1, 0, 0, 0, 0, 1, 1, 2.438400269, 239.247360229;
    Zone, SPACE4__1, 0, 0, 0, 0, 1, 1, 2.438400269, 103.311355591;
    Zone, SPACE5__1, 0, 0, 0, 0, 1, 1, 2.438400269, 447.682556152;
    ZoneList, azonelist, SPACE1__1, SPACE2__1;
    Lights, SPACE1__1_Lights_1, SPACE1__1, LIGHTS__1, LightingLevel, 1584, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE2__1_Lights_1, SPACE2__1, LIGHTS__1, LightingLevel, 684, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE3__1_Lights_1, SPACE3__1, LIGHTS__1, LightingLevel, 1584, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE4__1_Lights_1, SPACE4__1, LIGHTS__1, LightingLevel, 684, , , 0, 0.59, 0.2, 0, GeneralLights;
    Lights, SPACE5__1_Lights_1, SPACE5__1, LIGHTS__1, LightingLevel, 2964, , , 0, 0.59, 0.2, 0, GeneralLights;
    """,
    'lights'.upper(), 0, 2,
    ["PLENUM__1", "SPACE1__1", "SPACE2__1", "SPACE3__1", "SPACE4__1", "SPACE5__1", "azonelist"]  ), 
    # list comes from zone and zonelist 
    # idftxt, objkey, objid, fieldid, theobjlist
    )   
    # TODO : test if it is not an object list, test for zone and zonelist
    for idftxt, objkey, objid, fieldid, theobjlist in thedata:  
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        theidd = iddV6_0.theidd
        idd = eplus_functions.Idd(commdct, iddV6_0.commlst, theidd, iddV6_0.block)
        idfw = eplus_functions.IdfWrapper(data, idd)
        dt = idfw.idf.dt

        result = eplus_functions.getobjlistOfField(idfw, objkey, objid, fieldid)
        assert result == theobjlist

def test_getchoiceOFField():
    """py.test for getchoiceOFField"""
    thedata = (("""Building, Building, 30., City, 0.04, 0.4, FullExterior, 25;""",
    "Building".upper(), 0, 3, 
    ["Country",  "Suburbs",  "City",  "Ocean",  "Urban"]), # idftxt, objkey, objid, fieldid, choicelist
    ("""Building, Building, 30., City, 0.04, 0.4, FullExterior, 25;""",
    "Building".upper(), 0, 1, 
    []), # idftxt, objkey, objid, fieldid, choicelist
    )
    for idftxt, objkey, objid, fieldid, choicelist in thedata:
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        theidd = iddV6_0.theidd
        idd = eplus_functions.Idd(commdct, iddV6_0.commlst, theidd, iddV6_0.block)
        idfw = eplus_functions.IdfWrapper(data, idd)
        result = eplus_functions.getchoiceOFField(idfw, objkey, objid, fieldid)
        assert result == choicelist

def test_getreferences():
    """py.test for getreferences"""
    thedata = (("zone".upper(), 1, ['ZoneNames',
             'OutFaceEnvNames',
             'ZoneAndZoneListNames',
             'AirflowNetworkNodeAndZoneNames']
             ), # key, fieldid, refs
     ("FenestrationSurface:Detailed".upper(), 1, ['SubSurfNames',
            'SurfAndSubSurfNames',
            'AllHeatTranSurfNames',
            'OutFaceEnvNames',
            'AllHeatTranAngFacNames',
            'RadGroupAndSurfNames',
            'SurfGroupAndHTSurfNames',
            'AllShadingAndHTSurfNames']
              ), # key, fieldid, refs
    )
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    idd = eplus_functions.Idd(commdct, iddV6_0.commlst, theidd, iddV6_0.block)
    idfw = eplus_functions.IdfWrapper(data, idd)
    for key, fieldid, refs in thedata:
        anobject = eplus_functions.makeanobject(data, theidd, commdct, 
                                            key, objname="azone")
        data.dt[key].append(anobject)
        result = eplus_functions.getreferences(idfw, key, fieldid)
        assert result == refs
        
def test_getReferenceObjectList():
    """py.test for getReferenceObjectList"""
    thedata = (("zone".upper(), ['ZoneNames',
             'OutFaceEnvNames',
             'ZoneAndZoneListNames',
             'AirflowNetworkNodeAndZoneNames'],
             [('SIZING:ZONE', 1),
              ('ZONEHVAC:EQUIPMENTCONNECTIONS', 1),
              ('BUILDINGSURFACE:DETAILED', 4),
              ('FENESTRATIONSURFACE:DETAILED', 5),
              ('BUILDINGSURFACE:DETAILED', 6),
              ('LIGHTS', 2),
              ('PEOPLE', 2),
              ('ZONEINFILTRATION:DESIGNFLOWRATE', 2),
              ('ELECTRICEQUIPMENT', 2),
              ('ZONECONTROL:THERMOSTAT', 2)]
             ), # key, refs, reflist
    )
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    idd = eplus_functions.Idd(commdct, iddV6_0.commlst, theidd, iddV6_0.block)
    idfw = eplus_functions.IdfWrapper(data, idd)
    for key, refs, reflist in thedata:
        anobject = eplus_functions.makeanobject(data, theidd, commdct, 
                                                    key, objname="azone")
        data.dt[key].append(anobject)
        for akey, fieldid, in reflist:
            anobject = eplus_functions.makeanobject(data, theidd, commdct, 
                                                        akey, objname="azone")
            data.dt[akey].append(anobject)
        result = eplus_functions.getReferenceObjectList(idfw, refs)
        assert result == reflist
        
def test_newname2references_inner():
    """py.test for newname2references_inner"""
    # a zone name is changed. It is refered by lights and people.
    # test if the reference in lights and people also change        
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    idd = eplus_functions.Idd(commdct, iddV6_0.commlst, theidd, iddV6_0.block)
    idfw = eplus_functions.IdfWrapper(data, idd)
    # - 
    zonekey = 'zone'.upper()
    lightkey = 'lights'.upper()
    peoplekey = 'people'.upper()
    keys = [zonekey, lightkey, peoplekey]
    keys = keys + keys
    names = ['z1', 'l1', 'p1', 'z2', 'l2', 'p2']
    for key, name  in zip(keys, names):
        anobject = eplus_functions.makeanobject(data, theidd, commdct, 
                                                    key, objname="name")
        data.dt[key].append(anobject)
    data.dt[lightkey][0][2] = 'z1'
    data.dt[peoplekey][0][2] = 'z1'
    data.dt[lightkey][1][2] = 'z2'
    data.dt[peoplekey][1][2] = 'z2'
    oldname, newname = 'z1', 'zz1'
    # = 
    refs = eplus_functions.getreferences(idfw, zonekey, 1)
    reflist = eplus_functions.getReferenceObjectList(idfw, refs)
    # - 
    data.dt[zonekey][0][1] = newname
    eplus_functions.newname2references_inner(idfw, reflist, oldname, newname)
    assert data.dt[lightkey][0][2] == newname
    assert data.dt[peoplekey][0][2] == newname
    assert data.dt[lightkey][1][2] == 'z2'
    assert data.dt[peoplekey][1][2] == 'z2'

def test_newname2references():
    """py.test for newname2references"""
    # a zone name is changed. It is refered by lights and people.
    # test if the reference in lights and people also change        
    fname = StringIO("")
    data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                        iddV6_0.commdct)
    theidd = iddV6_0.theidd
    idd = eplus_functions.Idd(commdct, iddV6_0.commlst, theidd, iddV6_0.block)
    idfw = eplus_functions.IdfWrapper(data, idd)
    # - 
    zonekey = 'zone'.upper()
    lightkey = 'lights'.upper()
    peoplekey = 'people'.upper()
    keys = [zonekey, lightkey, peoplekey]
    keys = keys + keys
    names = ['z1', 'l1', 'p1', 'z2', 'l2', 'p2']
    for key, name  in zip(keys, names):
        anobject = eplus_functions.makeanobject(data, theidd, commdct, 
                                                    key, objname="name")
        data.dt[key].append(anobject)
    data.dt[lightkey][0][2] = 'z1'
    data.dt[peoplekey][0][2] = 'z1'
    data.dt[lightkey][1][2] = 'z2'
    data.dt[peoplekey][1][2] = 'z2'
    oldname, newname = 'z1', 'zz1'
    # = 
    data.dt[zonekey][0][1] = newname
    fieldid = 1
    eplus_functions.newname2references(idfw, zonekey, fieldid, 
                                                    oldname, newname)
    assert data.dt[lightkey][0][2] == newname
    assert data.dt[peoplekey][0][2] == newname
    assert data.dt[lightkey][1][2] == 'z2'
    assert data.dt[peoplekey][1][2] == 'z2'

def test_createobject():
    """py.test for createobject"""
    thedata = (("", "SimulationControl", None, 
        """SIMULATIONCONTROL,
             ,
             ,
             ,
             ,
             ;
        """),# idftxt, objkey, objname, outtxt
("", "RunPeriodControl:SpecialDays", 'Christmas', 
        """RUNPERIODCONTROL:SPECIALDAYS,
     Christmas,
     ,
     ,
     ;
"""),# idftxt, objkey, objname, outtxt
    )
    for idftxt, objkey, objname, outtxt in thedata:
        objkey = objkey.upper()
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        theidd = iddV6_0.theidd
        idd = eplus_functions.Idd(commdct, iddV6_0.commlst, 
            theidd, iddV6_0.block)
        idfw = eplus_functions.IdfWrapper(data, idd)
        result = eplus_functions.createobject(idfw, objkey, objname)
        data = idfw.idf
        fname = StringIO(outtxt)
        newdata, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        assert newdata.dt[objkey] == data.dt[objkey]
        
def test_fieldvalue():
    """py.test for fieldvalue"""
    thedata = (("""RunPeriodControl:SpecialDays,
     Christmas,
     December 25,
     1,
     Holiday;
""", "RunPeriodControl:SpecialDays", "Christmas", 'Start Date', '12/25', 
    """RunPeriodControl:SpecialDays,
     Christmas,
     12/25,
     1,
     Holiday;
"""), # idftxt, objkey, objname, field, value, outtxt
    ("""SimulationControl,
     Yes,
     Yes,
     Yes,
     Yes,
     Yes;
""", "SimulationControl", None, 'Do Zone Sizing Calculation', 'No', 
    """SimulationControl,
     No,
     Yes,
     Yes,
     Yes,
     Yes;
"""), # idftxt, objkey, objname, field, value, outtxt
    )
    for idftxt, objkey, objname, field, value, outtxt in thedata:
        objkey = objkey.upper()
        fname = StringIO(idftxt)
        data, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        theidd = iddV6_0.theidd
        idd = eplus_functions.Idd(commdct, iddV6_0.commlst, 
            theidd, iddV6_0.block)
        idfw = eplus_functions.IdfWrapper(data, idd)
        result = eplus_functions.fieldvalue(idfw, objkey, objname, field, 
            value)
        data = idfw.idf
        fname = StringIO(outtxt)
        newdata, commdct = readidf.readdatacommdct(fname, iddV6_0.theidd,
                                                            iddV6_0.commdct)
        assert newdata.dt[objkey] == data.dt[objkey]
