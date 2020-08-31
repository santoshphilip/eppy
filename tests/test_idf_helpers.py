# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for idf"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import StringIO

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal
import eppy.idf_helpers as idf_helpers

iddfhandle = StringIO(iddcurrent.iddtxt)

if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_idfobjectkeys():
    """py.test for idfobjectkeys"""
    expected = [
        "LEAD INPUT",
        "SIMULATION DATA",
        "VERSION",
        "SIMULATIONCONTROL",
        "BUILDING",
    ]
    idf = IDF(StringIO(""))
    result = idf_helpers.idfobjectkeys(idf)
    assert result[:5] == expected


def test_getanymentions():
    """py.test for getanymentions"""
    idf = IDF(StringIO(""))
    mat = idf.newidfobject("MATERIAL", Name="mat")
    aconst = idf.newidfobject("CONSTRUCTION", Name="const")
    foundobjs = idf_helpers.getanymentions(idf, mat)
    assert len(foundobjs) == 1
    assert foundobjs[0] == mat


def test_getobject_use_prevfield():
    """py.test for getobject_use_prevfield"""
    idf = IDF(StringIO(""))
    branch = idf.newidfobject(
        "BRANCH",
        Name="CW Pump Branch",
        Component_1_Object_Type="Pump:VariableSpeed",
        Component_1_Name="CW Circ Pump",
    )
    pump = idf.newidfobject("PUMP:VARIABLESPEED", Name="CW Circ Pump")
    foundobject = idf_helpers.getobject_use_prevfield(idf, branch, "Component_1_Name")
    assert foundobject == pump
    # test for all times it should return None
    foundobject = idf_helpers.getobject_use_prevfield(idf, branch, "Name")
    foundobject = None  # prev field not end with Object_Type
    foundobject = idf_helpers.getobject_use_prevfield(
        idf, branch, "Component_11_Object_Type"
    )
    foundobject = None  # field does not end with "Name"
    foundobject = idf_helpers.getobject_use_prevfield(idf, branch, "Component_3_Name")
    foundobject = None  # bad idfobject key


def test_getidfkeyswithnodes():
    """py.test for getidfkeyswithnodes"""
    nodekeys = idf_helpers.getidfkeyswithnodes()
    # print(len(nodekeys))
    assert "PLANTLOOP" in nodekeys
    assert "ZONE" not in nodekeys


# def test_a():
#     assert 1== 2


def test_getobjectswithnode():
    """py.test for getobjectswithnode"""
    idf = IDF(StringIO(""))
    nodekeys = idf_helpers.getidfkeyswithnodes()
    plantloop = idf.newidfobject(
        "PlantLoop",
        Name="Chilled Water Loop",
        Plant_Side_Inlet_Node_Name="CW Supply Inlet Node",
    )
    branch = idf.newidfobject(
        "Branch",
        Name="CW Pump Branch",
        Component_1_Inlet_Node_Name="CW Supply Inlet Node",
    )
    pump = idf.newidfobject(
        "Pump:VariableSpeed",
        Name="CW Circ Pump",
        Inlet_Node_Name="CW Supply Inlet Node",
    )
    zone = idf.newidfobject("zone")
    foundobjs = idf_helpers.getobjectswithnode(idf, nodekeys, "CW Supply Inlet Node")
    expected = [plantloop, branch, pump]
    expectedset = set([item.key for item in expected])
    resultset = set([item.key for item in foundobjs])
    assert resultset == expectedset
    expectedset = set([item.Name for item in expected])
    resultset = set([item.Name for item in foundobjs])
    assert resultset == expectedset


def test_name2idfobject():
    """py.test for name2idfobject"""
    idf = IDF(StringIO(""))
    plantloopname = "plantloopname"
    branchname = "branchname"
    pumpname = "pumpname"
    zonename = "zonename"
    plantloop = idf.newidfobject(
        "PlantLoop",
        Name=plantloopname,
        Plant_Side_Inlet_Node_Name="CW Supply Inlet Node",
    )
    branch = idf.newidfobject(
        "Branch", Name=branchname, Component_1_Inlet_Node_Name="CW Supply Inlet Node"
    )
    pump = idf.newidfobject(
        "Pump:VariableSpeed", Name=pumpname, Inlet_Node_Name="CW Supply Inlet Node"
    )
    zone = idf.newidfobject("zone", Name=zonename)
    simulation = idf.newidfobject("SimulationControl")
    # - test
    names = [plantloopname, branchname, pumpname, zonename]
    idfobjs = [plantloop, branch, pump, zone]
    for name, idfobj in zip(names, idfobjs):
        result = idf_helpers.name2idfobject(idf, Name=name)
        assert result == idfobj
    # test when objkeys!=None
    objkey = "ZoneHVAC:EquipmentConnections"
    equipconnections = idf.newidfobject(objkey, Zone_Name=zonename)
    result = idf_helpers.name2idfobject(idf, Zone_Name=zonename, objkeys=[objkey])
    assert result == equipconnections


def test_getidfobjectlist():
    """py.test for getidfobjectlist"""
    names = ["a", "b", "c", "d", "e"]
    idf = IDF(StringIO(""))
    idf.newidfobject("building", Name="a")
    idf.newidfobject("building", Name="b")
    idf.newidfobject("Site:Location", Name="c")
    idf.newidfobject("ScheduleTypeLimits", Name="d")
    idf.newidfobject("ScheduleTypeLimits", Name="e")
    result = idf_helpers.getidfobjectlist(idf)
    assert [res.Name for res in result] == names


def test_copyidfintoidf():
    """py.test for copyidfintoidf"""
    tonames = ["a", "b", "c"]
    fromnames = ["d", "e"]
    allnames = ["a", "b", "c", "d", "e"]
    toidf = IDF(StringIO(""))
    toidf.newidfobject("building", Name="a")
    toidf.newidfobject("building", Name="b")
    toidf.newidfobject("Site:Location", Name="c")
    result = idf_helpers.getidfobjectlist(toidf)
    assert [res.Name for res in result] == tonames
    fromidf = IDF(StringIO(""))
    fromidf.newidfobject("ScheduleTypeLimits", Name="d")
    fromidf.newidfobject("ScheduleTypeLimits", Name="e")
    result = idf_helpers.getidfobjectlist(fromidf)
    assert [res.Name for res in result] == fromnames
    idf_helpers.copyidfintoidf(toidf, fromidf)
    result = idf_helpers.getidfobjectlist(toidf)
    assert [res.Name for res in result] == allnames
