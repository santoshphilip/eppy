# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for relatedobjects.py"""

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from six import StringIO

from eppy.useful_scripts.relatedobjects import get_groupfield
from eppy.useful_scripts.relatedobjects import get_references


iddfhandle = StringIO(iddcurrent.iddtxt)


def test_get_groupfield():
    if IDF.getiddname() == None:
        IDF.setiddname(iddfhandle)
    idf = IDF(StringIO(""))
    # object has a reference but no groupfield
    okey = 'AVAILABILITYMANAGERASSIGNMENTLIST'
    idf.newidfobject(okey)
    references = [u'SystemAvailabilityManagerLists']
    groupfield = get_groupfield(idf, references)
    assert groupfield == {}

    # object has a reference and a groupfield
    okey = 'ZONEHVAC:OUTDOORAIRUNIT'
    idf.newidfobject(okey)
    references = [u'SystemAvailabilityManagerLists']
    groupfield = get_groupfield(idf, references)
    assert groupfield == {
        (u'Zone HVAC Forced Air Units', u'Availability_Manager_List_Name'):
            [u'ZONEHVAC:OUTDOORAIRUNIT']}


def test_get_references():
    if IDF.getiddname() == None:
        IDF.setiddname(iddfhandle)
    idf = IDF(StringIO(""))
    # object has a reference
    okey = 'AVAILABILITYMANAGERASSIGNMENTLIST'
    idf.newidfobject(okey)
    references = get_references(okey, idf)
    expected = [u'SystemAvailabilityManagerLists']
    assert references == expected
    
    # object has no references
    okey = 'PIPE:UNDERGROUND'
    idf.newidfobject(okey)
    references = get_references(okey, idf)
    expected = []
    assert references == expected


