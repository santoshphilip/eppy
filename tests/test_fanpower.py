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

from io import StringIO

import eppy.fanpower as fanpower
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal


iddfhandle = StringIO(iddcurrent.iddtxt)

if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_pascal2inh2o():
    """py.test for pascal2inh2o and inh2o2pascal"""
    data = (
        (1, 0.00401865),  # pascal, expected
        (186.816675, 0.7507501808391),  # pascal, expected
    )
    for pascal, expected in data:
        result = fanpower.pascal2inh2o(pascal)
        assert almostequal(result, expected, places=5)
    data = (
        (1, 0.00401865),  # expected, inh20
        (186.816675, 0.7507501808391),  # expected, inh20
    )
    for expected, inh20 in data:
        result = fanpower.inh2o2pascal(inh20)
        assert almostequal(result, expected, places=3)


def test_m3s2cfm():
    """py.test for m3s2cfm and cfm2m3s"""
    data = (
        (1, 2118.880003),  # m3s, expected
        (1.28442384, 2721.539989952472),  # m3s, expected
    )
    for m3s, expected in data:
        result = fanpower.m3s2cfm(m3s)
        assert result == expected
    data = (
        (1, 2118.880003),  # expected, cfm
        (1.28442384, 2721.539989952472),  # expected, cfm
    )
    for expected, cfm in data:
        result = fanpower.cfm2m3s(cfm)
        assert result == expected


def test_fan_bhp():
    """py.test for fan_bhp"""
    data = (
        (
            0.342,
            186.816675,
            1.28442384,
            0.939940898974,
        ),  # fan_tot_eff, pascal, m3s, expected
        (
            0.537,
            871.81115,
            2.44326719,
            5.31400249068,
        ),  # fan_tot_eff, pascal, m3s, expected
    )
    for fan_tot_eff, pascal, m3s, expected in data:
        result = fanpower.fan_bhp(fan_tot_eff, pascal, m3s)
        assert almostequal(result, expected)


def test_bhp2watts():
    """py.test for bhp2watts and watts2bhp"""
    data = (
        (0.939940898974, 700.9139283649118),  # bhp, expected
        (5.31400249068, 3962.6516573000763),  # bhp, expected
    )
    for bhp, expected in data:
        result = fanpower.bhp2watts(bhp)
        assert result == expected
    data = (
        (0.939940898974, 700.9139283649118),  # expected, watts
        (5.31400249068, 3962.6516573000763),  # expected, watts
    )
    for expected, watts in data:
        result = fanpower.watts2bhp(watts)
        assert result == expected


def test_fan_watts():
    """py.test for fan_watts"""
    data = (
        (
            0.342,
            186.816675,
            1.28442384,
            700.9139283649118,
        ),  # fan_tot_eff, pascal, m3s, expected
        (
            0.537,
            871.81115,
            2.44326719,
            3962.6516573000763,
        ),  # fan_tot_eff, pascal, m3s, expected
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
    """py.test for fanpower_bhp in idf"""
    idf = IDF(StringIO(vavfan))
    thefans = idf.idfobjects["Fan:VariableVolume".upper()]
    thefan = thefans[0]
    bhp = thefan.f_fanpower_bhp
    assert almostequal(bhp, 2.40306611606)
    # test autosize
    thefan.Maximum_Flow_Rate = "autosize"
    bhp = thefan.f_fanpower_bhp
    assert bhp == "autosize"


def testfanpower_watts():
    """py.test for fanpower_watts in idf"""
    idf = IDF(StringIO(vavfan))
    thefans = idf.idfobjects["Fan:VariableVolume".upper()]
    thefan = thefans[0]
    watts = thefan.f_fanpower_watts
    assert almostequal(watts, 1791.9664027495671)
    # test autosize
    thefan.Maximum_Flow_Rate = "autosize"
    watts = thefan.f_fanpower_watts
    assert watts == "autosize"


def test_fan_maxcfm():
    """py.test for fan_maxcfm in idf"""
    idf = IDF(StringIO(vavfan))
    thefans = idf.idfobjects["Fan:VariableVolume".upper()]
    thefan = thefans[0]
    cfm = thefan.f_fan_maxcfm
    assert almostequal(cfm, 12000, places=5)
    # test autosize
    thefan.Maximum_Flow_Rate = "autosize"
    watts = thefan.f_fanpower_watts
    assert watts == "autosize"


def test_bhp2pascal():
    """py.test for bhp2pascal"""
    bhp = 10.182489271962908
    cfm = 74999.99998975938
    fan_tot_eff = 0.58
    exp_pascal, exp_m3s = (124.544455, 35.39605824)
    result_pascal, result_m3s = fanpower.bhp2pascal(bhp, cfm, fan_tot_eff)
    assert almostequal(result_pascal, exp_pascal)
    assert almostequal(result_m3s, exp_m3s)


def test_watts2pascal():
    """py.test for watts2pascal"""
    watts = 7593.0822501027405
    cfm = 74999.99998975938
    fan_tot_eff = 0.58
    exp_pascal, exp_m3s = (124.544455, 35.39605824)
    result_pascal, result_m3s = fanpower.watts2pascal(watts, cfm, fan_tot_eff)
    assert almostequal(result_pascal, exp_pascal)
    assert almostequal(result_m3s, exp_m3s)
