# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Functions to calculate the thermal properties of constructions and materials.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from itertools import product

INSIDE_FILM_R = 0.12
OUTSIDE_FILM_R = 0.03


def rvalue(ddtt):
    """
    R value (W/K) of a construction or material.
    thickness (m) / conductivity (W/m-K)
    """
    if ddtt.obj[0] == 'Material':
        thickness = ddtt.obj[ddtt.objls.index('Thickness')]
        conductivity = ddtt.obj[ddtt.objls.index('Conductivity')]
        rvalue = thickness / conductivity
    elif ddtt.obj[0] == 'Material:AirGap':
        rvalue = ddtt.obj[ddtt.objls.index('Thermal_Resistance')] 
    elif ddtt.obj[0] == 'Construction':
        rvalue = INSIDE_FILM_R + OUTSIDE_FILM_R
        layers = ddtt.obj[2:]
        # TODO: function and data structure for getting object-lists
        object_list = ['MATERIAL', 'MATERIAL:AIRGAP']
        for key, layer in product(object_list, layers):
            try:
                rvalue += ddtt.theidf.getobject(key, layer).rvalue
            except AttributeError:
                pass
    return rvalue

def ufactor(ddtt):
    """
    U factor (W/m2-K) of a construction or material.
    1 / R value (W/K)
    """
    return 1 / rvalue(ddtt)
    
def ufactor_ip(ddtt):
    """return ufactor in IP inits"""
    # quick fix for Santosh. Needs to thought thru
    mult = 0.076 / 0.429 # base on doing conversion in the table report
    return ufactor(ddtt) * mult

def rvalue_ip(ddtt):
    """return R value in IP units"""
    # quick fix for Santosh. Needs to thought thru
    return 1. /  ufactor_ip(ddtt)       

def heatcapacity(ddtt):
    """
    Heat capacity (kJ/m2-K) of a construction or material.
    thickness (m) * density (kg/m3) * specific heat (J/kg-K) * 0.001
    """
    if ddtt.obj[0] == 'Material':
        thickness = ddtt.obj[ddtt.objls.index('Thickness')]
        density = ddtt.obj[ddtt.objls.index('Density')]
        specificheat = ddtt.obj[ddtt.objls.index('Specific_Heat')]
        heatcapacity = thickness * density * specificheat * 0.001
    elif ddtt.obj[0] == 'Material:AirGap':
        heatcapacity = 0
    elif ddtt.obj[0] == 'Construction':
        heatcapacity = 0
        layers = ddtt.obj[2:]
        object_list = ['MATERIAL', 'MATERIAL:AIRGAP']
        for key, layer in product(object_list, layers):
            try:
                heatcapacity += ddtt.theidf.getobject(key, layer).heatcapacity
            except AttributeError:
                pass
    return heatcapacity
        
