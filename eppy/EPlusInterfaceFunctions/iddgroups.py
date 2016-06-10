# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
"""extract the groups from the iddfile"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd

def idd2group(fhandle):
    """wrapper for iddtxt2groups"""
    try:
        txt = fhandle.read()
        return iddtxt2groups(txt)
    except AttributeError as e:
        txt = open(fhandle, 'r').read()
        return iddtxt2groups(txt)


def iddtxt2groups(txt):
    """extract the groups from the idd file"""
    txt = parse_idd.nocomment(txt, '!')
    txt = txt.replace("\\group", "!-group") # retains group in next line
    txt = parse_idd.nocomment(txt, '\\') # remove all other idd info
    lines = txt.splitlines()
    lines = [line.strip() for line in lines] # cleanup
    lines = [line for line in lines if line != ''] # cleanup
    txt = '\n'.join(lines)
    gsplits = txt.split('!') # split into groups, since we have !-group
    gsplits = [gsplit.splitlines() for gsplit in gsplits] # split group

    gsplits[0].insert(0, None)
        # Put None for the first group that does nothave a group name
    gdict = {}
    for gsplit in gsplits:
        gdict.update({gsplit[0]:gsplit[1:]})
        # makes dict {groupname:[k1, k2], groupname2:[k3, k4]}

    gdict = {k:'\n'.join(v) for k, v in gdict.items()}# joins lines back
    gdict = {k:v.split(';') for k, v in gdict.items()} # splits into idfobjects
    gdict = {k:[i.strip() for i in v] for k, v in gdict.items()} # cleanup
    gdict = {k:[i.splitlines() for i in v] for k, v in gdict.items()}
        # splits idfobjects into lines
    gdict = {k:[i for i in v if len(i) > 0] for k, v in gdict.items()}
        # cleanup - removes blank lines
    gdict = {k:[i[0] for i in v] for k, v in gdict.items()} # use first line
    gdict = {k:[i.split(',')[0] for i in v] for k, v in gdict.items()}
        # remove ','
    nvalue = gdict.pop(None) # remove group with no name
    gdict = {k[len('-group '):]:v for k, v in gdict.items()} # get group name
    gdict.update({None:nvalue}) # put back group with no name
    return gdict
