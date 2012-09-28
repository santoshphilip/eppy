
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
    



