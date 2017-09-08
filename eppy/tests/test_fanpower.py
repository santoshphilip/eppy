# Copyright (c) 2017 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Tests for fanpower.py
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import StringIO

import eppy.fanpower as fanpower
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal


iddfhandle = StringIO(iddcurrent.iddtxt)
  
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_pascal2inh2o():
    """py.test for pascal2inh2o"""
    data = (
    (1, 0.00401865), # pascal, expected
    (186.816675, 0.7507501808391), # pascal, expected
    )
    for pascal, expected in data:
        result = fanpower.pascal2inh2o(pascal)
        assert almostequal(result, expected, places=5)
        
def test_m3s2cfm():
    """py.test for m3s2cfm"""
    data = (
    (1, 2118.880003), # m3s, expected
    (1.28442384, 2721.539989952472), # m3s, expected
    ) 
    for m3s, expected in data:
        result = fanpower.m3s2cfm(m3s)
        assert result == expected
        
def test_fan_bhp():
    """py.test for fan_bhp"""
    data = (
    (0.342, 186.816675, 1.28442384, 0.939940898974), # fan_tot_eff, pascal, m3s, expected
    (0.537, 871.81115,2.44326719, 5.31400249068), # fan_tot_eff, pascal, m3s, expected
    )
    for fan_tot_eff, pascal, m3s, expected in data:
        result = fanpower.fan_bhp(fan_tot_eff, pascal, m3s)
        assert almostequal(result, expected)
        
def test_bhp2watts():
    """py.test for bhp2watts"""
    data = (
    (0.939940898974, 700.9139283649118), # bhp, expected
    (5.31400249068, 3962.6516573000763), # bhp, expected
    )
    for bhp, expected in data:
        result = fanpower.bhp2watts(bhp)
        assert result == expected
        
def test_fan_watts():
    """py.test for fan_watts"""
    data = (
    (0.342, 186.816675, 1.28442384, 700.9139283649118),  # fan_tot_eff, pascal, m3s, expected
    (0.537, 871.81115,2.44326719, 3962.6516573000763),  # fan_tot_eff, pascal, m3s, expected
    ) 
    for fan_tot_eff, pascal, m3s, expected in data:
        result = fanpower.fan_watts(fan_tot_eff, pascal, m3s)
        assert almostequal(result, expected)
        
vavfan = """Fan:VariableVolume,
  Fan 2,                                  !- Name
  OfficeHVACAvail,                        !- Availability Schedule Name
  0.519,                                  !- Fan Total Efficiency
  164.3824832215,                         !- Pressure Rise {Pa}
  5.6633693184,                           !- Maximum Flow Rate {m3/s}
  FixedFlowRate,                          !- Fan Power Minimum Flow Rate Input Method
  0,                                      !- Fan Power Minimum Flow Fraction
  1.4158423296,                           !- Fan Power Minimum Air Flow Rate {m3/s}
  0.865,                                  !- Motor Efficiency
  1,                                      !- Motor In Airstream Fraction
  0.04076,                                !- Fan Power Coefficient 1
  0.088045,                               !- Fan Power Coefficient 2
  -0.072926,                              !- Fan Power Coefficient 3
  0.94374,                                !- Fan Power Coefficient 4
  0,                                      !- Fan Power Coefficient 5
  AC(1)(2) Supply Side (Return Air) Inlet Node, !- Air Inlet Node Name
  Fan 2 Outlet Node;                      !- Air Outlet Node Name
""" 

def testfanpower_bhp():
    """py.test for fanpower_bhp"""
    idf = IDF(StringIO(vavfan))
    thefans = idf.idfobjects['Fan:VariableVolume'.upper()]
    thefan = thefans[0]
    bhp = thefan.fanpower_bhp
    assert almostequal(bhp, 2.40306611606)
    # test autosize
    thefan.Maximum_Flow_Rate = 'autosize'
    bhp = thefan.fanpower_bhp
    assert bhp == 'autosize'
    
def testfanpower_watts():
    """py.test for fanpower_watts"""
    idf = IDF(StringIO(vavfan))
    thefans = idf.idfobjects['Fan:VariableVolume'.upper()]
    thefan = thefans[0]
    watts = thefan.fanpower_watts
    assert almostequal(watts, 1791.9664027495671)
    # test autosize
    thefan.Maximum_Flow_Rate = 'autosize'
    watts = thefan.fanpower_watts
    assert watts == 'autosize'
    