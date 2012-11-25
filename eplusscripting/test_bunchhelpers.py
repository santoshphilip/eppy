"""pytest for bunchhelpers"""

import bunchhelpers

def test_makefieldname():
    """py.test for makefieldname"""
    data = (('aname', 'aname'), # namefromidd, bunchname
        ('a name', 'a_name'), # namefromidd, bunchname
        ('a name #1', 'a_name_1'), # namefromidd, bunchname
    )
    for namefromidd, bunchname in data:
        result = bunchhelpers.makefieldname(namefromidd)
        assert result == bunchname

