# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""useful functions that should in the class IDF. 
write them here first as a development step.
If they are really useful and don't muddy waters include them in IDF
and remove them here"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import itertools
from io import StringIO
from past.builtins import basestring  # pip install future

from eppy.modeleditor import IDF
from eppy.bunch_subclass import BadEPFieldError


def idfobjectkeys(idf):
    """returns the object keys in the order they were in the IDD file
    it is an ordered list of idf.idfobjects.keys()
    keys of a dict are unordered, so idf.idfobjects.keys() will not work for this purpose"""
    return idf.model.dtls


def getanymentions(idf, anidfobject):
    """Find out if idjobject is mentioned an any object anywhere"""
    name = anidfobject.obj[1]
    foundobjs = []
    keys = idfobjectkeys(idf)
    idfkeyobjects = [idf.idfobjects[key.upper()] for key in keys]
    for idfobjects in idfkeyobjects:
        for idfobject in idfobjects:
            if name.upper() in [
                item.upper() for item in idfobject.obj if isinstance(item, basestring)
            ]:
                foundobjs.append(idfobject)
    return foundobjs


def getobject_use_prevfield(idf, idfobject, fieldname):
    """field=object_name, prev_field=object_type. Return the object"""
    if not fieldname.endswith("Name"):
        return None
    # test if prevfieldname ends with "Object_Type"
    fdnames = idfobject.fieldnames
    ifieldname = fdnames.index(fieldname)
    prevfdname = fdnames[ifieldname - 1]
    if not prevfdname.endswith("Object_Type"):
        return None
    objkey = idfobject[prevfdname].upper()
    objname = idfobject[fieldname]
    try:
        foundobj = idf.getobject(objkey, objname)
    except KeyError as e:
        return None
    return foundobj


def getidfkeyswithnodes():
    """return a list of keys of idfobjects that hve 'None Name' fields"""
    idf = IDF(StringIO(""))
    keys = idfobjectkeys(idf)
    keysfieldnames = ((key, idf.newidfobject(key.upper()).fieldnames) for key in keys)
    keysnodefdnames = (
        (key, (name for name in fdnames if (name.endswith("Node_Name"))))
        for key, fdnames in keysfieldnames
    )
    nodekeys = [key for key, fdnames in keysnodefdnames if list(fdnames)]
    return nodekeys


def getobjectswithnode(idf, nodekeys, nodename):
    """return all objects that mention this node name"""
    keys = nodekeys
    # TODO getidfkeyswithnodes needs to be done only once. take out of here
    listofidfobjects = (
        idf.idfobjects[key.upper()] for key in keys if idf.idfobjects[key.upper()]
    )
    idfobjects = [idfobj for idfobjs in listofidfobjects for idfobj in idfobjs]
    objwithnodes = []
    for obj in idfobjects:
        values = obj.fieldvalues
        fdnames = obj.fieldnames
        for value, fdname in zip(values, fdnames):
            if fdname.endswith("Node_Name"):
                if value == nodename:
                    objwithnodes.append(obj)
                    break
    return objwithnodes


def name2idfobject(idf, groupnamess=None, objkeys=None, **kwargs):
    """return the object, if the Name or some other field is known.
    send field in ``**kwargs`` as Name='a name', Roughness='smooth'
    Returns the first find (field search is unordered)
    objkeys -> if objkeys=['ZONE', 'Material'], search only those
    groupnames -> not yet coded"""
    # TODO : this is a very slow search. revist to speed it up.
    if not objkeys:
        objkeys = idfobjectkeys(idf)
    for objkey in objkeys:
        idfobjs = idf.idfobjects[objkey.upper()]
        for idfobj in idfobjs:
            for key, val in kwargs.items():
                try:
                    if idfobj[key] == val:
                        return idfobj
                except BadEPFieldError as e:
                    continue


def getidfobjectlist(idf):
    """return a list of all idfobjects in idf"""
    idfobjects = idf.idfobjects
    # idfobjlst = [idfobjects[key] for key in idfobjects if idfobjects[key]]
    idfobjlst = [idfobjects[key] for key in idf.model.dtls if idfobjects[key]]
    # `for key in idf.model.dtls` maintains the order
    # `for key in idfobjects` does not have order
    idfobjlst = itertools.chain.from_iterable(idfobjlst)
    idfobjlst = list(idfobjlst)
    return idfobjlst


def copyidfintoidf(toidf, fromidf):
    """copy fromidf completely into toidf"""
    idfobjlst = getidfobjectlist(fromidf)
    for idfobj in idfobjlst:
        toidf.copyidfobject(idfobj)
