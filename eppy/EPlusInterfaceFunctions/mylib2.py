# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""leagacy code from EPlusInterface"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os, pickle

# import string
import eppy.EPlusInterfaceFunctions.mylib1 as mylib1


RET = "\r\n"


def readfile(filename):
    """readfile"""
    fhandle = open(filename, "rb")
    data = fhandle.read()
    try:
        data = data.decode("ISO-8859-2")
    except AttributeError:
        pass
    fhandle.close()
    return data


def printlist(alist):
    """printlist"""
    for num in range(0, len(alist)):
        print(alist[num])


def printdict(adict):
    """printdict"""
    dlist = list(adict.keys())
    dlist.sort()
    for i in range(0, len(dlist)):
        print(dlist[i], adict[dlist[i]])


def tabfile2list(fname):
    "tabfile2list"
    # dat = mylib1.readfileasmac(fname)
    # data = string.strip(dat)
    data = mylib1.readfileasmac(fname)
    # data = data[:-2]#remove the last return
    alist = data.split("\r")  # since I read it as a mac file
    blist = alist[1].split("\t")

    clist = []
    for num in range(0, len(alist)):
        ilist = alist[num].split("\t")
        clist = clist + [ilist]
    cclist = clist[:-1]  # the last element is turning out to be empty
    return cclist


def tabstr2list(data):
    """tabstr2list"""
    alist = data.split(os.linesep)
    blist = alist[1].split("\t")

    clist = []
    for num in range(0, len(alist)):
        ilist = alist[num].split("\t")
        clist = clist + [ilist]
    cclist = clist[:-1]
    # the last element is turning out to be empty
    # this is because the string ends with a os.linesep
    return cclist


def list2doe(alist):
    """list2doe"""
    theequal = ""
    astr = ""
    lenj = len(alist)
    leni = len(alist[0])
    for i in range(0, leni - 1):
        for j in range(0, lenj):
            if j == 0:
                astr = astr + alist[j][i + 1] + theequal + alist[j][0] + RET
            else:
                astr = astr + alist[j][0] + theequal + alist[j][i + 1] + RET
        astr = astr + RET
    return astr


def tabfile2doefile(tabfile, doefile):
    """tabfile2doefile"""
    alist = tabfile2list(tabfile)
    astr = list2doe(alist)
    mylib1.write_str2file(doefile, astr)


def tabstr2doestr(astr):
    """tabstr2doestr"""
    alist = tabstr2list(astr)
    astr = list2doe(alist)
    return astr


def makedoedict(str1):
    """makedoedict"""
    blocklist = str1.split("..")
    blocklist = blocklist[:-1]  # remove empty item after last '..'
    blockdict = {}
    belongsdict = {}
    for num in range(0, len(blocklist)):
        blocklist[num] = blocklist[num].strip()
        linelist = blocklist[num].split(os.linesep)
        aline = linelist[0]
        alinelist = aline.split("=")
        name = alinelist[0].strip()
        aline = linelist[1]
        alinelist = aline.split("=")
        belongs = alinelist[-1].strip()
        theblock = blocklist[num] + os.linesep + ".." + os.linesep + os.linesep
        # put the '..' back in the block
        blockdict[name] = theblock
        belongsdict[name] = belongs
    return [blockdict, belongsdict]


def makedoetree(ddict, bdict):
    """makedoetree"""
    dlist = list(ddict.keys())
    blist = list(bdict.keys())
    dlist.sort()
    blist.sort()
    # make space dict
    doesnot = "DOES NOT"
    lst = []
    for num in range(0, len(blist)):
        if bdict[blist[num]] == doesnot:  # belong
            lst = lst + [blist[num]]

    doedict = {}
    for num in range(0, len(lst)):
        # print lst[num]
        doedict[lst[num]] = {}
    lv1list = list(doedict.keys())
    lv1list.sort()

    # make wall dict
    # for each space
    for i in range(0, len(lv1list)):
        walllist = []
        adict = doedict[lv1list[i]]
        # loop thru the entire blist dictonary and list the ones that belong into walllist
        for num in range(0, len(blist)):
            if bdict[blist[num]] == lv1list[i]:
                walllist = walllist + [blist[num]]
        # put walllist into dict
        for j in range(0, len(walllist)):
            adict[walllist[j]] = {}

    # make window dict
    # for each space
    for i in range(0, len(lv1list)):
        adict1 = doedict[lv1list[i]]
        # for each wall
        walllist = list(adict1.keys())
        walllist.sort()
        for j in range(0, len(walllist)):
            windlist = []
            adict2 = adict1[walllist[j]]
            # loop thru the entire blist dictonary and list the ones that belong into windlist
            for num in range(0, len(blist)):
                if bdict[blist[num]] == walllist[j]:
                    windlist = windlist + [blist[num]]
            # put walllist into dict
            for k in range(0, len(windlist)):
                adict2[windlist[k]] = {}
    return doedict


