from BeautifulSoup import BeautifulSoup
import table

fname = 'CV_4autosiz2Table.html'
txt = open(fname, 'r').read()
soup = BeautifulSoup(txt)
head, body = table.getheadbody(soup)

btabledct = table.gettitletabledct(body)
flatbtable = table.flattenkey(btabledct)