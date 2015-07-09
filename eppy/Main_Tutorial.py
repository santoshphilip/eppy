# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Eppy Tutorial

# <markdowncell>

# Authors: Santosh Philip, Leora Tanjuatco

# <markdowncell>

# Eppy is a scripting language for E+ idf files, and E+ output files. Eppy is written in the programming language Python. As a result it takes full advantage of the rich data structure and idioms that are avaliable in python. You can programmatically navigate, search, and modify E+ idf files using eppy. The power of using a scripting language allows you to do the following:
# 
# - Make a large number of changes in an idf file with a few lines of eppy code.
# - Use conditions and filters when making changes to an idf file
# - Make changes to multiple idf files.
# - Read data from the output files of a E+ simulation run.
# - Based to the results of a E+ simulation run, generate the input file for the next simulation run.
# 
# So what does this matter? Here are some of the things you can do with eppy:
# 
# - Change construction for all north facing walls.
# - Change the glass type for all windows larger than 2 square meters.
# - Change the number of people in all the interior zones.
# - Change the lighting power in all south facing zones. 
# - Change the efficiency and fan power of all rooftop units.
# - Find the energy use of all the models in a folder (or of models that were run after a certain date) 
# - If a model is using more energy than expected, keep increasing the R-value of the roof until you get to the expected energy use.

# <headingcell level=2>

# Quick Start

# <markdowncell>

# Here is a short IDF file that I’ll be using as an example to start us off ::

# <rawcell>

#     VERSION,
#         7.2;                     !- Version Identifier
#     
#     SIMULATIONCONTROL,
#         Yes,                     !- Do Zone Sizing Calculation
#         Yes,                     !- Do System Sizing Calculation
#         Yes,                     !- Do Plant Sizing Calculation
#         No,                      !- Run Simulation for Sizing Periods
#         Yes;                     !- Run Simulation for Weather File Run Periods
#     
#     BUILDING,
#         White House,             !- Name
#         30.,                     !- North Axis {deg}
#         City,                    !- Terrain
#         0.04,                    !- Loads Convergence Tolerance Value
#         0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
#         FullExterior,            !- Solar Distribution
#         25,                      !- Maximum Number of Warmup Days
#         6;                       !- Minimum Number of Warmup Days
#     
#     SITE:LOCATION,
#         CHICAGO_IL_USA TMY2-94846,  !- Name
#         41.78,                   !- Latitude {deg}
#         -87.75,                  !- Longitude {deg}
#         -6.00,                   !- Time Zone {hr}
#         190.00;                  !- Elevation {m}

# <markdowncell>

# To use eppy to look at this model, we have to run a little code first:

# <codecell>

# you would normaly install eppy by doing
# python setup.py install
# or
# pip install eppy
# or
# easy_install eppy

# if you have not done so, uncomment the following three lines
import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy) 

from eppy import modeleditor 
from eppy.modeleditor import IDF
iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"

# <codecell>

IDF.setiddname(iddfile)
idf1 = IDF(fname1)

# <markdowncell>

# idf1 now holds all the data to your in you idf file.  
# 
# Now that the behind-the-scenes work is done, we can print this file. 

# <codecell>

idf1.printidf()

# <markdowncell>

# Looks like the same file as before, except that all the comments are slightly different.

# <markdowncell>

# As you can see, this file has four objects:
# 
# - VERSION
# - SIMULATIONCONTROL
# - BUILDING
# - SITE:LOCATION

# <markdowncell>

# So, let us look take a closer look at the BUILDING object.
# We can do this using this command::

# <rawcell>

#     print filename.idfobjects['OBJECTNAME']

# <codecell>

print idf1.idfobjects['BUILDING']  # put the name of the object you'd like to look at in brackets

# <markdowncell>

# We can also zoom in on the object and look just at its individual parts.
# 
# For example, let us look at the name of the building.
# 
# To do this, we have to do some more behind-the-scenes work, which we'll explain later.

# <codecell>

building = idf1.idfobjects['BUILDING'][0]

# <markdowncell>

# Now we can do this:

# <codecell>

print building.Name

