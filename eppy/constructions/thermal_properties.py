# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Functions to calculate the thermal properties of constructions.
"""

INSIDE_FILM_R = 0.12
OUTSIDE_FILM_R = 0.03


def rvalue(ddtt):
    """thickness (m) / conductivity (W/m-K)
    """
    if ddtt.obj[0] == 'Material':
        thickness = ddtt.obj[ddtt.objls.index('Thickness')]
        conductivity = ddtt.obj[ddtt.objls.index('Conductivity')]
        rvalue = thickness / conductivity
    else:
        rvalue = INSIDE_FILM_R + OUTSIDE_FILM_R
        layers = ddtt.obj[2:]
        rvalue += sum(ddtt.theidf.getobject('MATERIAL', l).rvalue 
                      for l in layers)
    return rvalue

def ufactor(ddtt):
    """reciprocal of the r value (W/K)
    """
    return 1 / rvalue(ddtt)

def heatcapacity(ddtt):
    """thickness (m) * density (kg/m3) * specific heat (J/kg-K) * 0.001
    """
    if ddtt.obj[0] == 'Material':
        thickness = ddtt.obj[ddtt.objls.index('Thickness')]
        density = ddtt.obj[ddtt.objls.index('Density')]
        specificheat = ddtt.obj[ddtt.objls.index('Specific_Heat')]
        heatcapacity = thickness * density * specificheat * 0.001
    else:
        layers = ddtt.obj[2:]
        heatcapacity = sum(ddtt.theidf.getobject('MATERIAL', l).heatcapacity 
                      for l in layers)
    return heatcapacity
        
