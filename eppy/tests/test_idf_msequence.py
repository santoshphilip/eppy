# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""pytest for idf_msequence.py"""

from eppy.idf_msequence import Idf_MSequence


def test_IDF_MSequence():
    l1 = ['a', 'b', 'c', 'd']
    l2 = ['1', '2', '3', '4']
    idfms =  Idf_MSequence(l1, l2, None)
    assert isinstance(idfms, Idf_MSequence)
    
    assert idfms[1] == 'b'

    class testV:
        def __init__(self):
            self.obj = 'anobj'
    
    myTestV = testV()
    idfms.insert(2, myTestV)
    assert idfms[2] == myTestV
    
    assert idfms.list1[2] == myTestV
    assert idfms.list2[2] == 'anobj'
    
    del idfms[2]
    assert idfms[2] is not myTestV
    assert idfms.__repr__() == "['a', 'b', 'c', 'd']"
    assert str(idfms) == "['a', 'b', 'c', 'd']"
    
    idfms[1] = myTestV
    assert idfms[1] == myTestV