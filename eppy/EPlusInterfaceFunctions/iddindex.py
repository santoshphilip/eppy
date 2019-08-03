# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""module for idd_index data structure and functions to work with it
- idd_index indexes idd_info so that it is easy to search through it.
- idd_info is the datastructure that holds the info in the Energy+.idd file"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# possible data structure:
# idd_index = {
#     ref2names:{
#         MaterialName:[MATERIAL, MATERIAL:AIRGAP, ...]
#         ZoneName:[ZONE,]
#     },
#     name2refs:{
#         ZONE:[ZoneNames, OutFaceEnvNames, ...]
#         SCHEDULE:DAY:HOURLY:[DayScheduleNames, ScheduleAndDayScheduleNames]
#     },
#     fieldsthatrefer:{
#         WINDOW:[], # will be list of fields in the future
#         DOOR:[], # once I figure how to not list all the repeating fields
#     }
#
# }

# embedd (actually point to) some of this info in idd_info
# In [17]: construction.getfieldidd('Layer_2')
# Out[17]:
# {u'field': [u'Layer 2'],
#  u'object-list': [u'MaterialName'],
#  u'type': [u'object-list']}
# will now become:
# Out[17]:
# {u'field': [u'Layer 2'],
#  u'object-list': [u'MaterialName'],
#  'referedobjkeys':[MATERIAL, MATERIAL:AIRGAP, ...]
#  # MaterialName:[MATERIAL, MATERIAL:AIRGAP, ...] is the same list as in
#  # ref2names above, not a new list. So we don't use too much memory
#  u'type': [u'object-list']}

from eppy.bunch_subclass import getfieldidd_item


def makename2refdct(commdct):
    """make the name2refs dict in the idd_index"""
    refdct = {}
    for comm in commdct:  # commdct is a list of dict
        try:
            idfobj = comm[0]["idfobj"].upper()
            field1 = comm[1]
            if "Name" in field1["field"]:
                references = field1["reference"]
                refdct[idfobj] = references
        except (KeyError, IndexError) as e:
            continue  # not the expected pattern for reference
    return refdct


def makeref2namesdct(name2refdct):
    """make the ref2namesdct in the idd_index"""
    ref2namesdct = {}
    for key, values in name2refdct.items():
        for value in values:
            ref2namesdct.setdefault(value, set()).add(key)
    return ref2namesdct


def ref2names2commdct(ref2names, commdct):
    """embed ref2names into commdct"""
    for comm in commdct:
        for cdct in comm:
            try:
                refs = cdct["object-list"][0]
                validobjects = ref2names[refs]
                cdct.update({"validobjects": validobjects})
            except KeyError as e:
                continue
    return commdct
