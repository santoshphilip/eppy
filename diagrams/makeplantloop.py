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

"""make plant loop"""

# build the following
# supplyinlet -> branchname0
# branchname0 -> splitter -> [branchname1, branchname2, branchname3]
# [branchname1, branchname2, branchname3] -> mixer -> branchname4
# branchname4 -> supplyoutlet


# supplyinlet -> branchname0 
# need code to build a new object.
# it should be in orig EPlusInterface
# need to find it. Althoough I dont thik it deals with extensible
# orig does not have an add node.
def newobj(objkey, objname):
    """docstring for newnode"""
    pass

# branchname0 -> splitter -> [branchname1, branchname2, branchname3]
# [branchname1, branchname2, branchname3] -> mixer -> branchname4
# branchname4 -> supplyoutlet
