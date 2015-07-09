# Copyright (c) 2012 Santosh Philip

"""pytest for idfreader. very few tests"""






import eppy.idfreader as idfreader
from io import StringIO

def test_iddversiontuple():
    """py.test for iddversiontuple"""
    iddtxt = """stuff 9.8.4
    other stuff"""
    fhandle = StringIO(iddtxt)
    result = idfreader.iddversiontuple(fhandle)
    assert result == (9, 8, 4)
