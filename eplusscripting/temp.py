# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""figure out the rename"""
from modeleditor import IDF


def dctvalue(dct, key):
    if dct.has_key(key):
        return dct[key]
    else:
        return None

<<<<<<< HEAD
iddfile = "../iddfiles/Energy+V7_2_0.idd"
=======
iddname = "../iddfiles/Energy+V7_2_0.idd"
>>>>>>> eppy
fname = "../idffiles/V_7_2/constructions.idf"
IDF.setiddname(iddname)
idf = IDF(fname)

consts = idf.idfobjects['construction'.upper()]
mats = idf.idfobjects['Material'.upper()]
intwall = [const for const in consts if const.Name == 'Interior Wall'][0]

matname = 'G01a 19mm gypsum board'
mat = [m for m in mats if m.Name == matname][0]

# def rename(idf, objkey, objname, newname):
#     refnames = xxx()
#     for refname in refnames:
#         for robjkey in objkeys:
#             for robj in objects[robjkey]:
#                 fieldidds = getfieldidds()
#                 for field in fieldidds:
#                     objectlistname = getobjlistname()
#                     if refname == objectlistname: # case-insensitive
#                         if objname = valueoffield():
#                             changedvalueofifled()
#                             
# def rename(idf, objname, newname):
#     refnames = getrefnames(idf, objname)
#     for refname in refnames:
#         for idfobj in idfobjects: # for each idfobject
#             for fielddata in idfobjfields(idfobj): # for each field
#                 ilist = referedin(refname, objname, fieldata)
#                 if ilist:
#                     for i in ilist: # for each positive field
#                         renamefield(idfobj, )

def rename(idf, objkey, objname, newname):
    refnames = getrefnames(idf, objkey)
    objlists = getallobjlists(idf.idf_info, refname) 
    # [('OBJKEY', refname, fieldindexlist), ...]
    for refname in refnames:
        for robjkey, refname, fieldindexlist in idfobjects:
            idfobjects = idf.idfobjects[robjkey]
            for idfobject in idfobjects:
                for findex in fieldindexlist: # for each field
                    if idfobject[idfobject[findex]] == objname:
                        idfobject[idfobject[findex]] = newname
                    



# getreferencename(idf, objkey, objname)
# there may be multiple references
# field may not be Name, but may end with Name
# Don't check for Name, check for reference
ref = [idd for idd in idds if dctvalue(idd, 'field') == ['Name']][0]['reference'][0]

# for refname in refnames
# findreferences(idf, objkey, objname, refname):
# return idfobject, index
#
# the refname in object_list may be a substring
    # look at oll refnames to see if substring works
    # might have to be case insensitive
cidds = const.objidd
irefered = [i for i, idd in enumerate(cidds) if dctvalue(idd, 'object-list') == [ref]]

# dorename(idfobject, indices, oldname, newname)
for i in irefered:
    try:
        print intwall.obj[i]
        if intwall.obj[i] == matname:
            print i
    except IndexError, e:
        pass
# updatereferences(idfobject, )