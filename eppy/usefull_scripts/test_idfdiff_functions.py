"""py.test for idfdiff_functions"""

import idfdiff_functions

def test_find_duplicates():
    """py.test for find_duplicates"""
    data = (([1, 2, 3, 1, 2], set([1, 2])), # lst, dups
    )
    for lst, dups in data:
        result = idfdiff_functions.find_duplicates(lst)
        assert result == dups