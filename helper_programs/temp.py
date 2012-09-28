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

