"""find all related objects - skiping extensible fields
this script is to assist in further coding - not for end user
Will assist in:
    - discovering useful functions to add to EpBunch using addfunctions
"""
# was designed to run from ../../docs
# to run from here change some of the file paths below
# run as
# python relatedbojects.py > outputfile.txt
# look at outputfile.txt
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys

# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = "../"
sys.path.append(pathnameto_eppy)

from eppy import modeleditor
from eppy.modeleditor import IDF
import StringIO

iddfile = "./eppy/resources/iddfiles/Energy+V7_2_0.idd"
iddfile = "./eppy/resources/iddfiles/Energy+V8_0_0.idd"

IDF.setiddname(iddfile)
idf = IDF(StringIO.StringIO(""))

okeys = idf.idfobjects.keys()
for okey in okeys:
    idf.newidfobject(okey)

for okey in okeys:
    referreds = idf.idfobjects[okey.upper()]
    referred = referreds[0]
    try:
        nameidd = referred.getfieldidd("Name")
    except ValueError as e:
        # print 'no Name', okey
        continue
    try:
        references = nameidd["reference"]
    except KeyError as e:
        # print 'no reference', okey
        continue

    groupfield = {}
    ikeys = idf.idfobjects.keys()
    for key in ikeys:
        # key = u'BUILDINGSURFACE:DETAILED'
        # key = u'ZONELIST'
        objs = idf.idfobjects[key]
        obj = objs[0]
        keyidd = obj.getfieldidd("key")
        group = keyidd["group"]

        fields = obj.objls
        for field in fields:
            # field = u'Zone_1_Name'
            fieldidd = obj.getfieldidd(field)
            try:
                referrings = fieldidd["object-list"]
            except KeyError as e:
                referrings = []
            if fieldidd.has_key("begin-extensible"):
                # print field, fieldidd['begin-extensible']
                break  # do extensibles later
            s_references = set(references)
            s_referrings = set(referrings)

            intersect = s_references.intersection(s_referrings)
            if intersect:
                akey = (group, field)
                if not groupfield.has_key(akey):
                    groupfield[akey] = []
                    groupfield[akey].append(key)
                else:
                    groupfield[akey].append(key)
                # print obj.key
                # print '\t', dict(group=group, field=field)
                # print

    for kkey, values in groupfield.items():
        print(okey)
        print("\t", "->", kkey)
        for value in values:
            print("\t\t", value)
        print
