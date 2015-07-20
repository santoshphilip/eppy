# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Reading outputs from E+

# <codecell>

# some initial set up
# if you have not installed epp, and only downloaded it
# you will need the following lines
import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy) 

# <headingcell level=2>

# Using titletable() to get at the tables

# <markdowncell>

# So far we have been making changes to the IDF input file.
# How about looking at the outputs.
# 
# Energyplus makes nice htmlout files that look like this.

# <codecell>

from eppy import ex_inits #no need to know this code, it just shows the image below
for_images = ex_inits
for_images.display_png(for_images.html_snippet1) #display the image below

# <markdowncell>

# If you look at the clipping of the html file above, you see tables with data in them. Eppy has functions that let you access of these tables and get the data from any of it's cells.
# 
# Let us say you want to find the "Net Site Energy".  
# 
# This is in table "Site and Source Energy".  
# 
# The number you want is in the third row, second column and it's value is "47694.47"
# 
# Let us use eppy to extract this number

# <codecell>

from eppy import readhtml # the eppy module with functions to read the html
fname = "../eppy/resources/outputfiles/V_7_2/5ZoneCAVtoVAVWarmestTempFlowTable_ABUPS.html" # the html file you want to read
filehandle = open(fname, 'r').read() # get a file handle to the html file


htables = readhtml.titletable(filehandle) # reads the tables with their titles

# <markdowncell>

# If you open the python file readhtml.py and look at the function titletable, you can see the function documentation.
# 
# It says the following

# <rawcell>

#     """return a list of [(title, table), .....]
#     title = previous item with a <b> tag
#     table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]"""
#     

# <markdowncell>

# The documentation says that it returns a list.
# Let us take a look inside this list.
# Let us look at the first item in the list.

# <codecell>

firstitem = htables[0]
print(firstitem)

# <markdowncell>

# Ughh !!! that is ugly. Hard to see what it is.  
# Let us use a python module to print it pretty

# <codecell>

import pprint
pp = pprint.PrettyPrinter()
pp.pprint(firstitem)

# <markdowncell>

# Nice. that is a little clearer

# <codecell>

firstitem_title = firstitem[0]
pp.pprint(firstitem_title)

# <codecell>

firstitem_table = firstitem[1]
pp.pprint(firstitem_table)

# <markdowncell>

# How do we get to value of "Net Site Energy".  
# We know it is in the third row, second column of the table.  
# 
# Easy.

# <codecell>

thirdrow = firstitem_table[2] # we start counting with 0. So 0, 1, 2 is third row
print(thirdrow)

# <codecell>

thirdrow_secondcolumn = thirdrow[1]
thirdrow_secondcolumn

# <markdowncell>

# the text from the html table is in unicode.  
# That is why you see that weird 'u' letter.  
# 
# Let us convert it to a floating point number

# <codecell>

net_site_energy = float(thirdrow_secondcolumn)
net_site_energy

# <markdowncell>

# Let us have a little fun with the tables.  
# 
# Get the titles of all the tables

# <codecell>

alltitles = [htable[0] for htable in htables]
alltitles

# <markdowncell>

# Now let us grab the tables with the titles "Building Area" and "Site to Source Energy Conversion Factors"

# <markdowncell>

# twotables = [htable for htable in htables if htable[0] in ["Building Area", "Site to Source Energy Conversion Factors"]]
# twotables

# <markdowncell>

# Let us leave readtables for now. 
# 
# It gives us the basic functionality to read any of the tables in the html output file.

# <headingcell level=2>

# Using lines_table() to get at the tables

# <markdowncell>

# We have been using titletable() to get at the tables. There is a constraint using function titletable(). Titletable() assumes that there is a unique title (in HTML bold) just above the table. It is assumed that this title will adequetly describe the table. This is true in most cases and titletable() is perfectly good to use. Unfortuntely there are some tables that do not follow this rule. The snippet below shows one of them.

# <codecell>

from eppy import ex_inits #no need to know this code, it just shows the image below
for_images = ex_inits
for_images.display_png(for_images.html_snippet2) # display the image below

# <markdowncell>

# Notice that the HTML snippet shows a table with three lines above it. The first two lines have information that describe the table. We need to look at both those lines to understand what the table contains. So we need a different function that will capture all those lines before the table. The funtion lines_table() described below will do this.

# <codecell>

from eppy import readhtml # the eppy module with functions to read the html
fname = "../eppy/resources/outputfiles/V_8_1/ASHRAE30pct.PI.Final11_OfficeMedium_STD2010_Chicago-baseTable.html" # the html file you want to read
filehandle = open(fname, 'r').read() # get a file handle to the html file


ltables = readhtml.lines_table(filehandle) # reads the tables with their titles

# <markdowncell>

# The html snippet shown above is the last table in HTML file we just opened. We have used lines_table() to read the tables into the variable ltables. We can get to the last table by ltable[-1]. Let us print it and see what we have.

# <codecell>

import pprint
pp = pprint.PrettyPrinter()
pp.pprint(ltables[-1])

# <markdowncell>

# We can see that ltables has captured all the lines before the table. Let us make our code more explicit to see this

# <codecell>

last_ltable = ltables[-1]
lines_before_table = last_ltable[0]
table_itself = last_ltable[-1]

pp.pprint(lines_before_table)

# <markdowncell>

