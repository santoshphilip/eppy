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

"""py.test for class IDF0"""

from modeleditor import IDF0

def test_IDF0():
    """py.test for class IDF0"""
    assert IDF0.iddname == None
    IDF0.setiddname("gumby")
    assert IDF0.iddname == "gumby"
    IDF0.setiddname("karamba")
    assert IDF0.iddname != "karamba"
    assert IDF0.iddname == "gumby"
