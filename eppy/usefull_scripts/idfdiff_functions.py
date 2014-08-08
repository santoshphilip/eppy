"""functions to find the diff between two idf files"""

def find_duplicates(lst):
    """find the duplicates in the list"""
    return set([x for x in lst if lst.count(x) > 1])
