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


import StringIO
import sys

import argparse
from eppy.modeleditor import IDF


pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)


def print_related_objects(args):
    """Find all related objects - skipping extensible fields
    """
    # @TODO Make this run faster using the new IDD index capability
    IDF.setiddname(args.idd)
    idf = IDF(StringIO.StringIO(""))
    
    okeys = idf.idfobjects.keys()
    for okey in okeys:
        idf.newidfobject(okey)
        
    for okey in okeys:
        referreds = idf.idfobjects[okey.upper()]    
        referred = referreds[0]
        try:
            nameidd = referred.getfieldidd('Name')
        except ValueError as e:
            continue
        try:
            references = nameidd['reference']
        except KeyError as e:
            continue
    
        groupfield = {}
        ikeys = idf.idfobjects.keys()
        for key in ikeys:
            objs = idf.idfobjects[key]
            obj = objs[0]
            keyidd = obj.getfieldidd('key')
            group = keyidd['group']
    
            fields = obj.objls
            for field in fields:
                fieldidd = obj.getfieldidd(field)
                try:
                    referrings = fieldidd[u'object-list']
                except KeyError as e:
                    referrings = []
                if fieldidd.has_key('begin-extensible'):
                    break # do extensibles later
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
    
        for kkey, values in groupfield.items():
            print(okey)
            print('\t', '->', kkey)
            for value in values:
                print('\t\t', value)
            print


def main():
    parser = argparse.ArgumentParser(usage=None, 
                description=__doc__, 
                formatter_class=argparse.RawTextHelpFormatter)
                # need the formatter to print newline from __doc__
    parser.add_argument('idd', type=str, action='store', 
        help='location of idd file = ./somewhere/eplusv8-0-1.idd')
    parser.add_argument('output', type=str, action='store', 
        help='location of output file = ./somewhere/output.txt')
    
    args = parser.parse_args()
    print_related_objects(args)
    
            
if __name__ == "__main__":
    sys.exit(main())
