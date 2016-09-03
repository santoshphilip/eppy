# Copyright (c) 2016 Santosh Philip
# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Find all related objects - skipping extensible fields

This script is to assist in further coding - not for end user use.
Will assist in:
    - discovering useful functions to add to EpBunch using addfunctions

Run as
  python relatedobjects.py <idd> > output.txt

"""

from collections import defaultdict
import sys

import argparse
from eppy.modeleditor import IDF
from six import StringIO


pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)


def print_related_objects(args):
    """Find and print all related objects - skipping extensible fields
    """
    IDF.setiddname(args.idd)
    idf = IDF(StringIO(""))
    
    # create a new object for each object type
    okeys = idf.idfobjects.keys()
    for okey in okeys:
        idf.newidfobject(okey)
    
    for okey in okeys:
        references = get_references(okey, idf)
        if not references:
            continue
        groupfield = get_groupfield(idf, references)
        print_references(okey, groupfield)


def get_references(okey, idf):
    """Get all references to an object based on the object type name.
    
    Parameters
    ----------
    okey : str
        The name of the object, e.g. "WALL:ADIABATIC".
    idf : object
        An eppy IDF object.
    
    Returns
    -------
    list
        List of object-lists, e.g. [u'MaterialNames', ...].
        
    """
    try:
        references = idf.idd_index['name2refs'][okey]
    except KeyError as e:
        return []
    return references


def get_groupfield(idf, references):
    # @TODO: Make this run faster
    groupfield = defaultdict(list)
    ikeys = idf.idfobjects.keys()
    for key in ikeys:
        objs = idf.idfobjects[key]
        try:
            obj = objs[0]
        except IndexError:
            continue
        keyidd = obj.getfieldidd('key')
        group = keyidd['group']

        fields = obj.objls
        for field in fields:
            fieldidd = obj.getfieldidd(field)
            try:
                referrings = fieldidd[u'object-list']
            except KeyError as e:
                referrings = []
            if 'begin-extensible' in fieldidd:
                break # do extensibles later
            s_references = set(references)
            s_referrings = set(referrings)

            intersect = s_references.intersection(s_referrings)
            if intersect:
                akey = (group, field)
                groupfield[akey].append(key)
    return groupfield


def print_references(okey, groupfield):
    for kkey, values in groupfield.items():
        print(okey)
        print('\t -> %s' % ''.join(kkey))
        for value in values:
            print('\t\t %s' % value)
        print


def main():
    parser = argparse.ArgumentParser(usage=None, 
                description=__doc__, 
                formatter_class=argparse.RawTextHelpFormatter)
                # need the formatter to print newline from __doc__
    parser.add_argument('idd', type=str, action='store', 
        help='location of idd file = ./somewhere/eplusv8-0-1.idd')
    
    args = parser.parse_args()
    print_related_objects(args)
    
            
if __name__ == "__main__":
    sys.exit(main())
