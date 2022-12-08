# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for class IDF"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import StringIO

from eppy.modeleditor import IDF

# Not sure why these tests are sitting in this file
# Should it not be in test_modeleditor.py or test_modeleditor1.py

def setup_module(module):
    """
    idd is read only once in this module
    if it has already been read from some other module, it will continue 
    without reading it again
    
    pytest run this before running the module
    """
    from eppy.iddcurrent import iddcurrent
    iddfhandle = StringIO(iddcurrent.iddtxt)
    if IDF.getiddname() == None:
        IDF.setiddname(iddfhandle)

def test_IDF():
    """py.test for class IDF"""
    stored_idd = IDF.iddname
    IDF.iddname = None
    assert IDF.iddname == None
    IDF.setiddname("gumby", testing=True)
    assert IDF.iddname == "gumby"
    IDF.setiddname("karamba", testing=True)
    assert IDF.iddname != "karamba"
    assert IDF.iddname == "gumby"
    IDF.iddname = stored_idd




class TestIDF(object):

    """py.test for IDF function"""

    def test_removeidfobject(self):
        """py.test for IDF.removeidfobject"""
        idftxt = ""
        idfhandle = StringIO(idftxt)
        idf = IDF(idfhandle)
        key = "BUILDING"
        idf.newidfobject(key, Name="Building_remove")
        idf.newidfobject(key, Name="Building1")
        idf.newidfobject(key, Name="Building_remove")
        idf.newidfobject(key, Name="Building2")
        buildings = idf.idfobjects["building"]
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
        buildings = idf.idfobjects["building"]
        removethis = buildings[-2]
        idf.popidfobject(key, 2)
        assert buildings[2].Name == "Building2"
        assert idf.model.dt[key][2][1] == "Building2"
