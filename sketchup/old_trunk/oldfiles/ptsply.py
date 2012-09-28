import upfront
from flatten import flatten

txt = open('a.txt', 'r').read()
lst = txt.split('--------------------')
lst.pop(0)
lst1 = [block.splitlines()[1:] for block in lst]
from flatten import flatten
lst2 = [x.split(',') for x in flatten(lst1)]
pts = [[float(p) for p in pt] for pt in lst2]
nn = 0
outer = []
for i,  item in enumerate(lst1):
    inner = []
    for j in range(len(item)):
        inner.append(nn)
        nn += 1
    outer.append(inner)

upfront.saveupfver1((pts, outer), outfile='b.up1')
