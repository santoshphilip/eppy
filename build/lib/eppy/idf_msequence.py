"""subclass from collections.MutableSequence to get finer ontrol over a list like object.

this is to work with issue 40 in github:

idf1.idfobjects['BUILDING'] is a list and is not connected to idf1.model.dt['BUILDING']
list has to be subclassed to solve this problem
"""

# Alex Martelli describes how to use collections.MutableSequence in
# <http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>
# Here I recreate and test his example

import collections

class TypedList(collections.MutableSequence):
    """This is Alex Martelli example from
    http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list

    Not used by eppy"""
    def __init__(self, oktypes, *args):
        self.oktypes = oktypes
        self.list = list()
        self.extend(list(args))
    def check(self, val):
        if not isinstance(val, self.oktypes):
            raise TypeError(val)
    def __len__(self):
        return len(self.list)
    def __getitem__(self, i):
        return self.list[i]
    def __delitem__(self, i):
        del self.list[i]
    def __setitem__(self, i, v):
        self.check(v)
        self.list[i] = v
    def insert(self, i, v):
        self.check(v)
        self.list.insert(i, v)
    def __str__(self):
        return str(self.list)

class TwoLists(collections.MutableSequence):
    """Used to learn. Not used by eppy"""
    def __init__(self, *args):
        super(TwoLists, self).__init__()
        self.list1 = list()
        self.list2 = list()
    def newval(self, val):
        return "r_%s" % (val, )
    def __getitem__(self, i):
        return self.list1[i]
    def __setitem__(self, i, v):
        self.list1[i] = v
        self.list2[i] = self.newval(v)
    def __delitem__(self, i):
        del self.list1[i]
        del self.list2[i]
    def __len__(self):
        return len(self.list1)
    def insert(self, i, v):
        self.list1.insert(i, v)
        self.list2.insert(i, self.newval(v))
    def __str__(self):
        astr = "list1 = %s, list2 = %s" % (self.list1, self.list2)
        return astr

class Idf_MSequence_old(collections.MutableSequence):
    def __init__(self, *args):
        super(Idf_MSequence_old, self).__init__()
        self.list1 = list()
        self.list2 = list() # this list has a different id from
                            # idf.model.dt[objtype]. This is a bug
    def __getitem__(self, i):
        return self.list1[i]
    def __setitem__(self, i, v):
        self.list1[i] = v
        self.list2[i] = v.obj
    def __delitem__(self, i):
        # print 'removing list1 %s' % (self.list1[i], )
        del self.list1[i]
        # print 'list2 ids = %s' % ([id(item) for item in self.list2], )
        # print 'removing list2 %s' % (self.list2[i], )
        del self.list2[i]
        # print "list1 %s" % (self.list1, )
        # print "list2 %s" % (self.list2, )
    def __len__(self):
        return len(self.list1)
    def insert(self, i, v):
        self.list1.insert(i, v)
        self.list2.insert(i, v.obj)
    def __str__(self):
        # st = "list1 = %s, list2 = %s" % (self.list1, self.list2)
        return str(self.list1)
    def __repr__(self):
        return str(self.list1)
    def __eq__(self, other):
        return self.list2 == other.list2

class Idf_MSequence(collections.MutableSequence):
    def __init__(self, list1, list2):
        super(Idf_MSequence, self).__init__()
        self.list1 = list1
        self.list2 = list2
    def __getitem__(self, i):
        return self.list1[i]
    def __setitem__(self, i, v):
        self.list1[i] = v
        self.list2[i] = v.obj
        # print "in __setitem__"
    def __delitem__(self, i):
        del self.list1[i]
        del self.list2[i]
    def __len__(self):
        return len(self.list1)
    def insert(self, i, v):
        # print len(self.list1), len(self.list2)
        self.list1.insert(i, v)
        self.list2.insert(i, v.obj)
        # print len(self.list1), len(self.list2)
        # print "in insert"
    def __str__(self):
        # st = "list1 = %s, list2 = %s" % (self.list1, self.list2)
        return str(self.list1)
    def __repr__(self):
        return str(self.list1)
    def __eq__(self, other):
        return self.list2 == other.list2

class FakeEpBunch(object):
    """use this to unit test Idf_MSequence_old"""
    def __init__(self, arg):
        super(FakeEpBunch, self).__init__()
        self.Name = arg
        self.obj = [arg, self.newval(arg)]
    def newval(self, val):
        return "r_%s" % (val, )
    def __str__(self):
        astr = "Name = %s, obj = %s" % (self.Name, self.obj)
        return astr



# import sys
# # pathnameto_eppy = 'c:/eppy'
# pathnameto_eppy = '../'
# sys.path.append(pathnameto_eppy)
#
# from eppy import modeleditor
# from eppy.modeleditor import IDF
# from eppy import bunchhelpers
# from bunch_subclass import EpBunch
#
#
# def makeabunch(commdct, obj, obj_i):
#     """make a bunch from the object"""
#     objidd = commdct[obj_i]
#     objfields = [comm.get('field') for comm in commdct[obj_i]]
#     objfields[0] = ['key']
#     objfields = [field[0] for field in objfields]
#     obj_fields = [bunchhelpers.makefieldname(field) for field in objfields]
#     bobj = EpBunch(obj, obj_fields, objidd)
#     return bobj
#
#
# iddfile = "./resources/iddfiles/Energy+V7_2_0.idd"
# IDF.setiddname(iddfile)
#
# idftxt = "" # empty string
# from StringIO import StringIO
# fhandle = StringIO(idftxt) # we can make a file handle of a string
# idf = IDF(fhandle) # initialize the IDF object with the file handle
#
#
# commdct = idf.idd_info
# obj_i = idf.model.dtls.index("BUILDING")
#
# idfobjects = IdfObjects()   # use IdfObjects here. Initialize with dt[key]
#                     # IdfObjects will have two parallel lists (list1 and list2)
#                     # append will add to both lists
#                     # pop or delete will remove from both lists
#                     # list2 is not directly accesed
#                     # only thru IdfObjects
#
#
# # add an object to the idf file
# objtype = "BUILDING"
# bobj = idf.newidfobject(objtype, Name="Taj Mahal")
# obj = bobj.obj
#
# bobj = makeabunch(commdct, obj, obj_i)
# idfobjects.append(bobj)
#
# print idfobjects.list2
# print '-' * 8
#
# # add an object to the idf file
# objtype = "BUILDING"
# bobj = idf.newidfobject(objtype, Name="Qoit tower")
# obj = bobj.obj
#
# bobj = makeabunch(commdct, obj, obj_i)
# idfobjects.append(bobj)
#
# print idfobjects.list2
# print '-' * 8
#
# idfobjects.remove(bobj)
#
# print idfobjects.list2
# print '-' * 8
#
# print idfobjects
#
# # idfobjects.pop(0)
# #
# # print idfobjects.list2
# # print '-' * 8
# #
# # idfobjects[0].Name = 'karamba'
# #
# # print idfobjects.list2
# # print '-' * 8
# #