# <markdowncell>

# Now that we've isolated the building name, we can change it.

# <codecell>

building.Name = "Empire State Building"

# <codecell>

print building.Name

# <markdowncell>

# Did this actually change the name in the model ? Let us print the entire model and see.

# <codecell>

idf1.printidf()

# <markdowncell>

# Yes! It did. So now you have a taste of what eppy can do. Let's get started!

# <headingcell level=2>

# Modifying IDF Fields

# <markdowncell>

# That was just a quick example -- we were showing off. Let's look a little closer.

# <markdowncell>

# As you might have guessed, changing an IDF field follows this structure:: 

# <rawcell>

#     object.fieldname = "New Field Name"

# <markdowncell>

# Plugging the object name (building), the field name (Name) and our new field name ("Empire State Building") into this command gave us this:

# <codecell>

building.Name = "Empire State Building"

# <codecell>

import eppy
# import eppy.ex_inits
# reload(eppy.ex_inits)
import eppy.ex_inits

# <markdowncell>

# But how did we know that "Name" is one of the fields in the object "building"?
# 
# Are there other fields?
# 
# What are they called?
# 
# Let's take a look at the IDF editor:

# <codecell>

from eppy import ex_inits #no need to know this code, it just shows the image below
for_images = ex_inits
for_images.display_png(for_images.idfeditor) 

# <markdowncell>

# In the IDF Editor, the building object is selected.
# 
# We can see all the fields of the object "BUILDING".
# 
# They are:
# 
# - Name
# - North Axis
# - Terrain
# - Loads Convergence Tolerance Value
# - Temperature Convergence Tolerance Value
# - Solar Distribution
# - Maximum Number of Warmup Days
# - Minimum Number of Warmup Days
# 
# Let us try to access the other fields.

# <codecell>

print building.Terrain

# <markdowncell>

# How about the field "North Axis" ?
# 
# It is not a single word, but two words.
# 
# In a programming language, a variable has to be a single word without any spaces.
# 
# To solve this problem, put an underscore where there is a space.
# 
# So "North Axis" becomes "North_Axis".

# <codecell>

print building.North_Axis

# <markdowncell>

# Now we can do:

# <codecell>

print building.Name
print building.North_Axis
print building.Terrain
print building.Loads_Convergence_Tolerance_Value
print building.Temperature_Convergence_Tolerance_Value
print building.Solar_Distribution
print building.Maximum_Number_of_Warmup_Days
print building.Minimum_Number_of_Warmup_Days

# <markdowncell>

# Where else can we find the field names?
# 
# The IDF Editor saves the idf file with the field name commented next to field.
# 
# Eppy also does this.
# 
# Let us take a look at the "BUILDING" object in the text file that the IDF Editor saves ::

# <rawcell>

#     BUILDING,
#         White House,             !- Name
#         30.,                     !- North Axis {deg}
#         City,                    !- Terrain
#         0.04,                    !- Loads Convergence Tolerance Value
#         0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
#         FullExterior,            !- Solar Distribution
#         25,                      !- Maximum Number of Warmup Days
#         6;                       !- Minimum Number of Warmup Days

# <markdowncell>

# This a good place to find the field names too.
# 
# It is easy to copy and paste from here. You can't do that from the IDF Editor.

# <markdowncell>

# We know that in an E+ model, there will be only ONE "BUILDING" object. This will be the first and only item in the list "buildings".
# 
# But E+ models are made up of objects such as "BUILDING", "SITE:LOCATION", "ZONE", "PEOPLE", "LIGHTS".   There can be a number of "ZONE" objects, a number of "PEOPLE" objects and a number of "LIGHTS" objects.
# 
# So how do you know if you're looking at the first "ZONE" object or the second one? Or the tenth one?  To answer this, we need to learn about how lists work in python.

# <headingcell level=2>

# Python lesson 1: lists

# <markdowncell>

# Eppy holds these objects in a python structure called list. Let us take a look at how lists work in python. 

# <codecell>

fruits = ["apple", "orange", "bannana"] 
# fruits is a list with three items in it.

# <markdowncell>

