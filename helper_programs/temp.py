# Copyright (c) 2012 Santosh Phillip

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

"""get a variable from the sql table and teal with getting the right dates correctly"""
import eplussql
fname = './eplussql_test/eplussql.sql'
cursor = eplussql.getcursor(fname)

input -> cursor, ReportVariableDataDictionaryIndex

sql = "SELECT EnvironmentPeriodIndex FROM EnvironmentPeriods WHERE EnvironmentType = 3"
cursor.execute(sql)
rows = [row for row in cursor]
EnvironmentPeriodIndex = rows[0][0]

sql = "SELECT TimeIndex, Month, Day, Hour, Minute FROM Time WHERE EnvironmentPeriodIndex = 3"
cursor.execute(sql)
rows = [row for row in cursor]
# find year from day in a date. ???
starttimeindex = rows[0][0]
endtimeindex = rows[-1][0]

ReportVariableDataDictionaryIndex = 6
sql = "SELECT rowid, VariableValue FROM ReportVariableData WHERE (TimeIndex BETWEEN %s and %s) and ReportVariableDataDictionaryIndex = 6" % (starttimeindex, endtimeindex)
cursor.execute(sql)
rows = [row for row in cursor]

