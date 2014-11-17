# Copyright (c) 2014 Eric Youngson

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

"""This module is used to implement native Python functions to replace those called from numpy,
	when using eppy with Rhino"""
# Wrote by Tuan Tran trantuan@hawaii.edu / tranhuuanhtuan@gmail.com
# School of Architecture, University of Hawaii at Manoa

####### The following code within the block credited by ActiveState Code Recipes code.activestate.com
## {{{ http://code.activestate.com/recipes/578276/ (r1)