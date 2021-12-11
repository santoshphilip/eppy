"""
Subclass from collections.MutableSequence to get finer control over a list like
object.

This is to work with issue 40 in github:

idf1.idfobjects['BUILDING'] is a list and is not connected to
idf1.model.dt['BUILDING']

List has to be subclassed to solve this problem.

# Alex Martelli describes how to use collections.MutableSequence in
# <http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import collections

from eppy.bunch_subclass import EpBunch


class Idf_MSequence(collections.abc.MutableSequence):
    """Used to keep IDF.idfobjects in sync with IDF.model.dt."""

    def __init__(self, list1, list2, theidf):
        """Initialise the object.

        Parameters
        ----------
        list1 : list
            Bunches (IDF.idfobjects).
        list2 : list
            Objects (IDF.model.dt).
        theidf : modeleditor.IDF
            The IDF.

        """
        super(Idf_MSequence, self).__init__()
        self.list1 = list1
        self.list2 = list2
        self.theidf = theidf
        for v in self.list1:
            if isinstance(v, EpBunch):
                v.theidf = self.theidf

    def __getitem__(self, i):
        """Gets an idfobject (bunch) from list1."""
        return self.list1[i]

    def __setitem__(self, i, v):
        """Sets an idfobject (bunch) to list1 and its object to list2."""
        self.list1[i] = v
        self.list2[i] = v.obj

    def __delitem__(self, i):
        """Deletes an idfobject (bunch) from list1 and its object from list2."""
        v = self.list1[i]
        if isinstance(v, EpBunch):
            v.theidf = None
        del self.list1[i]
        del self.list2[i]

    def __len__(self):
        """Number of idfobjects (bunches)."""
        return len(self.list1)

    def insert(self, i, v):
        """Insert an idfobject (bunch) to list1 and its object to list2."""
        self.list1.insert(i, v)
        self.list2.insert(i, v.obj)
        if isinstance(v, EpBunch):
            v.theidf = self.theidf

    def __str__(self):
        """String representation of the list of idfobjects (bunches)."""
        return str(self.list1)

    def __repr__(self):
        """Repr representation of the list of idfobjects (bunches)."""
        return str(self.list1)

    def __eq__(self, other):
        """Test for equality uses the IDF.model.dt list, list2."""
        return self.list2 == other.list2
