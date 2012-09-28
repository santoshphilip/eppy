#!/usr/local/bin/python

## EPlusInterface (EPI) - An interface for EnergyPlus
## Copyright (C) 2004 Santosh Philip
##
## This file is part of EPlusInterface.
## 
## EPlusInterface is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## EPlusInterface is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with EPlusInterface; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
##
##
## Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
## santosh_philip AT yahoo DOT com
## Please send all bug reports, enhancement proposals, questions and comments to that address.
## 
## VERSION: 0.005

"""scratch file for temporary functions and scripts"""

k = 1

def aplane(k):
    lst = []
    for i in range(4):
        lst1 = []
        for j in range(3):
            lst1.append(k)
            k += 1
        lst.append(lst1)
    return lst


def eplusplane(k):
    for i in range(12):
        if i == 11:
            print '    %s;' % (k + i, )
        else:
            print '    %s,' % (k + i, )
            
def txt2points(txt):
    """convert text of points fron sk2eplus7 to list of points"""            
    lst = [ln.strip().split() for ln in txt.splitlines()]
    return [[float(coord) for coord in p3d] for p3d in lst]

def etxtdct(fname='e.txt'):
    """get dct from a file"""
    import readsketchup
    txt = open(fname, 'r').read()
    return readsketchup.readsketchup(txt)

def test():
    # end first line with \ to avoid the empty line!
    s = '''\
    hello
      world
    '''
    print repr(s)          # prints '    hello\n      world\n    '
    print repr(dedent(s))  # prints 'hello\n  world\n'


from textwrap import dedent
a = """\
    bee
    bee
        bee
        bee
"""    

class Atxt(object):
    a = """\
    bee
    bee
        bee
        bee
            bee
            bee
    """
    def __init__(self):
        a = dedent("""\
        cee
        cee
            cee
            cee
                cee
                cee
        """)
        print a
    
def gen123(n=3):
    """generate 1,1,1,2,2,2,3,3,3,4,4,4,5,5,5"""
    i = 1
    while 1:
        for j in range(n):
            yield i
        i += 1

def genxyz():
    """generate x,y,z,x,y,z,x,y,z"""
    while 1:
        yield 'X'
        yield 'Y'
        yield 'Z'   

def vertexdata(s, e):
    """generate vertex data comment"""     
    num, xyz = gen123(), genxyz()
    for i in range(s, e):
        yield i, num.next(), xyz.next()

def vertexlines(s, e):
    lst = []
    for i in vertexdata(s, e):
        data, p, c = i
        comment = '!- Vertex %s %s-coordinate {m}' % (p, c)
        lst.append(makeline(data, comment))
    print ''.join(lst)
    