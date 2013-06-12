# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

from BeautifulSoup import BeautifulSoup
import table

fname = 'CV_4autosiz2Table.html'
txt = open(fname, 'r').read()
# txt = """<html><head><title>Page title</title></head><body><p id="firstpara" align="center">This is paragraph <b>one</b>.<p id="secondpara" align="blah">This is paragraph <b>two</b>.</html>
# """
soup = BeautifulSoup(txt)

head, body = table.getheadbody(soup)

# btable = []        
# for obj in body.contents:
#     try:
#         if obj.name in ('b', 'table'):
#             btable.append(obj)
#     except AttributeError, e:
#         pass
# 
# 
# bolds = [obj for obj in btable if obj.name == 'b']
# tables = [obj for obj in btable if obj.name == 'table']

btable = []        
tup = []
for obj in body.contents:
    try:
        if obj.name == 'b':
            tup = [obj]
        if obj.name == 'table':
            tup.append(obj)
            btable.append(tup)
    except AttributeError, e:
        pass
        
bold = [b for b, t in btable]
for b in bold:
    print b.contents[0]



btable[0][0].contents[0].replaceWith("gumby")
print soup
        
# from BeautifulSoup import BeautifulSoup
# soup = BeautifulSoup("""<b id="2">Argh!</b>""")
# print soup
# # <b id="2">Argh!</b>
# b = soup.b
# 
# b['id'] = 10
# print soup
# # <b id="10">Argh!</b>
# 
# b['id'] = "ten"
# print soup
# # <b id="ten">Argh!</b>
# 
# b['id'] = 'one "million"'
# print soup
# # <b id='one "million"'>Argh!</b>        

m1 = [[2,4,5], [5,6,7]]
m2 = [[2,4,5], [5,6]]