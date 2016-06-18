# Copyright (c) 2012-2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""functions that work with idf objects
some such functions are in modeleditor.py too"""
# TODO : maybe some of the functions in modeleditor can be move here.
# Copyright dates above depend on moving functions form modeleditor

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools

def getzonesurfaces(idf, zone):
    """get a list of surfaces belonging to the zone"""
    def issurface(surf):
        """Returns True if surf is a surface"""
        theidd = surf.getidd('Name')
        return u'SurfaceNames' in theidd[u'reference']
    glist = idf.getiddgroupdict()
    thermalgroup = u'Thermal Zones and Surfaces'
    objkeys = glist[thermalgroup]
    surfaces = [idf.idfobjects[objkey.upper()] for objkey in objkeys]
    surfaces = list(itertools.chain.from_iterable(surfaces)) # flatten list
    surfaces = [surface for surface in surfaces if issurface(surface)]
    surfs = [surf for surf in surfaces 
                if zone.isequal('Name', surf.Zone_Name)]
    return surfs

