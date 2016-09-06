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
import itertools
from eppy.constructions import thermal_properties
from eppy.geometry import surface as g_surface


def grouper(num, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * num
    return zip_longest(fillvalue=fillvalue, *args)

def getcoords(ddtt):
    """return the coordinates of the surface"""
    n_vertices_index = ddtt.objls.index('Number_of_Vertices')
    first_x = n_vertices_index + 1 # X of first coordinate
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

def tilt(ddtt):
    """tilt of the surface"""
    coords = getcoords(ddtt)
    return g_surface.tilt(coords)

def buildingname(ddtt):
    """return building name"""
    idf = ddtt.theidf
    building = idf.idfobjects['building'.upper()][0]
    return building.Name
    
def zonesurfaces(ddtt):
    """return al list of surfaces that belong to the zone"""
    kwargs = {'fields':[u'Zone_Name', ],
        'iddgroups':[u'Thermal Zones and Surfaces', ]}
    return ddtt.getreferingobjs(**kwargs)
    
def subsurfaces(ddtt):
    """return al list of surfaces that belong to the zone"""
    kwargs = {'fields':[u'Building_Surface_Name', ],
        'iddgroups':[u'Thermal Zones and Surfaces', ]}
    return ddtt.getreferingobjs(**kwargs)
    
def rvalue(ddtt):
    rvalue = thermal_properties.rvalue(ddtt)
    return rvalue

def ufactor(ddtt):
    ufactor = thermal_properties.ufactor(ddtt)
    return ufactor

def ufactor_ip(ddtt):
    ufactor_ip = thermal_properties.ufactor_ip(ddtt)
    return ufactor_ip

def rvalue_ip(ddtt):
    rvalue_ip = thermal_properties.rvalue_ip(ddtt)
    return rvalue_ip

def heatcapacity(ddtt):
    heatcapacity = thermal_properties.heatcapacity(ddtt)
    return heatcapacity

