# Copyright (c) 2012 Santosh Philip
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

from six.moves import zip_longest

import eppy.fanpower
from eppy.bunch_subclass import register_epbunch_function
from eppy.constructions import thermal_properties
from eppy.geometry import surface as g_surface


def grouper(num, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * num
    return zip_longest(fillvalue=fillvalue, *args)


@register_epbunch_function("coords", keys=None)
@property
def getcoords(ddtt):
    """return the coordinates of the surface"""
    n_vertices_index = ddtt.objls.index("Number_of_Vertices")
    first_x = n_vertices_index + 1  # X of first coordinate
    pts = ddtt.obj[first_x:]
    return list(grouper(3, pts))


@register_epbunch_function("area", keys=None)
@property
def area(ddtt):
    """area of the surface"""
    coords = ddtt.coords
    return g_surface.area(coords)


@register_epbunch_function("height", keys=None)
@property
def height(ddtt):
    """height of the surface"""
    coords = ddtt.coords
    return g_surface.height(coords)


@register_epbunch_function("width", keys=None)
@property
def width(ddtt):
    """width of the surface"""
    coords = ddtt.coords
    return g_surface.width(coords)


@register_epbunch_function("azimuth", keys=None)
@property
def azimuth(ddtt):
    """azimuth of the surface"""
    coords = ddtt.coords
    return g_surface.azimuth(coords)


@register_epbunch_function("tilt", keys=None)
@property
def tilt(ddtt):
    """tilt of the surface"""
    coords = ddtt.coords
    return g_surface.tilt(coords)


@register_epbunch_function("buildingname", keys=None)
@property
def buildingname(ddtt):
    """return building name"""
    idf = ddtt.theidf
    building = idf.idfobjects["building".upper()][0]
    return building.Name


@register_epbunch_function("zonesurfaces", keys=["ZONE"])
@property
def zonesurfaces(ddtt):
    """return al list of surfaces that belong to the zone"""
    kwargs = {"fields": ["Zone_Name"], "iddgroups": ["Thermal Zones and Surfaces"]}
    return ddtt.getreferingobjs(**kwargs)


@register_epbunch_function("subsurfaces", keys=None)
@property
def subsurfaces(ddtt):
    """return al list of surfaces that belong to the zone"""
    kwargs = {
        "fields": ["Building_Surface_Name"],
        "iddgroups": ["Thermal Zones and Surfaces"],
    }
    return ddtt.getreferingobjs(**kwargs)


@register_epbunch_function("rvalue", keys=None)
@property
def rvalue(ddtt):
    return thermal_properties.rvalue(ddtt)


@register_epbunch_function("ufactor", keys=None)
@property
def ufactor(ddtt):
    return thermal_properties.ufactor(ddtt)


@register_epbunch_function("ufactor_ip", keys=None)
@property
def ufactor_ip(ddtt):
    return thermal_properties.ufactor_ip(ddtt)


@register_epbunch_function("rvalue_ip", keys=None)
@property
def rvalue_ip(ddtt):
    return thermal_properties.rvalue_ip(ddtt)


@register_epbunch_function("heatcapacity", keys=None)
@property
def heatcapacity(ddtt):
    return thermal_properties.heatcapacity(ddtt)


@register_epbunch_function("f_fanpower_bhp", keys=None)
@property
def fanpower_bhp(ddtt):
    """return fanpower in bhp"""
    return eppy.fanpower.fanpower_bhp(ddtt)


@register_epbunch_function("f_fanpower_watts", keys=None)
@property
def fanpower_watts(ddtt):
    """return fanpower in watts"""
    return eppy.fanpower.fanpower_watts(ddtt)


@register_epbunch_function("f_fan_maxcfm", keys=None)
@property
def fan_maxcfm(ddtt):
    """return the Maximum_Flow_Rate in cfm"""
    return eppy.fanpower.fan_maxcfm(ddtt)
