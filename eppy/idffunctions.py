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

def getzonesurfaces(idf, zname):
    """get a list of surfaces belonging to the zone"""
    # TODO : code this for idf object, not the name.
    # get BuildingSurface:Detailed
    detailedbsurfaces = idf.idfobjects["BuildingSurface:Detailed".upper()]
    surfs = [surf.Name for surf in detailedbsurfaces if surf.Zone_Name == zname]
    return surfs

