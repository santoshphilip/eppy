"""
Subclass from collections.MutableSequence to get finer control over a list-like
object.

This is to work with issue 40 in github:

idf1.idfobjects['BUILDING'] is a list and is not connected to 
idf1.model.dt['BUILDING']
List has to be subclassed to solve this problem.

"""
# Alex Martelli describes how to use collections.MutableSequence in
# <http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>
# Here I recreate and test his example

import collections

from eppy.bunch_subclass import EpBunch


class Idf_MSequence(collections.MutableSequence):

    def __init__(self, list1, list2, theidf):
        super(Idf_MSequence, self).__init__()
        self.list1 = list1
        self.list2 = list2
        self.theidf = theidf
        for v in self.list1:
            if isinstance(v, EpBunch):
                v.theidf = self.theidf            

    def __getitem__(self, i):
        return self.list1[i]
    
    def __setitem__(self, i, v):
        self.list1[i] = v
        self.list2[i] = v.obj

    def __delitem__(self, i):
        v = self.list1[i]
        if isinstance(v, EpBunch):
            v.theidf = None
        del self.list1[i]
        del self.list2[i]

    def __len__(self):
        return len(self.list1)
    
    def insert(self, i, v):
        self.list1.insert(i, v)
        self.list2.insert(i, v.obj)
        if isinstance(v, EpBunch):
            v.theidf = self.theidf

    def __str__(self):
        return str(self.list1)
    
    def __repr__(self):
        return str(self.list1)
    
    def __eq__(self, other):
        return self.list2 == other.list2
    
