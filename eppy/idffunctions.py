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

from eppy.bunch_subclass import BadEPFieldError

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

def getreferingobjs_old(idf, zone,
            refnames=None,
            iddgroup="all groups",
            referringfields=None):
    """Get a list of objects that refer to this object"""
    def isrefered(anobj, refnames):
        """Returns True if anobj.Name is referred to"""
        if not refnames:
            return True
        theidd = anobj.getidd('Name')
        for refname in refnames:
            if refname not in theidd[u'reference']:
                return False
        return True
    glist = idf.getiddgroupdict()
    try:
        # select only objects in the group
        objkeys = glist[iddgroup]
        objs = [idf.idfobjects[objkey.upper()] for objkey in objkeys]
    except KeyError as e:
        # select all objects
        objkeys = idf.idfobjects.keys()
        objs = [idf.idfobjects[objkey.upper()] for objkey in objkeys]
    objs = list(itertools.chain.from_iterable(objs)) # flatten list
    objs = [anobj for anobj in objs if isrefered(anobj, refnames)]
    # objs = [anobj for anobj in objs
    #             if zone.isequal('Name', anobj[referringfields])]
    fobjs = []
    for anobj in objs:
        try:
            if not referringfields:
                referringfields = anobj.objls[1:]
                try:
                    referringfields.remove('Name')
                except ValueError as e:
                    pass
            for referringfield in referringfields:
                fieldvalue = anobj[referringfield]
                if zone.isequal('Name', fieldvalue):
                    fobjs.append(anobj)
        except BadEPFieldError as e:
            continue
    return fobjs
    # return objs

def getreferingobjs(referedobj, iddgroups=None, fields=None):
    """Get a list of objects that refer to this object"""
    # pseudocode for code below
    # referringobjs = []
    # referedobj has: -> Name
    #                 -> reference
    # for each obj in idf:
    # [optional filter -> objects in iddgroup]
    #     each field of obj:
    #     [optional filter -> field in fieldlist]
    #         has object-list [refname]:
    #             if refname in reference:
    #                 if Name = field value:
    #                     referringobjs.append()
    referringobjs = []
    idf = referedobj.theidf
    referedidd = referedobj.getidd("Name")
    references = referedidd['reference']
    idfobjs = idf.idfobjects.values()
    idfobjs = list(itertools.chain.from_iterable(idfobjs)) # flatten list
    if iddgroups: # optional filter
        idfobjs = [anobj for anobj in idfobjs 
            if anobj.getidd('key')['group'] in iddgroups]
    for anobj in idfobjs:
        if not fields:
            thefields = anobj.objls
        else:
            thefields = fields
        for field in thefields:
            try:
                itsidd = anobj.getidd(field)
            except ValueError as e:
                continue
            if itsidd.has_key('object-list'):
                refname = itsidd['object-list'][0]
                if refname in references:
                    if referedobj.isequal('Name', anobj[field]):
                        referringobjs.append(anobj)
    return referringobjs
