from BeautifulSoup import BeautifulSoup, Tag
soup = BeautifulSoup()
mem_attr = ['Description', 'PhysicalID', 'Slot', 'Size', 'Width']
html = Tag(soup, name="html")
table = Tag(soup, name="table")
tr = Tag(soup, name="tr")
soup.append(html)
html.append(table)
table.append(tr)
for attr in mem_attr:
    th = Tag(soup, name="th")
    tr.append(th)
    th.append(attr)

print soup.prettify()