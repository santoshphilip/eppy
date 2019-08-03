# -*- coding: utf-8 -*-
# Copyright (c) 2017 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""quick and dirty functions for get fan power BHP or Watts
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# from eppy.bunch_subclass import BadEPFieldError
# import eppy.bunch_subclass


def pascal2inh2o(pascal):
    """convert pressure in Pascals to inches of water"""
    # got this from a google search
    return pascal * 0.00401865


def inh2o2pascal(inh2o):
    """convert pressure in inches of water to Pascals"""
    return (inh2o * 1.0) / 0.00401865


def m3s2cfm(m3s):
    """convert flow meter^3/second to cfm"""
    # from http://www.traditionaloven.com/tutorials/flow-rate/convert-m3-cubic-meter-per-second-to-ft3-cubic-foot-per-minute.html
    return (m3s * 1.0) * 2118.880003


def cfm2m3s(cfm):
    """convert flow cfm to meter^3/second"""
    return cfm / 2118.880003


def fan_bhp(fan_tot_eff, pascal, m3s):
    """return the fan power in bhp given fan efficiency, Pressure rise (Pa) and flow (m3/s)"""
    # from discussion in
    # http://energy-models.com/forum/baseline-fan-power-calculation
    inh2o = pascal2inh2o(pascal)
    cfm = m3s2cfm(m3s)
    return (cfm * inh2o * 1.0) / (6356.0 * fan_tot_eff)


def bhp2pascal(bhp, cfm, fan_tot_eff):
    """return inputs for E+ in pascal and m3/s"""
    inh2o = bhp * 6356.0 * fan_tot_eff / cfm
    pascal = inh2o2pascal(inh2o)
    m3s = cfm2m3s(cfm)
    return pascal, m3s


def bhp2watts(bhp):
    """convert brake horsepower (bhp) to watts"""
    return bhp * 745.7


def watts2bhp(watts):
    """convert watts to brake horsepower (bhp)"""
    return watts / 745.7


def fan_watts(fan_tot_eff, pascal, m3s):
    """return the fan power in watts given fan efficiency, Pressure rise (Pa) and flow (m3/s)"""
    # got this from a google search
    bhp = fan_bhp(fan_tot_eff, pascal, m3s)
    return bhp2watts(bhp)


def watts2pascal(watts, cfm, fan_tot_eff):
    """convert and return inputs for E+ in pascal and m3/s"""
    bhp = watts2bhp(watts)
    return bhp2pascal(bhp, cfm, fan_tot_eff)


def fanpower_bhp(ddtt):
    """return fan power in bhp given the fan IDF object"""
    from eppy.bunch_subclass import (
        BadEPFieldError,
    )  # here to prevent circular dependency

    try:
        fan_tot_eff = ddtt.Fan_Total_Efficiency  # from V+ V8.7.0 onwards
    except BadEPFieldError as e:
        fan_tot_eff = ddtt.Fan_Efficiency
    pascal = float(ddtt.Pressure_Rise)
    if str(ddtt.Maximum_Flow_Rate).lower() == "autosize":
        # str can fail with unicode chars :-(
        return "autosize"
    else:
        m3s = float(ddtt.Maximum_Flow_Rate)
    return fan_bhp(fan_tot_eff, pascal, m3s)


def fanpower_watts(ddtt):
    """return fan power in bhp given the fan IDF object"""
    from eppy.bunch_subclass import (
        BadEPFieldError,
    )  # here to prevent circular dependency

    try:
        fan_tot_eff = ddtt.Fan_Total_Efficiency  # from V+ V8.7.0 onwards
    except BadEPFieldError as e:
        fan_tot_eff = ddtt.Fan_Efficiency
    pascal = float(ddtt.Pressure_Rise)
    if str(ddtt.Maximum_Flow_Rate).lower() == "autosize":
        # str can fail with unicode chars :-(
        return "autosize"
    else:
        m3s = float(ddtt.Maximum_Flow_Rate)
    return fan_watts(fan_tot_eff, pascal, m3s)


def fan_maxcfm(ddtt):
    """return the fan max cfm"""
    if str(ddtt.Maximum_Flow_Rate).lower() == "autosize":
        # str can fail with unicode chars :-(
        return "autosize"
    else:
        m3s = float(ddtt.Maximum_Flow_Rate)
        return m3s2cfm(m3s)