# To get the first item in fruits we say: 

# <codecell>

fruits[0]  

# <markdowncell>

# Why "0" ?
# 
# Because, unlike us, python starts counting from zero in a list. So, to get the third item in the list we'd need to input 2, like this:

# <codecell>

print fruits[2]

# <markdowncell>

# But calling the first fruit "fruit[0]" is rather cumbersome. Why don't we call it firstfruit?

# <codecell>

firstfruit = fruits[0]
print firstfruit

# <markdowncell>

# We also can say

# <codecell>

goodfruit = fruits[0]
redfruit = fruits[0]

print firstfruit
print goodfruit
print redfruit
print fruits[0]

# <markdowncell>

#  As you see, we can call that item in the list whatever we want.  

# <headingcell level=4>

# How many items in the list

# <markdowncell>

# To know how many items are in a list, we ask for the length of the list.
# 
# The function 'len' will do this for us.

# <codecell>

print len(fruits)

# <markdowncell>

# There are 3 fruits in the list.

# <headingcell level=2>

# Saving an idf file

# <markdowncell>

# This is easy:

# <codecell>

idf1.save()

# <markdowncell>

# If you'd like to do a "Save as..." use this:

# <codecell>

idf1.saveas('something.idf')

# <headingcell level=2>

# Working with E+ objects

# <markdowncell>

# Let us open a small idf file that has only "CONSTRUCTION" and "MATERIAL" objects in it. You can go into "../idffiles/V_7_2/constructions.idf" and take a look at the file. We are not printing it here because it is too big.  
# 
# So let us open it using the idfreader -

# <codecell>

from eppy import modeleditor
from eppy.modeleditor import IDF

iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
try:
    IDF.setiddname(iddfile)
except modeleditor.IDDAlreadySetError as e:
    pass

fname1 = "../eppy/resources/idffiles/V_7_2/constructions.idf"
idf1 = IDF(fname1)

# <markdowncell>

# Let us print all the "MATERIAL" objects in this model.

# <codecell>

materials = idf1.idfobjects["MATERIAL"]
print materials

# <markdowncell>

# As you can see, there are many material objects in this idf file.
# 
# The variable "materials" now contains a list of "MATERIAL" objects.
# 
# You already know a little about lists, so let us take a look at the items in this list.  

# <codecell>

firstmaterial = materials[0]
secondmaterial = materials[1]

# <codecell>

print firstmaterial

# <markdowncell>

# Let us print secondmaterial

# <codecell>

print secondmaterial

# <markdowncell>

# This is awesome!! Why?
# 
# To understand what you can do with your objects organized as lists, you'll have to learn a little more about lists.

# <headingcell level=2>

# Python lesson 2: more about lists

# <headingcell level=4>

# More ways to access items in a list

# <markdowncell>

# You should remember that you can access any item in a list by passing in its index.
# 
# The tricky part is that python starts counting at 0, so you need to input 0 in order to get the first item in a list.
# 
# Following the same logic, you need to input 3 in order to get the fourth item on the list. Like so:

# <codecell>

bad_architects = ["Donald Trump", "Mick Jagger", 
        "Steve Jobs", "Lady Gaga", "Santa Clause"]
print bad_architects[3]

# <markdowncell>

# But there's another way to access items in a list. If you input -1, it will return the last item. -2 will give you the second-to-last item, etc.

# <codecell>

print bad_architects[-1]
print bad_architects[-2]

# <headingcell level=4>

# Slicing a list

# <markdowncell>

# You can also get more than one item in a list:

# <rawcell>

# bad_architects[first_slice:second_slice]

# <codecell>

print bad_architects[1:3] # slices at 1 and 3

# <markdowncell>

# How do I make sense of this?
# 
# To understand this you need to see the list in the following manner::

# <rawcell>

#     [ "Donald Trump", "Mick Jagger", "Steve Jobs", "Lady Gaga", "Santa Clause" ]
#      ^               ^              ^             ^            ^              ^
#      0               1              2             3            4              5
#     -5              -4             -3            -2           -1

# <markdowncell>

