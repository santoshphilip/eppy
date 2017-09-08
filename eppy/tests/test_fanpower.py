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

import eppy.fanpower.fanpower as fanpower
from eppy.pytest_helpers import almostequal


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