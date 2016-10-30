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
    
    
        