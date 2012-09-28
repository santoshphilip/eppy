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
        
