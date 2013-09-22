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

"""track down references"""

from idfreader import idfreader

# iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
# fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
iddfile = "../iddfiles/Energy+V7_2_0.idd"
fname = "../idffiles/V_7_2/constructions.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)  

def getreferences(data, commdct, key):
    i = data.dtls.index(key)
    for fieldcomm in commdct[i]:
        if fieldcomm.has_key('reference'):
            if fieldcomm['field'][0].endswith('Name'):
                return fieldcomm['reference']
                
def getrefered_inner(data, commdct, refs):
    refered = {}
    for i, fieldcomms in enumerate(commdct):
        for j, fieldcomm in enumerate(fieldcomms):
            if fieldcomm.has_key('object-list'):
                theobjectlist = fieldcomm['object-list']
                refs = [ref.upper() for ref in refs]
                if theobjectlist[0].upper() in refs:
                    refered[data.dtls[i]] = j
    return refered
    
def getrefered(data, commdct, key):
    refs =  getreferences(data, commdct, key)
    return getrefered_inner(data, commdct, refs)
    
refered =  getrefered(data, commdct, 'construction'.upper())

# refered = {}
# for i, fieldcomms in enumerate(commdct):
#     for j, fieldcomm in enumerate(fieldcomms):
#         if fieldcomm.has_key('object-list'):
#             theobjectlist = fieldcomm['object-list']
#             refs = [ref.upper() for ref in refs]
#             if theobjectlist[0].upper() in refs:
#                 refered[data.dtls[i]] = j
#                 # print theobjectlist[0], data.dtls[i], j
for key, item in refered.items():
    print key, item


# for i, key in enumerate(data.dtls):
#     if key == 'ZONE':
#         for fieldcomm in commdct[i]:
#             if fieldcomm.has_key('reference'):
#                 if fieldcomm['field'][0].endswith('Name'):# != ["Name"]:
#                     print key
#                     print fieldcomm['field']
#                     print fieldcomm['reference']
#                     print fieldcomm.keys()
        # print key_comm
        # print
        # for comms in key_comm:
        #     print comms
        # for comm in comms:
        #     print comm
        #     if comm.has_key('reference'):
        #         print comm['field']
        #         print comm['reference']
    # if i > 3:
    #     break

# find reference    
# (key, name, field)