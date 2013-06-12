# Copyright (c) 2012 Santosh Philip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""py.test for above_functions"""
import above_functions


def test_getabovedays():
    """py.test getabovedays"""
    data = (('./eplussql_test/hup01_23_pytest.sql',
        386, 88, ['2001-9-12'] * 24), # fname, varindex, aboveval, date
    )
    for fname, varindex, aboveval, date in data:
        varname, keyvalue, varunit, daysabove = above_functions.getabovedays(fname, varindex, aboveval, convertc2f=True)
        print daysabove
        result = [dt.split()[0] for dt, val in daysabove]
        assert result == date
        
