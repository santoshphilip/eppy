"""read the html outputs"""

from bs4 import BeautifulSoup

class NotSimpleTable(Exception):
    pass
        

def is_simpletable(table):
    """test if the table has only strings in the cells"""
    tds = table('td')
    for td in tds:
        if td.contents != []:
            if len(td.contents) == 1:
                if not isinstance(td.contents[0], NavigableString):
                    return False
            else:
                return False
    return True

def table2matrix(table):
    """convert a table to a list of lists - a 2D matrix"""
    if not is_simpletable(table):
        raise NotSimpleTable, "Not able read a cell in the table as a string"
    rows = []
    for tr in table('tr'):
        row = []
        for td in tr('td'):
            try:
                row.append(td.contents[0])
            except IndexError, e:
                row.append('')
        rows.append(row)
    return rows

fname = "../outputfiles/V_7_2/5ZoneCAVtoVAVWarmestTempFlowTable.html"
html_doc = open(fname, 'r').read()

soup = BeautifulSoup(html_doc)
all = soup.find_all(['b', 'table'])
all[0]
all[1]
all[2]
all[3]
all[4]
all[8]
all[9]
all[10]
all[11]
all[0]
all[0].name