def tree2doe(str1):
    """tree2doe"""
    retstuff = makedoedict(str1)
    ddict = makedoetree(retstuff[0], retstuff[1])
    ddict = retstuff[0]
    retstuff[1] = {}  # don't need it anymore

    str1 = ""  # just re-using it
    l1list = list(ddict.keys())
    l1list.sort()
    for i in range(0, len(l1list)):
        str1 = str1 + ddict[l1list[i]]
        l2list = list(ddict[l1list[i]].keys())
        l2list.sort()
        for j in range(0, len(l2list)):
            str1 = str1 + ddict[l2list[j]]
            l3list = list(ddict[l1list[i]][l2list[j]].keys())
            l3list.sort()
            for k in range(0, len(l3list)):
                str1 = str1 + ddict[l3list[k]]
    return str1


def mtabstr2doestr(st1):
    """mtabstr2doestr"""
    seperator = "$ =============="
    alist = st1.split(seperator)

    # this removes all the tabs that excel
    # puts after the seperator and before the next line
    for num in range(0, len(alist)):
        alist[num] = alist[num].lstrip()
    st2 = ""
    for num in range(0, len(alist)):
        alist = tabstr2list(alist[num])
        st2 = st2 + list2doe(alist)

    lss = st2.split("..")
    mylib1.write_str2file("forfinal.txt", st2)  # for debugging
    print(len(lss))

    st3 = tree2doe(st2)
    lsss = st3.split("..")
    print(len(lsss))
    return st3


def getoneblock(astr, start, end):
    """get the block bounded by start and end
    doesn't work for multiple blocks"""
    alist = astr.split(start)
    astr = alist[-1]
    alist = astr.split(end)
    astr = alist[0]
    return astr


def doestr2tabstr(astr, kword):
    """doestr2tabstr"""
    alist = astr.split("..")
    del astr
    # strip junk put .. back
    for num in range(0, len(alist)):
        alist[num] = alist[num].strip()
        alist[num] = alist[num] + os.linesep + ".." + os.linesep
    alist.pop()

    lblock = []
    for num in range(0, len(alist)):
        linels = alist[num].split(os.linesep)
        firstline = linels[0]
        assignls = firstline.split("=")
        keyword = assignls[-1].strip()
        if keyword == kword:
            lblock = lblock + [alist[num]]
            # print firstline

    # get all val
    lval = []
    for num in range(0, len(lblock)):
        block = lblock[num]
        linel = block.split(os.linesep)
        lvalin = []
        for k in range(0, len(linel)):
            line = linel[k]
            assignl = line.split("=")
            if k == 0:
                lvalin = lvalin + [assignl[0]]
            else:
                if assignl[-1] == "..":
                    assignl[-1] = "."
                lvalin = lvalin + [assignl[-1]]
        lvalin.pop()
        lval = lval + [lvalin]

    # get keywords
    kwordl = []
    block = lblock[0]
    linel = block.split(os.linesep)
    for k in range(0, len(linel)):
        line = linel[k]
        assignl = line.split("=")
        if k == 0:
            kword = " =  " + assignl[1].strip()
        else:
            if assignl[0] == "..":
                assignl[0] = "."
            else:
                assignl[0] = assignl[0] + "="
            kword = assignl[0].strip()
        kwordl = kwordl + [kword]
    kwordl.pop()

    astr = ""
    for num in range(0, len(kwordl)):
        linest = ""
        linest = linest + kwordl[num]
        for k in range(0, len(lval)):
            linest = linest + "\t" + lval[k][num]
        astr = astr + linest + os.linesep

    return astr


def myreplace(astr, thefind, thereplace):
    """in string astr replace all occurences of thefind with thereplace"""
    alist = astr.split(thefind)
    new_s = alist.split(thereplace)
    return new_s


def fslicebefore(astr, sub):
    """Return the slice starting at sub in string astr"""
    findex = astr.find(sub)
    return astr[findex:]


def fsliceafter(astr, sub):
    """Return the slice after at sub in string astr"""
    findex = astr.find(sub)
    return astr[findex + len(sub) :]


def pickleload(fname):
    """same as pickle.load(fhandle).takes filename as parameter"""
    fhandle = open(fname, "rb")
    return pickle.load(fhandle)


def pickledump(theobject, fname):
    """same as pickle.dump(theobject, fhandle).takes filename as parameter"""
    fhandle = open(fname, "wb")
    pickle.dump(theobject, fhandle)