# The slice operation bad_architects[1:3] slices right where the numbers are.
# 
# Does that make sense?

# <markdowncell>

# Let us try a few other slices:

# <codecell>

print bad_architects[2:-1] # slices at 2 and -1
print bad_architects[-3:-1] # slices at -3 and -1

# <markdowncell>

# You can also slice in the following way:

# <codecell>

print bad_architects[3:] 
print bad_architects[:2] 
print bad_architects[-3:] 
print bad_architects[:-2] 

# <markdowncell>

# I'll let you figure that out on your own.

# <headingcell level=4>

# Adding to a list

# <markdowncell>

# This is simple: the append function adds an item to the end of the list.
# 
# The following command will add 'something' to the end of the list called listname::

# <rawcell>

#     listname.append(something)

# <codecell>

bad_architects.append("First-year students")
print bad_architects

# <headingcell level=4>

# Deleting from a list

# <markdowncell>

# There are two ways to do this, based on the information you have.  If you have the value of the object, you'll want to use the remove function.  It looks like this:  

# <rawcell>

# listname.remove(value) 

# <markdowncell>

# An example:

# <codecell>

bad_architects.remove("First-year students")
print bad_architects

# <markdowncell>

# What if you know the index of the item you want to remove?
# 
# What if you appended an item by mistake and just want to remove the last item in the list?
# 
# You should use the pop function. It looks like this:

# <rawcell>

# listname.pop(index)

# <codecell>

what_i_ate_today = ["coffee", "bacon", "eggs"]
print what_i_ate_today

# <codecell>

what_i_ate_today.append("vegetables") # adds vegetables to the end of the list
# but I don't like vegetables
print what_i_ate_today

# <codecell>

# since I don't like vegetables
what_i_ate_today.pop(-1) # use index of -1, since vegetables is the last item in the list
print what_i_ate_today

# <markdowncell>

# You can also remove the second item.

# <codecell>

what_i_ate_today.pop(1)

# <markdowncell>

# Notice the 'bacon' in the line above.
# 
# pop actually 'pops' the value (the one you just removed from the list) back to you.  
# 
# Let us pop the first item.

# <codecell>

was_first_item = what_i_ate_today.pop(0)
print 'was_first_item =', was_first_item
print 'what_i_ate_today = ', what_i_ate_today

# <markdowncell>

# what_i_ate_today is just 'eggs'?
# 
# That is not much of a breakfast!  
# 
# Let us get back to eppy.

# <headingcell level=2>

# Continuing to work with E+ objects

# <markdowncell>

# Let us get those "MATERIAL" objects again

# <codecell>

materials = idf1.idfobjects["MATERIAL"]

# <markdowncell>

# With our newfound knowledge of lists, we can do a lot of things.
# 
# Let us get the last material:

# <codecell>

print materials[-1]

# <markdowncell>

# How about the last two?

# <codecell>

print materials[-2:]

# <markdowncell>

# Pretty good.

# <headingcell level=4>

# Counting all the materials ( or counting all objects )

# <markdowncell>

# How many materials are in this model ?

# <codecell>

print len(materials)

# <headingcell level=4>

# Removing a material

# <markdowncell>

# Let us remove the last material in the list

# <codecell>

was_last_material = materials.pop(-1)

# <codecell>

print len(materials)

# <markdowncell>

# Success! We have only 9 materials now.

# <markdowncell>

# The last material used to be:
# 
# 'G05 25mm wood'

# <codecell>

print materials[-1]

# <markdowncell>

# Now the last material in the list is:
# 
# 'M15 200mm heavyweight concrete'

# <headingcell level=4>

# Adding a material to the list

# <markdowncell>

# We still have the old last material

# <codecell>

print was_last_material

# <markdowncell>

# Let us add it back to the list

# <codecell>

materials.append(was_last_material)

# <codecell>

print len(materials)

# <markdowncell>

# Once again we have 10 materials and the last material is:

# <codecell>

print materials[-1]

# <headingcell level=4>

# Add a new material to the model

# <markdowncell>

# So far we have been working only with materials that were already in the list.
# 
# What if we want to make new material?
# 
# Obviously we would use the function 'newidfobject'.

