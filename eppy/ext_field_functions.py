# Copyright (c) 2022 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""functions to deal with extensible fields
Moving the functions here is a work in progress"""


import eppy.iddgaps as iddgaps
import eppy.bunchhelpers as bunchhelpers


def getextensible(objidd):
    """return the extensible from the idd"""
    keys = objidd[0].keys()
    extkey = [key for key in keys if key.startswith("extensible")]
    if extkey:
        extens = extkey[0].split(":")[-1]
        return int(extens)
    else:
        return None


def extension_of_extensible(objidd, objblock, n):
    """generate the list of new vars needed to extend by n"""
    ext = getextensible(objidd)
    n = n // ext
    lastvars = endof_extensible(ext, objblock)
    alpha_lastvars = [i[0] for i in lastvars]
    int_lastvars = [int(i[1:]) for i in lastvars]
    lst = []
    for alpha, start in zip(alpha_lastvars, int_lastvars):
        step = alpha_lastvars.count(alpha)
        rng = range(start + step, start + 1 + n * step, step)
        lst.append(["{}{}".format(alpha, item) for item in rng])

    from itertools import chain

    return list(chain(*zip(*lst)))


def endof_extensible(extensible, thisblock):
    """get the vars from where extension happens"""
    return thisblock[-extensible:]


def increaseIDDfields(block, commdct, key_i, key_txt, n):
    """increase fields in IDD - ie in block and commdct"""
    extlst = extension_of_extensible(commdct[key_i], block[key_i], n)
    block[key_i] = block[key_i] + extlst
    commdct[key_i] = commdct[key_i] + [{}] * len(extlst)
    nofirstfields = []
    # print(commdct[key_i])
    iddgaps.a_missingkey_standard(commdct, key_i, key_txt, nofirstfields)
    objfields = [comm.get("field") for comm in commdct[key_i]]
    return objfields


# def increaseIDDfields_1(o_block, o_commdct, key_txt, n):
#     """increase fields in IDD - ie in block and commdct"""
#     print(o_commdct)
#     extlst = extension_of_extensible(o_commdct, o_block, n)
#     # o_block = o_block + extlst
#     o_block.append(extlst)
#     # o_commdct = o_commdct + [{}] * len(extlst)
#     o_commdct.append([{}] * len(extlst))
#     nofirstfields = []
#     # print(o_commdct)
#     iddgaps.a_missingkey_standard_1(o_commdct, key_txt, nofirstfields)
#     objfields = [comm.get("field") for comm in o_commdct]
#     return objfields


def islegalextensiblefield(objidd, fieldname):
    """return true if afieldname is an extensible field in objidd"""
    comm = objidd
    if getextensible(comm):
        if " " not in fieldname:  # a space instead of a underscore will return True
            # the code below is a little wierd
            fields = iddgaps.getfields(comm)
            repnames_tuples = iddgaps.repeatingfieldsnames(fields, "0")
            repnames = [bunchhelpers.makefieldname(item[0]) for item in repnames_tuples]
            fieldname_spaces = fieldname.replace("_", " ")
            fieldname_spaces0 = bunchhelpers.replaceint(fieldname_spaces, "0")
            fieldname0 = bunchhelpers.makefieldname(fieldname_spaces0)
            expected = fieldname0 in repnames
        else:
            expected = False
    return expected


def extfieldint(fieldname, sep=None):
    """return the integer in the extensible field
    It there is more than one integer, it will return the last one"""
    if not sep:
        sep = "_"
    words = fieldname.split(sep)
    digits = [int(word) for word in words if word.isdigit()]
    if digits:
        return digits[-1]
    else:
        return None
