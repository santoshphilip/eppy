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

"""py.test for class IDF"""

# if you have not done so, uncomment the following three lines


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


from io import StringIO
iddfhandle = StringIO(iddsnippet)

from eppy import modeleditor
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
        