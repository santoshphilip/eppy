"""just stuff"""

def getnamedargs(*args, **kwargs):
    """allows you to pass a dict and named args
    so you can pass ({'a':5, 'b':3}, c=8) and get
    dict(a=5, b=3, c=8)"""
    adict = {}
    for arg in args:
        if isinstance(arg, dict):
            adict.update(arg)
    adict.update(kwargs)
    return adict
    
def test_getnamedargs():
    """py.test for getnamedargs"""
    result = dict(a=1, b=2, c=3)
    assert result == getnamedargs(a=1, b=2, c=3)
    assert result == getnamedargs(dict(a=1, b=2, c=3))
    assert result == getnamedargs(dict(a=1, b=2), c=3)
    assert result == getnamedargs(dict(a=1), c=3, b=2)
    
# printkeywords(Name='Santosh', Last='Philip')
# printkeywords(dict(Name='Santosh', Last='Philip'))