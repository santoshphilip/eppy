# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""functions to use json to modify an idf file"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


def key2elements(key):
    """split key to elements"""
    # words = key.split('.')
    # if len(words) == 4:
    #     return words
    # # there is a dot in object name
    # fieldword = words.pop(-1)
    # nameword = '.'.join(words[-2:])
    # if nameword[-1] in ('"', "'"):
    #     # The object name is in quotes
    #     nameword = nameword[1:-1]
    # elements = words[:-2] + [nameword, fieldword, ]
    # return elements
    words = key.split(".")
    first2words = words[:2]
    lastword = words[-1]
    namewords = words[2:-1]
    namephrase = ".".join(namewords)
    if namephrase.startswith("'") and namephrase.endswith("'"):
        namephrase = namephrase[1:-1]
    return first2words + [namephrase] + [lastword]


def updateidf(idf, dct):
    """update idf using dct"""
    for key in list(dct.keys()):
        if key.startswith("idf."):
            idftag, objkey, objname, field = key2elements(key)
            if objname == "":
                try:
                    idfobj = idf.idfobjects[objkey.upper()][0]
                except IndexError as e:
                    idfobj = idf.newidfobject(objkey.upper())
            else:
                idfobj = idf.getobject(objkey.upper(), objname)
                if idfobj == None:
                    idfobj = idf.newidfobject(objkey.upper(), Name=objname)
            idfobj[field] = dct[key]
