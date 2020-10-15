# -*- coding: utf-8 -*-
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
import warnings


INSIDE_FILM_R = 0.12
OUTSIDE_FILM_R = 0.03


def rvalue(ddtt):
    """
    R value (m2-K/W) of a construction or material.
    thickness (m) / conductivity (W/m-K)
    """
    object_type = ddtt.obj[0]
    if object_type == "Construction":
        rvalue = INSIDE_FILM_R + OUTSIDE_FILM_R
        layers = ddtt.obj[2:]
        field_idd = ddtt.getfieldidd("Outside_Layer")
        validobjects = field_idd["validobjects"]
        for layer in layers:
            found = False
            for key in validobjects:
                try:
                    rvalue += ddtt.theidf.getobject(key, layer).rvalue
                    found = True
                except AttributeError:
                    pass
            if not found:
                raise AttributeError("%s material not found in IDF" % layer)
    elif object_type == "Material":
        thickness = ddtt.obj[ddtt.objls.index("Thickness")]
        conductivity = ddtt.obj[ddtt.objls.index("Conductivity")]
        rvalue = thickness / conductivity
    elif object_type == "Material:AirGap":
        rvalue = ddtt.obj[ddtt.objls.index("Thermal_Resistance")]
    elif object_type == "Material:InfraredTransparent":
        rvalue = 0
    elif object_type == "Material:NoMass":
        rvalue = ddtt.obj[ddtt.objls.index("Thermal_Resistance")]
    elif object_type == "Material:RoofVegetation":
        warnings.warn(
            "Material:RoofVegetation thermal properties are based on dry soil",
            UserWarning,
        )
        thickness = ddtt.obj[ddtt.objls.index("Thickness")]
        conductivity = ddtt.obj[ddtt.objls.index("Conductivity_of_Dry_Soil")]
        rvalue = thickness / conductivity
    else:
        raise AttributeError("%s rvalue property not implemented" % object_type)
    return rvalue


def ufactor(ddtt):
    """
    U factor (W/m2-K) of a construction or material.
    1 / R value (W/K)
    """
    return 1 / rvalue(ddtt)


def ufactor_ip(ddtt):
    """
    U factor (BTU/(h °F ft^2)) of a construction or material.
    1 / R value (ft^2 °F hr/Btu)
    """
    # quick fix for Santosh. Needs to thought thru
    mult = 0.076 / 0.429  # base on doing conversion in the table report
    return ufactor(ddtt) * mult


def rvalue_ip(ddtt):
    """return R value in IP units"""
    # quick fix for Santosh. Needs to thought thru
    return 1 / ufactor_ip(ddtt)


def heatcapacity(ddtt):
    """
    Heat capacity (kJ/m2-K) of a construction or material.
    thickness (m) * density (kg/m3) * specific heat (J/kg-K) * 0.001
    """
    object_type = ddtt.obj[0]
    if object_type == "Construction":
        heatcapacity = 0
        layers = ddtt.obj[2:]
        field_idd = ddtt.getfieldidd("Outside_Layer")
        validobjects = field_idd["validobjects"]
        for layer in layers:
            found = False
            for key in validobjects:
                try:
                    heatcapacity += ddtt.theidf.getobject(key, layer).heatcapacity
                    found = True
                except AttributeError:
                    pass
            if not found:
                raise AttributeError("%s material not found in IDF" % layer)
    elif object_type == "Material":
        thickness = ddtt.obj[ddtt.objls.index("Thickness")]
        density = ddtt.obj[ddtt.objls.index("Density")]
        specificheat = ddtt.obj[ddtt.objls.index("Specific_Heat")]
        heatcapacity = thickness * density * specificheat * 0.001
    elif object_type == "Material:AirGap":
        heatcapacity = 0
    elif object_type == "Material:InfraredTransparent":
        heatcapacity = 0
    elif object_type == "Material:NoMass":
        warnings.warn(
            "Material:NoMass materials included in heat capacity calculation",
            UserWarning,
        )
        heatcapacity = 0
    elif object_type == "Material:RoofVegetation":
        warnings.warn(
            "Material:RoofVegetation thermal properties are based on dry soil",
            UserWarning,
        )
        thickness = ddtt.obj[ddtt.objls.index("Thickness")]
        density = ddtt.obj[ddtt.objls.index("Density_of_Dry_Soil")]
        specificheat = ddtt.obj[ddtt.objls.index("Specific_Heat_of_Dry_Soil")]
        heatcapacity = thickness * density * specificheat * 0.001
    else:
        raise AttributeError("%s has no heatcapacity property" % object_type)
    return heatcapacity
