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

"""pytest for iddgaps.py"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.iddgaps as iddgaps

def test_cleaniddfield():
    """pytest for cleaniddfield"""
    data = (({'field': ['Water Supply Storage Tank Name'],
          'Field': ['Water Supply Storage Tank Name'],
      'object-list': ['WaterStorageTankNames'],
      'type': ['object-list']},
     {'field': ['Water Supply Storage Tank Name'],
      'object-list': ['WaterStorageTankNames'],
      'type': ['object-list']}), #field, newfield
    )
    for field, newfield in data:
        result = iddgaps.cleaniddfield(field)
        assert result == newfield