# <codecell>

idf1.newidfobject("MATERIAL")

# <codecell>

len(materials)

# <markdowncell>

# We have 11 items in the materials list.
# 
# Let us take a look at the last material in the list, where this fancy new material was added

# <codecell>

print materials[-1]

# <markdowncell>

# Looks a little different from the other materials. It does have the name we gave it. 
# 
# Why do some fields have values and others are blank ?  
# 
# "addobject" puts in all the default values, and leaves the others blank. It is up to us to put values in the the new fields. 
# 
# Let's do it now.  

# <codecell>

materials[-1].Name = 'Peanut Butter'
materials[-1].Roughness = 'MediumSmooth'
materials[-1].Thickness = 0.03
materials[-1].Conductivity = 0.16
materials[-1].Density = 600
materials[-1].Specific_Heat = 1500

# <codecell>

print materials[-1]

# <headingcell level=4>

# Copy an existing material

# <codecell>

Peanutbuttermaterial = materials[-1]
idf1.copyidfobject(Peanutbuttermaterial)
materials = idf1.idfobjects["MATERIAL"]
len(materials)
materials[-1]

# <headingcell level=2>

# Python lesson 3: indentation and looping through lists

# <markdowncell>

# I'm tired of doing all this work, it's time to make python do some heavy lifting for us!  

# <markdowncell>

# Python can go through each item in a list and perform an operation on any (or every) item in the list.
# 
# This is called looping through the list.
# 
# Here's how to tell python to step through each item in a list, and then do something to every single item.
# 
# We'll use a 'for' loop to do this. ::

# <rawcell>

#     for <variable> in <listname>:
#         <do something>
#             

# <markdowncell>

# A quick note about the second line. Notice that it's indented? There are 4 blank spaces before the code starts::

# <rawcell>

#     in python, indentations are used    
#     to determine the grouping of statements  
#            some languages use symbols to mark 
#            where the function code starts and stops   
#            but python uses indentation to tell you this  
#                     i'm using indentation to
#                     show the beginning and end of a sentence
#            this is a very simple explanation
#            of indentation in python
#      if you'd like to know more, there is plenty of information
#      about indentation in python on the web
#     

# <markdowncell>

# It's elegant, but it means that the indentation of the code holds meaning.
# 
# So make sure to indent the second (and third and forth) lines of your loops!
# 
# Now let's make some fruit loops.  

# <codecell>

fruits = ["apple", "orange", "bannana"] 

# <markdowncell>

# Given the syntax I gave you before I started rambling about indentation, we can easily print every item in the fruits list by using a 'for' loop.

# <codecell>

for fruit in fruits:
   print fruit
    

# <markdowncell>

# That was easy! But it can get complicated pretty quickly... 
# 
# Let's make it do something more complicated than just print the fruits.  
# 
# Let's have python add some words to each fruit. 

# <codecell>

for fruit in fruits:
    print "I am a fruit said the", fruit
    

# <markdowncell>

# Now we'll try to confuse you:

# <codecell>

rottenfruits = [] # makes a blank list called rottenfruits
for fruit in fruits: # steps through every item in fruits
    rottenfruit = "rotten " + fruit # changes each item to "rotten _____"
    rottenfruits.append(rottenfruit) # adds each changed item to the formerly empty list
    

# <codecell>

print rottenfruits

# <codecell>

# here's a shorter way of writing it
rottenfruits = ["rotten " + fruit for fruit in fruits]

# <markdowncell>

# Did you follow all that??
# 
# Just in case you didn't, let's review that last one::

# <rawcell>

#     ["rotten " + fruit for fruit in fruits]
#                        -------------------
#                        This is the "for loop"
#                        it steps through each fruit in fruits
#     
#     ["rotten " + fruit for fruit in fruits]
#      -----------------
#      add "rotten " to the fruit at each step
#      this is your "do something"
#      
#     ["rotten " + fruit for fruit in fruits]
#     ---------------------------------------
#     give a new list that is a result of the "do something"

# <codecell>

print rottenfruits

# <headingcell level=4>

