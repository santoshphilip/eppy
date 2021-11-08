"""Legacy code from EPlusInterface"""
# Copyright (C) 2004 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================


# this is a test version ... not for real use
# dammit i am using it
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import copy
from io import StringIO
from pathlib import Path

import eppy.EPlusInterfaceFunctions.mylib2 as mylib2


def removecomment(astr, cphrase):
    """
    the comment is similar to that in python.
    any charachter after the # is treated as a comment
    until the end of the line
    astr is the string to be de-commented
    cphrase is the comment phrase"""
    # linesep = mylib3.getlinesep(astr)
    alist = astr.splitlines()
    for i in range(len(alist)):
        alist1 = alist[i].split(cphrase)
        alist[i] = alist1[0]

    # return string.join(alist, linesep)
    return "\n".join(alist)


class Idd(object):

    """Idd object"""

    def __init__(self, dictfile, version=2):
        if version == 2:
            # version == 2. This is a just a flag I am using
            # it may wind up being the only type... then I can clean this up
            # and not use the other option
            self.dt, self.dtls = self.initdict2(dictfile)
            return
        self.dt, self.dtls = self.initdict(dictfile)

    def initdict2(self, dictfile):
        """initdict2"""
        dt = {}
        dtls = []
        adict = dictfile
        for element in adict:
            dt[element[0].upper()] = []  # dict keys for objects always in caps
            dtls.append(element[0].upper())
        return dt, dtls

    def initdict(self, fname):
        """initdict"""
        astr = mylib2.readfile(fname)
        nocom = removecomment(astr, "!")
        idfst = nocom
        alist = idfst.split(";")
        lss = []
        for element in alist:
            lst = element.split(",")
            lss.append(lst)

        for i in range(0, len(lss)):
            for j in range(0, len(lss[i])):
                lss[i][j] = lss[i][j].strip()

        dt = {}
        dtls = []
        for element in lss:
            if element[0] == "":
                continue
            dt[element[0].upper()] = []
            dtls.append(element[0].upper())

        return dt, dtls


class Eplusdata(object):

    """Eplusdata"""

    def __init__(self, dictfile=None, fname=None):
        # import pdb; pdb.set_trace()
        if fname == None and dictfile == None:
            self.dt, self.dtls = {}, []
        if isinstance(dictfile, (str, Path)) and fname == None:
            self.initdict(dictfile)
        if isinstance(dictfile, Idd) and fname == None:
            self.initdict(dictfile)
        if isinstance(fname, (str, Path)) and isinstance(dictfile, (str, Path)):
            fnamefobject = open(fname, "rb")
            self.makedict(dictfile, fnamefobject)
        if isinstance(fname, (str, Path)) and isinstance(dictfile, Idd):
            fnamefobject = open(fname, "rb")
            self.makedict(dictfile, fnamefobject)
        try:
            # will fail in python3 because of file
            if isinstance(fname, (file, StringIO)) and isinstance(dictfile, str):
                self.makedict(dictfile, fname)
            if isinstance(fname, (file, StringIO)) and isinstance(dictfile, Idd):
                self.makedict(dictfile, fname)
        except NameError:
            from io import IOBase

            if isinstance(fname, (IOBase, StringIO)) and isinstance(dictfile, str):
                self.makedict(dictfile, fname)
            if isinstance(fname, (IOBase, StringIO)) and isinstance(dictfile, Idd):
                self.makedict(dictfile, fname)

    def __repr__(self):
        # print dictionary
        dt = self.dt
        dtls = self.dtls
        UNIXSEP = "\n"
        DOSSEP = UNIXSEP  # using a unix EOL
        astr = ""
        for node in dtls:
            nodedata = dt[node.upper()]
            for block in nodedata:
                for i in range(len(block)):
                    fformat = "     %s," + DOSSEP
                    if i == 0:
                        fformat = "%s," + DOSSEP
                    if i == len(block) - 1:
                        fformat = "     %s;" + DOSSEP * 2
                    astr = astr + fformat % block[i]

        return astr

    # ------------------------------------------
    def initdict(self, fname):
        """create a blank dictionary"""
        if isinstance(fname, Idd):
            self.dt, self.dtls = fname.dt, fname.dtls
            return self.dt, self.dtls

        astr = mylib2.readfile(fname)
        nocom = removecomment(astr, "!")
        idfst = nocom
        alist = idfst.split(";")
        lss = []
        for element in alist:
            lst = element.split(",")
            lss.append(lst)

        for i in range(0, len(lss)):
            for j in range(0, len(lss[i])):
                lss[i][j] = lss[i][j].strip()

        dt = {}
        dtls = []
        for element in lss:
            if element[0] == "":
                continue
            dt[element[0].upper()] = []
            dtls.append(element[0].upper())

        self.dt, self.dtls = dt, dtls
        return dt, dtls

    # ------------------------------------------
    def makedict(self, dictfile, fnamefobject):
        """stuff file data into the blank dictionary"""
        # fname = './exapmlefiles/5ZoneDD.idf'
        # fname = './1ZoneUncontrolled.idf'
        if isinstance(dictfile, Idd):
            localidd = copy.deepcopy(dictfile)
            dt, dtls = localidd.dt, localidd.dtls
        else:
            dt, dtls = self.initdict(dictfile)
        # astr = mylib2.readfile(fname)
        astr = fnamefobject.read()
        try:
            astr = astr.decode("ISO-8859-2")
        except AttributeError:
            pass
        fnamefobject.close()
        nocom = removecomment(astr, "!")
        idfst = nocom
        # alist = string.split(idfst, ';')
        alist = idfst.split(";")
        lss = []
        for element in alist:
            # lst = string.split(element, ',')
            lst = element.split(",")
            lss.append(lst)

        for i in range(0, len(lss)):
            for j in range(0, len(lss[i])):
                lss[i][j] = lss[i][j].strip()

        for element in lss:
            node = element[0].upper()
            if node in dt:
                # stuff data in this key
                dt[node.upper()].append(element)
            else:
                # scream
                if node == "":
                    continue
                print("this node -%s-is not present in base dictionary" % (node))

        self.dt, self.dtls = dt, dtls
        return dt, dtls

    def replacenode(self, othereplus, node):
        """replace the node here with the node from othereplus"""
        node = node.upper()
        self.dt[node.upper()] = othereplus.dt[node.upper()]

    def add2node(self, othereplus, node):
        """add the node here with the node from othereplus
        this will potentially have duplicates"""
        node = node.upper()
        self.dt[node.upper()] = self.dt[node.upper()] + othereplus.dt[node.upper()]

    def addinnode(self, otherplus, node, objectname):
        """add an item to the node.
        example: add a new zone to the element 'ZONE'"""
        # do a test for unique object here
        newelement = otherplus.dt[node.upper()]

    def getrefs(self, reflist):
        """
        reflist is got from getobjectref in parse_idd.py
        getobjectref returns a dictionary.
        reflist is an item in the dictionary
        getrefs gathers all the fields refered by reflist
        """
        alist = []
        for element in reflist:
            if element[0].upper() in self.dt:
                for elm in self.dt[element[0].upper()]:
                    alist.append(elm[element[1]])
        return alist


# ------------------------------------------
