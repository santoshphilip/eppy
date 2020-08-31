# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""some helper files"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from string import ascii_letters, digits


def onlylegalchar(name):
    """return only legal chars"""
    legalchar = ascii_letters + digits + " "
    return "".join([s for s in name[:] if s in legalchar])


def makefieldname(namefromidd):
    """made a field name that can be used by bunch"""
    newname = onlylegalchar(namefromidd)
    bunchname = newname.replace(" ", "_")
    return bunchname


def matchfieldnames(field_a, field_b):
    """Check match between two strings, ignoring case and spaces/underscores.

    Parameters
    ----------
    a : str
    b : str

    Returns
    -------
    bool

    """
    normalised_a = field_a.replace(" ", "_").lower()
    normalised_b = field_b.replace(" ", "_").lower()

    return normalised_a == normalised_b


def intinlist(lst):
    """test if int in list"""
    for item in lst:
        try:
            item = int(item)
            return True
        except ValueError:
            pass
    return False


def replaceint(fname, replacewith="%s"):
    """replace int in lst"""
    words = fname.split()
    for i, word in enumerate(words):
        try:
            word = int(word)
            words[i] = replacewith
        except ValueError:
            pass
    return " ".join(words)


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


def scientificnotation(val, width=19):
    """return val in scientific notation if it is wider than 'width' chars
    otherwise return val with no change"""
    vtxt = "%s" % (val)
    if len(vtxt) > width:
        try:
            stxt = "%e" % (val,)
            return stxt
        except TypeError as e:
            return val
    return val
