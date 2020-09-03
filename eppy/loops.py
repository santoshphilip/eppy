# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""get the loop data to draw the diagram
Other notes:
- tested for idd version 6.0
- when E+ is updated, run versionchangecheck.py for the following objects
uses the following objects
['plantloop', ]
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def extractfields(data, commdct, objkey, fieldlists):
    """get all the objects of objkey.
    fieldlists will have a fieldlist for each of those objects.
    return the contents of those fields"""
    # TODO : this assumes that the field list identical for
    # each instance of the object. This is not true.
    # So we should have a field list for each instance of the object
    # and map them with a zip
    objindex = data.dtls.index(objkey)
    objcomm = commdct[objindex]
    objfields = []
    # get the field names of that object
    for dct in objcomm[0:]:
        try:
            thefieldcomms = dct["field"]
            objfields.append(thefieldcomms[0])
        except KeyError as err:
            objfields.append(None)
    fieldindexes = []
    for fieldlist in fieldlists:
        fieldindex = []
        for item in fieldlist:
            if isinstance(item, int):
                fieldindex.append(item)
            else:
                fieldindex.append(objfields.index(item) + 0)
                # the index starts at 1, not at 0
        fieldindexes.append(fieldindex)
    theobjects = data.dt[objkey]
    fieldcontents = []
    for theobject, fieldindex in zip(theobjects, fieldindexes):
        innerlst = []
        for item in fieldindex:
            try:
                innerlst.append(theobject[item])
            except IndexError as err:
                break
        fieldcontents.append(innerlst)
        # fieldcontents.append([theobject[item] for item in fieldindex])
    return fieldcontents


def plantloopfieldlists(data):
    """return the plantloopfield list"""
    objkey = "plantloop".upper()
    numobjects = len(data.dt[objkey])
    return [
        [
            "Name",
            "Plant Side Inlet Node Name",
            "Plant Side Outlet Node Name",
            "Plant Side Branch List Name",
            "Demand Side Inlet Node Name",
            "Demand Side Outlet Node Name",
            "Demand Side Branch List Name",
        ]
    ] * numobjects


def plantloopfields(data, commdct):
    """get plantloop fields to diagram it"""
    fieldlists = plantloopfieldlists(data)
    objkey = "plantloop".upper()
    return extractfields(data, commdct, objkey, fieldlists)


def branchlist2branches(data, commdct, branchlist):
    """get branches from the branchlist"""
    objkey = "BranchList".upper()
    theobjects = data.dt[objkey]
    fieldlists = []
    objnames = [obj[1] for obj in theobjects]
    for theobject in theobjects:
        fieldlists.append(list(range(2, len(theobject))))
    blists = extractfields(data, commdct, objkey, fieldlists)
    thebranches = [
        branches for name, branches in zip(objnames, blists) if name == branchlist
    ]
    return thebranches[0]


def branch_inlet_outlet(data, commdct, branchname):
    """return the inlet and outlet of a branch"""
    objkey = "Branch".upper()
    theobjects = data.dt[objkey]
    theobject = [obj for obj in theobjects if obj[1] == branchname]
    theobject = theobject[0]
    inletindex = 6
    outletindex = len(theobject) - 2
    return [theobject[inletindex], theobject[outletindex]]


def splittermixerfieldlists(data, commdct, objkey):
    """docstring for splittermixerfieldlists"""
    objkey = objkey.upper()
    objindex = data.dtls.index(objkey)
    objcomms = commdct[objindex]
    theobjects = data.dt[objkey]
    fieldlists = []
    for theobject in theobjects:
        fieldlist = list(range(1, len(theobject)))
        fieldlists.append(fieldlist)
    return fieldlists


def splitterfields(data, commdct):
    """get splitter fields to diagram it"""
    objkey = "Connector:Splitter".upper()
    fieldlists = splittermixerfieldlists(data, commdct, objkey)
    return extractfields(data, commdct, objkey, fieldlists)


def mixerfields(data, commdct):
    """get mixer fields to diagram it"""
    objkey = "Connector:Mixer".upper()
    fieldlists = splittermixerfieldlists(data, commdct, objkey)
    return extractfields(data, commdct, objkey, fieldlists)


def repeatingfields(theidd, commdct, objkey, flds):
    """return a list of repeating fields
    fld is in format 'Component %s Name'
    so flds = [fld % (i, ) for i in range(n)]
    does not work for 'fields as indicated'"""
    # TODO : make it work for 'fields as indicated'
    if type(flds) != list:
        flds = [flds]  # for backward compatability
    objindex = theidd.dtls.index(objkey)
    objcomm = commdct[objindex]
    allfields = []
    for fld in flds:
        thefields = []
        indx = 1
        for i in range(len(objcomm)):
            try:
                thefield = fld % (indx,)
                if objcomm[i]["field"][0] == thefield:
                    thefields.append(thefield)
                    indx = indx + 1
            except KeyError as err:
                pass
        allfields.append(thefields)
    allfields = list(zip(*allfields))
    return [item for sublist in allfields for item in sublist]


def objectcount(data, key):
    """return the count of objects of key"""
    objkey = key.upper()
    return len(data.dt[objkey])


def getfieldindex(data, commdct, objkey, fname):
    """given objkey and fieldname, return its index"""
    objindex = data.dtls.index(objkey)
    objcomm = commdct[objindex]
    for i_index, item in enumerate(objcomm):
        try:
            if item["field"] == [fname]:
                break
        except KeyError as err:
            pass
    return i_index


def getadistus(data, commdct):
    """docstring for fname"""
    objkey = "ZoneHVAC:AirDistributionUnit".upper()
    objindex = data.dtls.index(objkey)
    objcomm = commdct[objindex]
    adistutypefield = "Air Terminal Object Type"
    ifield = getfieldindex(data, commdct, objkey, adistutypefield)
    adistus = objcomm[ifield]["key"]
    return adistus


def makeadistu_inlets(data, commdct):
    """make the dict adistu_inlets"""
    adistus = getadistus(data, commdct)
    # assume that the inlet node has the words "Air Inlet Node Name"
    airinletnode = "Air Inlet Node Name"
    adistu_inlets = {}
    for adistu in adistus:
        objkey = adistu.upper()
        objindex = data.dtls.index(objkey)
        objcomm = commdct[objindex]
        airinlets = []
        for i, comm in enumerate(objcomm):
            try:
                if comm["field"][0].find(airinletnode) != -1:
                    airinlets.append(comm["field"][0])
            except KeyError as err:
                pass
        adistu_inlets[adistu] = airinlets
    return adistu_inlets
