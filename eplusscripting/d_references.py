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

"""find the references that are refered to by object-list
check for any wierdness
conclusions:
1. references will need case-insensitive test
2. there are references that are not there in object-list
3. the substring 'And' does not mean two seperate references
4. all references are of field .endswith('Name')"""
# develop a series of tests here for every time the idd updates, to see if these rules change
# only 4. needs to tested
# running this script will do it

from modeleditor import IDF
from StringIO import StringIO
iddname = "../iddfiles/Energy+V8_0_0.idd"
IDF.setiddname(iddname)
idf = IDF(StringIO(""))
idds = idf.idd_info

refs = {}
olist = {}
for fieldidds in idds:
    for fieldidd in fieldidds:
        if fieldidd.has_key('reference'):
            for aref in fieldidd['reference']:
                refs[aref.upper()] = None
        if fieldidd.has_key('object-list'):
            for oitem in fieldidd['object-list']:
                olist[oitem.upper()] = None
            # print fieldidd['reference']
# 
# for key in refs.keys():
#     print key
# for key in olist.keys():
#     print key

refk = refs.keys()
olistk = olist.keys()
refk.sort()
olistk.sort()
for item in olistk:
    if not refs.has_key(item):
        pass
        # print item
for item in refk:
    if not olist.has_key(item):
        pass
        # print item

# check for references that are not Name fields
# it did not print anything. So all references are in field Name
for fieldidds in idds:
    for fieldidd in fieldidds:
        if fieldidd.has_key('reference'):
            if fieldidd.has_key('field'):
                if not fieldidd['field'][0].endswith('Name'):
                    print fieldidd

#         