# Filtering in a loop

# <markdowncell>

# But what if you don't want to change *every* item in a list?
# 
# We can use an 'if' statement to operate on only some items in the list.  
# 
# Indentation is also important in 'if' statements, as you'll see::

# <rawcell>

#     if <someconstraint>:
#         <if the first line is true, do this>
#     <but if it's false, do this>
#                

# <codecell>

fruits = ["apple", "orange", "pear", "berry", "mango", "plum", "peach", "melon", "bannana"]

# <codecell>

for fruit in fruits:               # steps through every fruit in fruits
    if len(fruit) > 5:             # checks to see if the length of the word is more than 5
        print fruit                # if true, print the fruit
                                   # if false, python goes back to the 'for' loop 
                                      # and checks the next item in the list
                

# <markdowncell>

# Let's say we want to pick only the fruits that start with the letter 'p'. 

# <codecell>

p_fruits = []                      # creates an empty list called p_fruits
for fruit in fruits:               # steps through every fruit in fruits
    if fruit.startswith("p"):      # checks to see if the first letter is 'p', using a built-in function
        p_fruits.append(fruit)     # if the first letter is 'p', the item is added to p_fruits
                                   # if the first letter is not 'p', python goes back to the 'for' loop
                                      # and checks the next item in the list
                

# <codecell>

print p_fruits

# <codecell>

# here's a shorter way to write it
p_fruits = [fruit for fruit in fruits if fruit.startswith("p")]

# <markdowncell>

# ::

# <rawcell>

#     [fruit for fruit in fruits if fruit.startswith("p")]
#            -------------------
#            for loop
#     
#     [fruit for fruit in fruits if fruit.startswith("p")]
#                                ------------------------
#                                pick only some of the fruits
#     
#     [fruit for fruit in fruits if fruit.startswith("p")]
#      -----
#      give me the variable fruit as it appears in the list, don't change it
#      
#     [fruit for fruit in fruits if fruit.startswith("p")]
#     ----------------------------------------------------
#     a fresh new list with those fruits
#     

# <codecell>

print p_fruits

# <headingcell level=4>

# Counting through loops

# <markdowncell>

# This is not really needed, but it is nice to know. You can safely skip this.

# <markdowncell>

# Python's built-in function range() makes a list of numbers within a range that you specify.
# 
# This is useful because you can use these lists inside of loops.

# <codecell>

range(4) # makes a list

# <codecell>

for i in range(4):
    print i
    

# <codecell>

len(p_fruits)

# <codecell>

for i in range(len(p_fruits)):
    print i
    

# <codecell>

for i in range(len(p_fruits)):
    print p_fruits[i]
    

# <codecell>

for i in range(len(p_fruits)):
    print i,  p_fruits[i]
    

# <codecell>

for item_from_enumerate in enumerate(p_fruits):
    print item_from_enumerate
    

# <codecell>

for i, fruit in enumerate(p_fruits):
    print i, fruit
    

# <headingcell level=2>

# Looping through E+ objects

# <markdowncell>

# If you have read the python explanation of loops, you are now masters of using loops.
# 
# Let us use the loops with E+ objects.
# 
# We'll continue to work with the materials list.

# <codecell>

for material in materials:
    print material.Name 
    

# <codecell>

[material.Name for material in materials] 

# <codecell>

[material.Roughness for material in materials]

# <codecell>

[material.Thickness for material in materials]

# <codecell>

[material.Thickness for material in materials if material.Thickness > 0.1]

# <codecell>

[material.Name for material in materials if material.Thickness > 0.1]

# <codecell>

thick_materials = [material for material in materials if material.Thickness > 0.1]

# <codecell>

thick_materials

# <codecell>

# change the names of the thick materials
for material in thick_materials:
    material.Name = "THICK " + material.Name
    

# <codecell>

thick_materials

# <markdowncell>

# So now we're working with two different lists: materials and thick_materials.
# 
# But even though the items can be separated into two lists, we're still working with the same items.
# 
# Here's a helpful illustration:

# <codecell>

for_images.display_png(for_images.material_lists) # display the image below