# We found this table the easy way this time, because we knew it was the last one. How do we find it if we don't know where it is in the file ? Python comes to our rescue :-) Let assume that we want to find the table that has the following two lines before it.
# 
# - Report: FANGER DURING COOLING AND ADAPTIVE COMFORT
# - For: PERIMETER_MID_ZN_4

# <codecell>

line1 = 'Report: FANGER DURING COOLING AND ADAPTIVE COMFORT'
line2 = 'For: PERIMETER_MID_ZN_4'
#
# check if those two lines are before the table
line1 in lines_before_table and line2 in lines_before_table

# <codecell>

# find all the tables where those two lines are before the table
[ltable for ltable in ltables 
    if line1 in ltable[0] and line2 in ltable[0]]

# <markdowncell>

# That worked !
# 
# What if you want to find the words "FANGER"  and "PERIMETER_MID_ZN_4" before the table. The following code will do it.

# <codecell>

# sample code to illustrate what we are going to do
last_ltable = ltables[-1]
lines_before_table = last_ltable[0]
table_itself = last_ltable[-1]

# join lines_before_table into a paragraph of text
justtext = '\n'.join(lines_before_table)
print(justtext)

# <codecell>

"FANGER" in justtext and "PERIMETER_MID_ZN_4" in justtext

# <codecell>

# Let us combine the this trick to find the table
[ltable for ltable in ltables 
    if "FANGER" in '\n'.join(ltable[0]) and "PERIMETER_MID_ZN_4" in '\n'.join(ltable[0])]

# <headingcell level=2>

# Extracting data from the tables

# <markdowncell>

# The tables in the HTML page in general have text in the top header row. The first vertical row has text. The remaining cells have numbers. We can identify the numbers we need by looking at the labelin the top row and the label in the first column. Let us construct a simple example and explore this.

# <codecell>

# ignore the following three lines. I am using them to construct the table below
from IPython.display import HTML
atablestring = '<TABLE cellpadding="4" style="border: 1px solid #000000; border-collapse: collapse;" border="1">\n <TR>\n  <TD>&nbsp;</TD>\n  <TD>a b</TD>\n  <TD>b c</TD>\n  <TD>c d</TD>\n </TR>\n <TR>\n  <TD>x y</TD>\n  <TD>1</TD>\n  <TD>2</TD>\n  <TD>3</TD>\n </TR>\n <TR>\n  <TD>y z</TD>\n  <TD>4</TD>\n  <TD>5</TD>\n  <TD>6</TD>\n </TR>\n <TR>\n  <TD>z z</TD>\n  <TD>7</TD>\n  <TD>8</TD>\n  <TD>9</TD>\n </TR>\n</TABLE>'
HTML(atablestring)

# <markdowncell>

# This table is actually in the follwoing form:

# <codecell>

atable = [["",  "a b", "b c", "c d"],
     ["x y", 1,     2,     3 ],
     ["y z", 4,     5,     6 ],
     ["z z", 7,     8,     9 ],]

# <markdowncell>

# We can see the labels in the table. So we an look at row "x y" and column "c d". The value there is 3

# <markdowncell>

# right now we can get to it by saying atable[1][3]

# <codecell>

print(atable[1][3])

# <markdowncell>

# readhtml has some functions that will let us address the values by the labels. We use a structure from python called named tuples to do this. The only limitation is that the labels have to be letters or digits. Named tuples does not allow spaces in the labels. We could replace the space with an underscore ' _ '. So "a b" will become "a_b". So we can look for row "x_y" and column "c_d". Let us try this out.

# <codecell>

from eppy import readhtml
h_table = readhtml.named_grid_h(atable)

# <codecell>

print(h_table.x_y.c_d)

# <markdowncell>

# We can still get to the value by index

# <codecell>

print(h_table[0][2])

# <markdowncell>

# Note that we used atable[1][3], but here we used h_table[0][2]. That is because h_table does not count the rows and columns where the labels are.

# <markdowncell>

# We can also do the following:

# <codecell>

print(h_table.x_y[2])
# or
print(h_table[0].c_d)

# <markdowncell>

# Wow … that is pretty cool. What if we want to just check what the labels are ?

# <codecell>

print(h_table._fields)

# <markdowncell>

# That gives us the horizontal lables. How about the vertical labels ?

# <codecell>

h_table.x_y._fields

# <markdowncell>

# There you go !!!

# <markdowncell>

# How about if I want to use the labels differently ? Say I want to refer to the row first and then to the column. That woul be saying table.c_d.x_y. We can do that by using a different function

# <codecell>

v_table = readhtml.named_grid_v(atable)
print(v_table.c_d.x_y)

# <markdowncell>

# And we can do the following

# <codecell>

print(v_table[2][0])
print(v_table.c_d[0])
print(v_table[2].x_y)

# <markdowncell>

# Let us try to get the numbers in the first column and then get their sum

# <codecell>

v_table.a_b

# <markdowncell>

# Look like we got the right column. But not in the right format. We really need a list of numbers

# <codecell>

[cell for cell in v_table.a_b]

# <markdowncell>

# That looks like waht we wanted. Now let us get the sum

# <codecell>

values_in_first_column = [cell for cell in v_table.a_b]
print(values_in_first_column)
print(sum(values_in_first_column)) # sum is a builtin function that will sum a list

# <markdowncell>

# To get the first row we use the variable h_table

# <codecell>

values_in_first_row = [cell for cell in h_table.x_y]
print(values_in_first_row)
print(sum(values_in_first_row))

# <codecell>


