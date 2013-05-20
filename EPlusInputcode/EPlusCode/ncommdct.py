# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""commdct in the original EPlusinterface is not working correctly.
This is a a hack to get the correct comdct
Call the function: getcommdct"""


from EPlusInterfaceFunctions import readidf
from EPlusInterfaceFunctions import eplusdata

def getobjnamelist(txt):
    """get the list of object names from the text of the idd file"""
    txtc = eplusdata.removecomment(txt, '!')
    txtsc = eplusdata.removecomment(txtc, '\\')
    lines = txtsc.splitlines()
    lines = [line.strip()  for line in lines]
    lines = [line for line in lines if line != '']
    txtsc = '\n'.join(lines)
    blocks = txtsc.split(';')
    blocks1 = [block.split(',') for block in blocks]
    names = [block[0].strip() for block in blocks1]
    names = [name.upper() for name in names if name != '']
    return names

def makecommdct(ablock, alist=False):
    """docstring for makecommdct"""
    # print ablock
    ablock1 = [line.strip().split('\\') for line in ablock]
    ablock2 = []
    for line in ablock1:
        if len(line) == 2:
            ablock2.append(line)
        else:
            variables = line[0].split(',')
            for v in variables:
                ablock2.append([v.strip(), ''])
    ablock2 = [item for item in ablock2 if ''.join(item) != '']   
    ablock2 = [[name.strip(), comm] for name, comm in ablock2]
    ablock2 = [[name.split(',')[0], comm] for name, comm in ablock2]
    # block2 is now
    # [['Report:Table:TimeBins', ''],
    #  ['', 'min-fields 5'],
    #  ['A1', 'field Key_Value'],
    #  ['', 'default *'],
    #  ['', "note use '*' (without quotes) to apply this variable to all keys"],
    # ['N1', ''], ['N2', '']]

    ablock3 = []
    nameorder = []
    for name, comm in ablock2:
        if name != '': 
            thename = name
            nameorder.append(name)
        ablock3.append([thename, comm])
    # block3 is now
    # [['Report:Table:TimeBins', ''],
    #  ['Report:Table:TimeBins', 'min-fields 5'],
    #  ['A1', 'field Key_Value'],
    #  ['A1', 'default *'],
    #  ['A1', "note use '*' (without quotes) to apply this variable to all keys"],
    # ['N1', ''], ['N2', '']]
    comms = dict([[name, []] for name in nameorder])
    for name, comm in ablock3:
        comms[name].append(comm)

    justcomms = []
    for name in nameorder:
        justcomms.append(comms[name])
    justcomms1 = []
    for acomm in justcomms:
        if alist:
            justcomms1.append(comm2lst(acomm))
        else:
            justcomms1.append(comm2dct(acomm))
    return justcomms1

def comm2lst(acomm):
    # acomm = [comm for comm in acomm if comm != '']
    # acomm = [comm.strip() for comm in acomm]
    # acomm = [comm for comm in acomm if comm.split()[0] != 'group']
    return acomm

def comm2dct(acomm):
    """
    make the comment into dct
        ['field IntervalCount',
         'type integer',
         'minimum 1',
         'maximum 20',
         'note The number of bins used. The number of hours below the start of the lowest bin and above the value of the last bin',
         'note are also shown.']
    becomes:
        {'field': ['IntervalCount'],
         'maximum': ['20'],
         'minimum': ['1'],
         'note': ['The number of bins used. The number of hours below the start of the lowest bin and above the value of the last bin',
                  'are also shown.'],
         'type': ['integer']}
    """
    acomm = [comm for comm in acomm if comm != '']
    acomm = [comm.strip() for comm in acomm]
    acomm = [comm for comm in acomm if comm.split()[0] != 'group']
    firstwords = [c.split()[0] for c in acomm]
    acommdct = dict([[word, []] for word in firstwords])
    for comm in acomm:
        firstword = comm.split()[0]
        rest = comm[len(firstword):]
        rest = rest.strip()
        acommdct[firstword].append(rest)
    return acommdct

def getobjlines(txtc):
    """return a list of (i, obj) = obj and the line on which it occurs in the idd file"""
    iobj = []
    lines = txtc.splitlines()
    s = 0
    objnamelist = getobjnamelist(txtc)
    for obj in objnamelist:
        for i in range(s,len(lines)):
            line = lines[i]
            line = line.strip()
            if line.split(',')[0].upper() == obj.upper():
                iobj.append((i, obj))
                break
            if line.split(';')[0].upper() == obj.upper():
                iobj.append((i, obj))
                break
        s = i 
    return iobj    

def getcommdct(txt):
    """get commdct
    txt is the text of the idd file"""
    txtc = eplusdata.removecomment(txt, '!')
    iobj = getobjlines(txtc)

    lines = txtc.splitlines()
    objblock =[]
    for k, (i, obj) in enumerate(iobj):
        try:
            theblock = lines[iobj[k][0]:iobj[k+1][0]]
            objblock.append(theblock)
        except IndexError, e:
            theblock = lines[iobj[k][0]:]
            objblock.append(theblock)

    ncommdct = []
    for ablock in objblock:
        ncommdct.append(makecommdct(ablock))
    return ncommdct


def getcommlst(txt):
    """get commlst
    txt is the text of the idd file"""
    txtc = eplusdata.removecomment(txt, '!')
    iobj = getobjlines(txtc)

    lines = txtc.splitlines()
    objblock =[]
    for k, (i, obj) in enumerate(iobj):
        try:
            theblock = lines[iobj[k][0]:iobj[k+1][0]]
            objblock.append(theblock)
        except IndexError, e:
            theblock = lines[iobj[k][0]:]
            objblock.append(theblock)

    ncommdct = []
    for ablock in objblock:
        ncommdct.append(makecommdct(ablock, alist=True))
        # for item in ablock:
        #     print item
        # print ablock
        # print makecommdct(ablock, alist=True)
    return ncommdct

# iddname = './EPlusInterfaceFunctions/Energy+.idd'
# txt = open(iddname, 'r').read()
# ncommdct = getcommdct(txt)