# <codecell>

# here's the same concept, demonstrated with code
# remember, we changed the names of the items in the list thick_materials
# these changes are visible when we print the materials list; the thick materials are also in the materials list
[material.Name for material in materials]

# <headingcell level=2>

# Geometry functions in eppy

# <markdowncell>

# Sometimes, we want information about the E+ object that is not in the fields. For example, it would be useful to know the areas and orientations of the surfaces. These attributes of the surfaces are not in the fields of surfaces, but surface objects *do* have fields that have the coordinates of the surface. The areas and orientations can be calculated from these coordinates.  
# 
# Pyeplus has some functions that will do the calculations.  
# 
# In the present version, pyeplus will calculate:
# 
# - surface azimuth
# - surface tilt
# - surface area
# 
# Let us explore these functions

# <codecell>

# OLD CODE, SHOULD BE DELETED
# from idfreader import idfreader

# iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
# fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
# model, to_print, idd_info = idfreader(fname, iddfile)
# surfaces = model['BUILDINGSURFACE:DETAILED'] # all the surfaces

# <codecell>

from eppy import modeleditor
from eppy.modeleditor import IDF

iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
try:
    IDF.setiddname(iddfile)
except modeleditor.IDDAlreadySetError as e:
    pass


fname1 = "../eppy/resources/idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
idf1 = IDF(fname1)
surfaces = idf1.idfobjects['BUILDINGSURFACE:DETAILED']

# <codecell>

# Let us look at the first surface
asurface = surfaces[0]
print "surface azimuth =",  asurface.azimuth, "degrees"
print "surface tilt =", asurface.tilt, "degrees"
print "surface area =", asurface.area, "m2"

# <codecell>

# all the surface names
s_names = [surface.Name for surface in surfaces]
print s_names[:5] # print five of them

# <codecell>

# surface names and azimuths
s_names_azm = [(sf.Name, sf.azimuth) for sf in surfaces]
print s_names_azm[:5] # print five of them

# <codecell>

# or to do that in pretty printing
for name, azimuth in s_names_azm[:5]: # just five of them
    print name, azimuth
    

# <codecell>

# surface names and tilt
s_names_tilt = [(sf.Name, sf.tilt) for sf in surfaces]
for name, tilt in s_names_tilt[:5]: # just five of them
    print name, tilt
    

# <codecell>

# surface names and areas
s_names_area = [(sf.Name, sf.area) for sf in surfaces]
for name, area in s_names_area[:5]: # just five of them
    print name, area, "m2"
    

# <markdowncell>

# Let us try to isolate the exterior north facing walls and change their construnctions

# <codecell>

# just vertical walls
vertical_walls = [sf for sf in surfaces if sf.tilt == 90.0]
print [sf.Name for sf in vertical_walls]

# <codecell>

# north facing walls
north_walls = [sf for sf in vertical_walls if sf.azimuth == 0.0]
print [sf.Name for sf in north_walls]

# <codecell>

# north facing exterior walls
exterior_nwall = [sf for sf in north_walls if sf.Outside_Boundary_Condition == "Outdoors"]
print [sf.Name for sf in exterior_nwall]

# <codecell>

# print out some more details of the north wall
north_wall_info = [(sf.Name, sf.azimuth, sf.Construction_Name) for sf in exterior_nwall]
for name, azimuth, construction in north_wall_info:
    print name, azimuth, construction
    

# <codecell>

# change the construction in the exterior north walls
for wall in exterior_nwall:
    wall.Construction_Name = "NORTHERN-WALL" # make sure such a construction exists in the model
    

# <codecell>

# see the change
north_wall_info = [(sf.Name, sf.azimuth, sf.Construction_Name) for sf in exterior_nwall]
for name, azimuth, construction in north_wall_info:
    print name, azimuth, construction
    

# <codecell>

# see this in all surfaces
for sf in surfaces:
    print sf.Name, sf.azimuth, sf.Construction_Name
    

# <markdowncell>

# You can see the "NORTHERN-WALL" in the print out above.
# 
# This shows that very sophisticated modification can be made to the model rather quickly. 

