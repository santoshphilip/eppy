# Copyright (c) 2012 Santosh Philip
# Copyright (c) 2020 Cheng Cui
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""helper functions for the functions called by bunchdt"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
from itertools import zip_longest
from eppy.constructions import thermal_properties
from eppy.geometry import surface as g_surface
import eppy.fanpower


def grouper(num, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * num
    return zip_longest(fillvalue=fillvalue, *args)


def getcoords(ddtt):
    """return the coordinates of the surface"""
    n_vertices_index = ddtt.objls.index("Number_of_Vertices")
    first_x = n_vertices_index + 1  # X of first coordinate
    pts = ddtt.obj[first_x:]
    return list(grouper(3, pts))


def area(ddtt):
    """area of the surface"""
    coords = getcoords(ddtt)
    return g_surface.area(coords)


def height(ddtt):
    """height of the surface"""
    coords = getcoords(ddtt)
    return g_surface.height(coords)


def width(ddtt):
    """width of the surface"""
    coords = getcoords(ddtt)
    return g_surface.width(coords)


def azimuth(ddtt):
    """azimuth of the surface"""
    coords = getcoords(ddtt)
    return g_surface.azimuth(coords)


def true_azimuth(ddtt):
    """true azimuth of the surface"""
    idf = ddtt.theidf
    coord_system = idf.idfobjects["GlobalGeometryRules"][0].Coordinate_System
    if coord_system.lower() == "relative":
        zone_name = ddtt.Zone_Name
        bldg_north = idf.idfobjects["Building"][0].North_Axis
        zone_rel_north = idf.getobject("Zone", zone_name).Direction_of_Relative_North
        surf_azimuth = azimuth(ddtt)
        return g_surface.true_azimuth(bldg_north, zone_rel_north, surf_azimuth)
    elif coord_system.lower() in ("world", "absolute"):
        # NOTE: "absolute" is not supported in v9.3.0
        return azimuth(ddtt)
    else:
        raise ValueError(
            "'{:s}' is no valid value for 'Coordinate System'".format(coord_system)
        )


def tilt(ddtt):
    """tilt of the surface"""
    coords = getcoords(ddtt)
    return g_surface.tilt(coords)


def buildingname(ddtt):
    """return building name"""
    idf = ddtt.theidf
    building = idf.idfobjects["building".upper()][0]
    return building.Name


def zonesurfaces(ddtt):
    """return al list of surfaces that belong to the zone"""
    kwargs = {"fields": ["Zone_Name"], "iddgroups": ["Thermal Zones and Surfaces"]}
    return ddtt.getreferingobjs(**kwargs)


def subsurfaces(ddtt):
    """return al list of surfaces that belong to the zone"""
    kwargs = {
        "fields": ["Building_Surface_Name"],
        "iddgroups": ["Thermal Zones and Surfaces"],
    }
    return ddtt.getreferingobjs(**kwargs)


def rvalue(ddtt):
    return thermal_properties.rvalue(ddtt)


def ufactor(ddtt):
    return thermal_properties.ufactor(ddtt)


def ufactor_ip(ddtt):
    return thermal_properties.ufactor_ip(ddtt)


def rvalue_ip(ddtt):
    return thermal_properties.rvalue_ip(ddtt)


def heatcapacity(ddtt):
    return thermal_properties.heatcapacity(ddtt)


def fanpower_bhp(ddtt):
    """return fanpower in bhp"""
    return eppy.fanpower.fanpower_bhp(ddtt)


def fanpower_watts(ddtt):
    """return fanpower in watts"""
    return eppy.fanpower.fanpower_watts(ddtt)


def fan_maxcfm(ddtt):
    """return the Maximum_Flow_Rate in cfm"""
    return eppy.fanpower.fan_maxcfm(ddtt)
