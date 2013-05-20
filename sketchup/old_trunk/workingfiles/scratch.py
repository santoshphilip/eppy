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
    



