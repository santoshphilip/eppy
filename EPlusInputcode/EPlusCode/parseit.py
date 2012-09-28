from BeautifulSoup import BeautifulSoup

fname = 'CAVsystem1exp1Table.html'
txt = open(fname, 'r').read()
txt = """<html><head><title>Page title</title></head><body><p id="firstpara" align="center">This is paragraph <b>one</b>.<p id="secondpara" align="blah">This is paragraph <b>two</b>.</html>
"""
soup = BeautifulSoup(txt)

# for sp in range(len(soup.contents)):
#     try 

for obj in soup.contents:
    try:
        # there may be 
        if obj.name == 'html':
            html = obj
            break
    except AttributeError, e:
        pass
        
for obj in html.contents:
    try:
        if obj.name == 'head':
            head = obj
        if obj.name == 'body':
            body = obj
    except AttributeError, e:
        pass
        
# for obj in body.contents:
#     try:
#         print obj.name
#     except AttributeError, e:
#         print 'no name'

btable = []        
for obj in body.contents:
    try:
        if obj.name in ('b', 'table'):
            btable.append(obj)
    except AttributeError, e:
        pass


bolds = [obj for obj in btable if obj.name == 'b']
tables = [obj for obj in btable if obj.name == 'table']
# for bold in bolds:
#     print bold.contents

table = tables[0]            
trs = []
for obj in table.contents:
    try:
        if obj.name == 'tr':
            trs.append(obj)
    except AttributeError, e:
        pass

tr = trs[0]
tds = []
row = []
for obj in tr.contents:
    try:
        if obj.name == 'td':
            tds.append(obj)
            row.append(obj.contents)
    except AttributeError, e:
        pass

td = tds[1]
try:
    cell = td.contents[0]
except IndexError, e:
    cell = ''

arow = []
for cell in row:
    try:
        arow.append(cell[0])
    except IndexError, e:
        arow.append('')
            
        
print table