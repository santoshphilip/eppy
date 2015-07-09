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

"""pytest for idfreader. very few tests"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.idfreader as idfreader
from StringIO import StringIO

def test_iddversiontuple():
    """py.test for iddversiontuple"""
    iddtxt = """stuff 9.8.4
    other stuff"""
    fhandle = StringIO(iddtxt)
    result = idfreader.iddversiontuple(fhandle)
    assert result == (9, 8, 4)
