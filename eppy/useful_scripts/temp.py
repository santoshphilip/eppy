from bs4 import BeautifulSoup, Tag



def heading2table(table, row):
    """add heading row to table"""
    tr = Tag(soup, name="tr")
    table.append(tr)
    for attr in row:
        th = Tag(soup, name="th")
        tr.append(th)
        th.append(attr)
    
def row2table(table, row):
    """ad a row to the table"""
    tr = Tag(soup, name="tr")
    table.append(tr)
    for attr in row:
        td = Tag(soup, name="td")
        tr.append(td)
        td.append(attr)

soup = BeautifulSoup()
mem_attr = ['Description', 'PhysicalID', 'Slot', 'Size', 'Width']
men_vals = [str(i) for i in [1,2,3,4,5]]
html = Tag(soup, name="html")
table = Tag(soup, name="table")
table.attrs.update(dict(border="1"))

soup.append(html)
html.append(table)
# tr = Tag(soup, name="tr")
# table.append(tr)
# for attr in mem_attr:
#     th = Tag(soup, name="th")
#     tr.append(th)
#     th.append(attr)
heading2table(table, mem_attr)
for i in range(5):
    row2table(table, men_vals)

print soup.prettify()


    