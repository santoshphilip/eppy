import eplussql
fname = './eplussql_test/eplussql1.sql'
fname = '/Volumes/Server/Staff/Santosh/transfer/eplussql_stuff/eplussql1.sql'
cursor = eplussql.getcursor(fname)

ReportVariableDataDictionaryIndex = 8

rows = eplussql.get_variables1(cursor, ReportVariableDataDictionaryIndex)

print rows[:150]