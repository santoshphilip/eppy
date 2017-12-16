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

from six import iteritems
from six import StringIO

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal
import eppy.idf_helpers as idf_helpers

iddfhandle = StringIO(iddcurrent.iddtxt)
  
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

def test_idfobjectkeys():
    """py.test for idfobjectkeys"""
    expected = [u'LEAD INPUT',
            u'SIMULATION DATA',
            u'VERSION',
            u'SIMULATIONCONTROL',
            u'BUILDING']
    idf = IDF(StringIO(""))
    result = idf_helpers.idfobjectkeys(idf)
    assert result[:5] == expected
    
    
def test_getanymentions():
    """py.test for getanymentions"""
    idf = IDF(StringIO(""))
    mat = idf.newidfobject('MATERIAL', Name='mat')
    aconst = idf.newidfobject('CONSTRUCTION', Name='const')
    foundobjs = idf_helpers.getanymentions(idf, mat)
    assert len(foundobjs) == 1
    assert foundobjs[0] == mat
    
def test_getobject_use_prevfield():
    """py.test for getobject_use_prevfield"""
    idf = IDF(StringIO(""))
    branch = idf.newidfobject('BRANCH', 
                    Name='CW Pump Branch',
                    Component_1_Object_Type='Pump:VariableSpeed',
                    Component_1_Name='CW Circ Pump')    
    pump = idf.newidfobject('PUMP:VARIABLESPEED', 
                    Name='CW Circ Pump')
    foundobject = idf_helpers.getobject_use_prevfield(idf, 
                                branch, 'Component_1_Name')
    assert foundobject == pump
    # test for all times it should return None
    foundobject = idf_helpers.getobject_use_prevfield(idf, 
                                branch, 'Name')
    foundobject = None # prev field not end with Object_Type
    foundobject = idf_helpers.getobject_use_prevfield(idf, 
                                branch, u'Component_11_Object_Type')
    foundobject = None# field does not end with "Name"
    foundobject = idf_helpers.getobject_use_prevfield(idf, 
                                branch,  u'Component_3_Name')
    foundobject = None # bad idfobject key


def test_getidfkeyswithnodes():
    """py.test for getidfkeyswithnodes"""
    nodekeys = idf_helpers.getidfkeyswithnodes()
    # print(len(nodekeys))
    assert 'PLANTLOOP' in nodekeys
    assert 'ZONE' not in nodekeys

# def test_a():
#     assert 1== 2
        
def test_getobjectswithnode():
    """py.test for getobjectswithnode"""
    idf = IDF(StringIO(""))
    nodekeys = idf_helpers.getidfkeyswithnodes() 
    plantloop = idf.newidfobject('PlantLoop'.upper(), 
                    Name='Chilled Water Loop',
                    Plant_Side_Inlet_Node_Name='CW Supply Inlet Node')
    branch = idf.newidfobject('Branch'.upper(), 
                    Name='CW Pump Branch',
                    Component_1_Inlet_Node_Name='CW Supply Inlet Node')
    pump = idf.newidfobject('Pump:VariableSpeed'.upper(), 
                    Name='CW Circ Pump',
                    Inlet_Node_Name='CW Supply Inlet Node')
    zone = idf.newidfobject('zone'.upper())
    foundobjs = idf_helpers.getobjectswithnode(idf, nodekeys, 
                                        'CW Supply Inlet Node')
    expected = [plantloop, branch, pump] 
    expectedset = set([item.key for item in expected])
    resultset = set([item.key for item in foundobjs]) 
    assert  resultset ==  expectedset
    expectedset = set([item.Name for item in expected])
    resultset = set([item.Name for item in foundobjs]) 
    assert  resultset ==  expectedset

def test_name2idfobject():
    """py.test for name2idfobject"""
    idf = IDF(StringIO(""))
    plantloopname = "plantloopname"
    branchname = "branchname"
    pumpname = "pumpname"
    zonename = "zonename"
    plantloop = idf.newidfobject('PlantLoop'.upper(), 
                    Name=plantloopname,
                    Plant_Side_Inlet_Node_Name='CW Supply Inlet Node')
    branch = idf.newidfobject('Branch'.upper(), 
                    Name=branchname,
                    Component_1_Inlet_Node_Name='CW Supply Inlet Node')
    pump = idf.newidfobject('Pump:VariableSpeed'.upper(), 
                    Name=pumpname,
                    Inlet_Node_Name='CW Supply Inlet Node')
    zone = idf.newidfobject('zone'.upper(), Name=zonename)
    simulation = idf.newidfobject('SimulationControl'.upper()) 
    # - test
    names = [plantloopname, branchname, pumpname, zonename]
    idfobjs = [plantloop, branch, pump, zone]
    for name, idfobj in zip(names, idfobjs):
        result = idf_helpers.name2idfobject(idf, Name=name)
        assert result == idfobj
    # test when objkeys!=None
    objkey = 'ZoneHVAC:EquipmentConnections'.upper()
    equipconnections = idf.newidfobject(objkey,
                        Zone_Name=zonename)
    result = idf_helpers.name2idfobject(idf, Zone_Name=zonename, 
                    objkeys=[objkey, ])
    assert result == equipconnections

def test_getidfobjectlist():
    """py.test for getidfobjectlist"""
    names = ["a", "b", "c", "d", "e"]
    idf = IDF(StringIO(""))
    idf.newidfobject("Site:Location".upper(), Name="a")
    idf.newidfobject("building".upper(), Name="b")
    idf.newidfobject("building".upper(), Name="c")
    idf.newidfobject("ScheduleTypeLimits".upper(), Name="d")
    idf.newidfobject("ScheduleTypeLimits".upper(), Name="e")
    result = idf_helpers.getidfobjectlist(idf)
    assert [res.Name for res in result] == names
    
def test_copyidfintoidf():
    """py.test for copyidfintoidf"""
    tonames = ["a", "b", "c"]
    fromnames = ["d", "e"]
    allnames = ["a", "b", "c", "d", "e"]
    toidf = IDF(StringIO(""))
    toidf.newidfobject("Site:Location".upper(), Name="a")
    toidf.newidfobject("building".upper(), Name="b")
    toidf.newidfobject("building".upper(), Name="c")
    result = idf_helpers.getidfobjectlist(toidf)
    assert set([res.Name for res in result]) == set(tonames)
    fromidf = IDF(StringIO(""))
    fromidf.newidfobject("ScheduleTypeLimits".upper(), Name="d")
    fromidf.newidfobject("ScheduleTypeLimits".upper(), Name="e")
    result = idf_helpers.getidfobjectlist(fromidf)
    assert set([res.Name for res in result]) == set(fromnames)
    idf_helpers.copyidfintoidf(toidf, fromidf)
    result = idf_helpers.getidfobjectlist(toidf)
    assert set([res.Name for res in result]) == set(allnames)
        