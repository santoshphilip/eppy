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

"""idd comments have gaps in them.
With \note fields as indicated
This code fills those gaps
see: SCHEDULE:DAY:LIST as an example"""

# see iddgaps6.py on usage
# TODO : need unit tests for all htese functions


# works for all objects, including troublesome ones
# factor the code i  iddgaps4.py into functions


# idd might look like this
# <snip>
# / field varA 1
# / field varB 1
# / field varC 1
# / field varA 2
# / field varB 2
# / field varC 2
# / above pattern continues
# - 
# find objects where the fields are not named
# do the following only for those objects
# find the first field that has an integer. This is a repeating field
# gather the repeating field names (without the integer)
# generate all the repeating fields for all variables



import sys
from pprint import pprint
from EPlusInterfaceFunctions import readidf

import bunchhelpers

def cleaniddfield(acomm):
    """make all the keys lower case"""
    for key in acomm.keys():
        val = acomm[key]
        acomm[key.lower()] = val
    for key in acomm.keys():
        val = acomm[key]
        if key != key.lower():
            acomm.pop(key)
    return acomm
    
def cleancommdct(commdct):
    """make all keys in commdct lower case"""
    return [[cleaniddfield(fcomm) for fcomm in comm] for comm in commdct]    
    
def getfields(comm):
    """get all the fields that have the key 'field' """
    fields = []
    for field in comm:
        if field.has_key('field'):
            fields.append(field)
    return fields
    
def repeatingfieldsnames(fields):
    """get the names of the repeating fields"""
    fnames = [field['field'][0] for field in fields]
    fnames = [bunchhelpers.onlylegalchar(fname) for fname in fnames]
    fnames = [fname for fname in fnames if bunchhelpers.intinlist(fname.split())]
    fnames = [(bunchhelpers.replaceint(fname), None) for fname in fnames]
    dct = dict(fnames)
    repnames = fnames[:len(dct.keys())]
    return repnames
    

# TODO : looks like "TABLE:MULTIVARIABLELOOKUP" will have to be skipped for now.
def missingkeys_standard(commdct, dtls, skiplist=None):
    """put missing keys in commdct for standard objects
    return a list of keys where it is unable to do so
    commdct is not returned, but is updated"""
    if skiplist == None:
        skiplist = []
    # find objects where all the fields are not named
    gkeys = [dtls[i] for i in range(len(dtls)) if commdct[i].count({}) > 2]
    nofirstfields = []
    # operatie on those fields
    for key_txt in gkeys:
        if key_txt in skiplist:
            continue
        # print key_txt
        # for a function, pass comm as a variable
        key_i = dtls.index(key_txt.upper())
        comm = commdct[key_i]



        # get all fields
        fields = getfields(comm)
    
        # get repeating field names
        repnames = repeatingfieldsnames(fields)
    
        try:
            first = repnames[0][0] % (1, )
        except IndexError, e:
            nofirstfields.append(key_txt)
            continue
        # print first

        # get all comments of the first repeating field names
        firstnames = [repname[0] % (1, ) for repname in repnames]
        fcomments = [field for field in fields if bunchhelpers.onlylegalchar(field['field'][0]) in firstnames]
        fcomments = [dict(fcomment) for fcomment in fcomments]
        for cm in fcomments:
            fld = cm['field'][0]
            fld = bunchhelpers.onlylegalchar(fld)
            fld = bunchhelpers.replaceint(fld)
            cm['field'] = [fld]

        for i, cm in enumerate(comm[1:]):
            thefield = cm['field'][0]
            thefield = bunchhelpers.onlylegalchar(thefield)
            if thefield == first:
                break
        first_i = i + 1

        newfields = []
        for i in range(1, len(comm[first_i:]) / len(repnames) + 1):
            for fcomment in fcomments:
                nfcomment = dict(fcomment)
                fld = nfcomment['field'][0]
                fld = fld % (i, )
                nfcomment['field'] = [fld]
                newfields.append(nfcomment)

        for i, cm in enumerate(comm):
            if i < first_i:
                continue
            else:
                afield = newfields.pop(0)
                comm[i] = afield
        commdct[key_i] = comm
    return nofirstfields

def missingkeys_nonstandard(commdct, dtls, objectlist, afield='afiled %s'):
    """This is an object list where thre is no first field name 
    to give a hint of what the first field name should be"""
    afield = 'afield %s'
    for key_txt in objectlist:
        key_i = dtls.index(key_txt.upper())
        comm = commdct[key_i]
        for i, cm in enumerate(comm):
            if cm == {}:
                first_i = i
                break
        for i, cm in enumerate(comm):
            if i >= first_i:
                comm[i]['field'] = afield % (i - first_i +1,)
