# Copyright (c) 2012 Santosh Philip

"""py.test for class IDF"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals



from eppy.modeleditor import IDF0

def test_IDF0():
    """py.test for class IDF0"""
    assert IDF0.iddname == None
    IDF0.setiddname("gumby", testing=True)
    assert IDF0.iddname == "gumby"
    IDF0.setiddname("karamba", testing=True)
    assert IDF0.iddname != "karamba"
    assert IDF0.iddname == "gumby"


# import eppy.snippet as snippet


from eppy.iddcurrent import iddcurrent
iddsnippet = iddcurrent.iddtxt


from StringIO import StringIO
iddfhandle = StringIO(iddsnippet)

from eppy.modeleditor import IDF

if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

class TestIDF(object):
    """py.test for IDF function"""
    def test_removeidfobject(self):
        """py.test for IDF.removeidfobject """
        idftxt = ""
        idfhandle = StringIO(idftxt)
        idf = IDF(idfhandle)
        key = "BUILDING"
        idf.newidfobject(key, Name="Building_remove")
        idf.newidfobject(key, Name="Building1")
        idf.newidfobject(key, Name="Building_remove")
        idf.newidfobject(key, Name="Building2")
        buildings = idf.idfobjects["building".upper()]
        removethis = buildings[-2]
        idf.removeidfobject(removethis)
        assert buildings[2].Name == "Building2"
        assert idf.model.dt[key][2][1] == "Building2"

    def test_popidfobject(self):
        idftxt = ""
        idfhandle = StringIO(idftxt)
        idf = IDF(idfhandle)
        key = "BUILDING"
        idf.newidfobject(key, Name="Building_remove")
        idf.newidfobject(key, Name="Building1")
        idf.newidfobject(key, Name="Building_remove")
        idf.newidfobject(key, Name="Building2")
        buildings = idf.idfobjects["building".upper()]
        removethis = buildings[-2]
        idf.popidfobject(key, 2)
        assert buildings[2].Name == "Building2"
        assert idf.model.dt[key][2][1] == "Building2"
        