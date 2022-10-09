# Copyright (c) 2012, 2022 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""idd comments have gaps in them.
With \note fields as indicated
This code fills those gaps
see: SCHEDULE:DAY:LIST as an example"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

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
#
# find objects where the fields are not named
# do the following only for those objects
# find the first field that has an integer. This is a repeating field
# gather the repeating field names (without the integer)
# generate all the repeating fields for all variables


import eppy.bunchhelpers as bunchhelpers


def cleaniddfield(acomm):
    """make all the keys lower case"""
    for key in list(acomm.keys()):
        val = acomm[key]
        acomm[key.lower()] = val
    for key in list(acomm.keys()):
        val = acomm[key]
        if key != key.lower():
            acomm.pop(key)
    return acomm


def cleancommdct(commdct):
    """make all keys in commdct lower case"""
    return [[cleaniddfield(fcomm) for fcomm in comm] for comm in commdct]


def getfields(comm):
    """get all the fields that have the key 'field'"""
    fields = []
    for field in comm:
        if "field" in field:
            fields.append(field)
    return fields


def repeatingfieldsnames(fields, int_replace=None):
    """get the names of the repeating fields"""
    if not int_replace:
        int_replace = "%s"
    fnames = [field["field"][0] for field in fields]
    fnames = [bunchhelpers.onlylegalchar(fname) for fname in fnames]
    fnames = [fname for fname in fnames if bunchhelpers.intinlist(fname.split())]
    fnames = [(bunchhelpers.replaceint(fname, int_replace), None) for fname in fnames]
    dct = dict(fnames)
    repnames = fnames[: len(list(dct.keys()))]
    return repnames


def a_missingkey_standard(commdct, key_i, key_txt, nofirstfields):
    """
    sometimes IDD has fields with no field description. This happens in extensible.
    This functions picks up the previous field description and adds them
    to the fields that have no field descriptions. This update is done in place to commdct
    commdct is not returned.
    missing field descriptions are actually mising keys of a dict
    hence the function is called a missingkey

    This is very old function. Not sure how it works now.
    """
    comm = commdct[key_i]

    # get all fields
    fields = getfields(comm)

    # get repeating field names
    repnames = repeatingfieldsnames(fields)

    try:
        first = repnames[0][0] % (1,)
    except IndexError:
        nofirstfields.append(key_txt)
        return nofirstfields

    # get all comments of the first repeating field names
    firstnames = [repname[0] % (1,) for repname in repnames]
    fcomments = [
        field
        for field in fields
        if bunchhelpers.onlylegalchar(field["field"][0]) in firstnames
    ]
    fcomments = [dict(fcomment) for fcomment in fcomments]
    for cmt in fcomments:
        fld = cmt["field"][0]
        fld = bunchhelpers.onlylegalchar(fld)
        fld = bunchhelpers.replaceint(fld)
        cmt["field"] = [fld]

    for i, cmt in enumerate(comm[1:]):
        thefield = cmt["field"][0]
        thefield = bunchhelpers.onlylegalchar(thefield)
        if thefield == first:
            break
    first_i = i + 1

    newfields = []
    for i in range(1, len(comm[first_i:]) // len(repnames) + 1):
        for fcomment in fcomments:
            nfcomment = dict(fcomment)
            fld = nfcomment["field"][0]
            fld = fld % (i,)
            nfcomment["field"] = [fld]
            newfields.append(nfcomment)

    for i, cmt in enumerate(comm):
        if i < first_i:
            continue
        else:
            afield = newfields.pop(0)
            comm[i] = afield
    commdct[key_i] = comm
    return nofirstfields


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
            # return nofirstfields
        key_i = dtls.index(key_txt.upper())
        # a_missingkey_standard_1(commdct[key_i], key_txt, nofirstfields)
        a_missingkey_standard(commdct, key_i, key_txt, nofirstfields)
    return nofirstfields


def missingkeys_nonstandard(block, commdct, dtls, objectlist, afield="afiled %s"):
    """This is an object list where thre is no first field name
    to give a hint of what the first field name should be"""
    afield = "afield %s"
    for key_txt in objectlist:
        key_i = dtls.index(key_txt.upper())
        comm = commdct[key_i]
        if block:
            blk = block[key_i]
        for i, cmt in enumerate(comm):
            if cmt == {}:
                first_i = i
                break
        for i, cmt in enumerate(comm):
            if i >= first_i:
                if block:
                    comm[i]["field"] = ["%s" % (blk[i])]
                else:
                    comm[i]["field"] = [afield % (i - first_i + 1,)]
