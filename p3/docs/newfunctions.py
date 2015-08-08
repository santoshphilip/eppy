# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# New functions

# <markdowncell>

# These are recently written functions that have not made it into the main documentation

# <headingcell level=2>

# Python Lesson: Errors and Exceptions

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

# <markdowncell>

# When things go wrong in your eppy script, you get "Errors and Exceptions". 
# 
# To know more about how this works in python and eppy, take a look at [Python: Errors and Exceptions](http://docs.python.org/2/tutorial/errors.html)

# <headingcell level=2>

# Setting IDD name

# <markdowncell>

# When you work with Energyplus you are working with **idf** files (files that have the extension \*.idf). There is another file that is very important, called the **idd** file. This is the file that defines all the objects in Energyplus. Esch version of Energyplus has a different **idd** file. 
# 
# So eppy needs to know which **idd** file to use. Only one **idd** file can be used in a script or program. This means that you cannot change the **idd** file once you have selected it. Of course you have to first select an **idd** file before eppy can work.
# 
# If you use eppy and break the above rules, eppy will raise an exception. So let us use eppy incorrectly and make eppy raise the exception, just see how that happens.
# 
# First let us try to open an **idf** file without setting an **idd** file.

# <codecell>

from eppy import modeleditor 
from eppy.modeleditor import IDF
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"

# <markdowncell>

# Now let us open file fname1 without setting the **idd** file

# <codecell>

try:
    idf1 = IDF(fname1)
except modeleditor.IDDNotSetError as e:
    print("raised eppy.modeleditor.IDDNotSetError")
    

# <markdowncell>

# OK. It does not let you do that and it raises an exception
# 
# So let us set the **idd** file and then open the idf file

# <codecell>

iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
IDF.setiddname(iddfile)
idf1 = IDF(fname1)

# <markdowncell>

# That worked without raising an exception
# 
# Now let us try to change the **idd** file. Eppy should not let you do this and should raise an exception.

# <codecell>

try:
    IDF.setiddname("anotheridd.idd")
except modeleditor.IDDAlreadySetError as e:
    print("raised modeleditor.IDDAlreadySetError")   
    

# <markdowncell>

# Excellent!! It raised the exception we were expecting.

# <headingcell level=2>

# Check range for fields

# <markdowncell>

# The fields of idf objects often have a range of legal values. The following functions will let you discover what that range is and test if your value lies within that range

# <markdowncell>

# demonstrate two new functions:
# 
# - EpBunch.getrange(fieldname) # will return the ranges for that field
# - EpBunch.checkrange(fieldname) # will throw an exception if the value is outside the range

# <codecell>

from eppy import modeleditor 
from eppy.modeleditor import IDF
iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"

# <codecell>

# IDF.setiddname(iddfile)# idd ws set further up in this page
idf1 = IDF(fname1)

# <codecell>

building = idf1.idfobjects['building'.upper()][0]
print(building)

# <codecell>

print(building.getrange("Loads_Convergence_Tolerance_Value"))

# <codecell>

print(building.checkrange("Loads_Convergence_Tolerance_Value"))

# <markdowncell>

# Let us set these values outside the range and see what happens

# <codecell>

building.Loads_Convergence_Tolerance_Value = 0.6
from eppy.bunch_subclass import RangeError
try:
    print(building.checkrange("Loads_Convergence_Tolerance_Value"))
except RangeError as e:
    print("raised range error")
    

# <markdowncell>

# So the Range Check works

# <headingcell level=2>

# Looping through all the fields in an idf object

# <markdowncell>

# We have seen how to check the range of field in the idf object. What if you want to do a *range check* on all the fields in an idf object ? To do this we will need a list of all the fields in the idf object. We can do this easily by the following line

# <codecell>

print(building.fieldnames)

# <markdowncell>

# So let us use this

# <codecell>

for fieldname in building.fieldnames:
    print("%s = %s" % (fieldname, building[fieldname]))
    

# <markdowncell>

# Now let us test if the values are in the legal range. We know that "Loads_Convergence_Tolerance_Value" is out of range

# <codecell>

from eppy.bunch_subclass import RangeError
for fieldname in building.fieldnames:
    try:
        building.checkrange(fieldname)
        print("%s = %s #-in range" % (fieldname, building[fieldname],))
    except RangeError as e:
        print("%s = %s #-****OUT OF RANGE****" % (fieldname, building[fieldname],))
        

# <markdowncell>

# You see, we caught the out of range value

# <headingcell level=2>

# Blank idf file

# <markdowncell>

# Until now in all our examples, we have been reading an idf file from disk:
# 
# - How do I create a blank new idf file  
# - give it a file name
# - Save it to the disk
# 
# Here are the steps to do that

# <codecell>

# some initial steps
from eppy.modeleditor import IDF
iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
# IDF.setiddname(iddfile) # Has already been set 

# - Let us first open a file from the disk
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
idf_fromfilename = IDF(fname1) # initialize the IDF object with the file name

idf_fromfilename.printidf()

# <codecell>

# - now let us open a file from the disk differently
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
fhandle = open(fname1, 'r') # open the file for reading and assign it a file handle
idf_fromfilehandle = IDF(fhandle) # initialize the IDF object with the file handle

idf_fromfilehandle.printidf()

# <codecell>

# So IDF object can be initialized with either a file name or a file handle

# - How do I create a blank new idf file  
idftxt = "" # empty string
from io import StringIO
fhandle = StringIO(idftxt) # we can make a file handle of a string
idf_emptyfile = IDF(fhandle) # initialize the IDF object with the file handle

idf_emptyfile.printidf()

# <markdowncell>

# It did not print anything. Why should it. It was empty. 
# 
# What if we give it a string that was not blank

# <codecell>

# - The string does not have to be blank
idftxt = "VERSION, 7.3;" # Not an emplty string. has just the version number
fhandle = StringIO(idftxt) # we can make a file handle of a string
idf_notemptyfile = IDF(fhandle) # initialize the IDF object with the file handle

idf_notemptyfile.printidf()

# <markdowncell>

# Aha !
# 
# Now let us give it a file name

# <codecell>

# - give it a file name
idf_notemptyfile.idfname = "notemptyfile.idf"
# - Save it to the disk
idf_notemptyfile.save()

# <markdowncell>

# Let us confirm that the file was saved to disk

# <codecell>

txt = open("notemptyfile.idf", 'r').read()# read the file from the disk
print(txt)

# <markdowncell>

# Yup ! that file was saved. Let us delete it since we were just playing

# <codecell>

import os
os.remove("notemptyfile.idf")

# <headingcell level=2>

# Deleting, copying/adding and making new idfobjects

# <headingcell level=3>

# Making a new idf object

# <markdowncell>

# Let us start with a blank idf file and make some new "MATERIAL" objects in it

# <codecell>

# making a blank idf object
blankstr = ""
from io import StringIO
idf = IDF(StringIO(blankstr))

# <markdowncell>

# To make and add a new idfobject object, we use the function IDF.newidfobject(). We want to make an object of type "MATERIAL"

# <codecell>

newobject = idf.newidfobject("material".upper()) # the key for the object type has to be in upper case
                                     # .upper() makes it upper case
    

# <codecell>

print(newobject)

# <markdowncell>

# Let us give this a name, say "Shiny new material object"

# <codecell>

newobject.Name = "Shiny new material object"
print(newobject)

# <codecell>

anothermaterial = idf.newidfobject("material".upper())
anothermaterial.Name = "Lousy material"
thirdmaterial = idf.newidfobject("material".upper())
thirdmaterial.Name = "third material"
print(thirdmaterial)

# <markdowncell>

# Let us look at all the "MATERIAL" objects

# <codecell>

print(idf.idfobjects["MATERIAL"])

# <markdowncell>

# As we can see there are three MATERIAL idfobjects. They are:
# 
# 1. Shiny new material object
# 2. Lousy material
# 3. third material

# <headingcell level=3>

# Deleting an idf object

# <markdowncell>

# Let us remove 2. Lousy material. It is the second material in the list. So let us remove the second material

# <codecell>

idf.popidfobject('MATERIAL', 1) # first material is '0', second is '1'

# <codecell>

print(idf.idfobjects['MATERIAL'])

# <markdowncell>

# You can see that the second material is gone ! Now let us remove the first material, but do it using a different function

# <codecell>

firstmaterial = idf.idfobjects['MATERIAL'][-1]

# <codecell>

idf.removeidfobject(firstmaterial)

# <codecell>

print(idf.idfobjects['MATERIAL'])

# <markdowncell>

# So we have two ways of deleting an idf object:
# 
# 1. popidfobject -> give it the idf key: "MATERIAL", and the index number
# 2. removeidfobject -> give it the idf object to be deleted

# <headingcell level=3>

# Copying/Adding an idf object

# <markdowncell>

# Having deleted two "MATERIAL" objects, we have only one left. Let us make a copy of this object and add it to our idf file

# <codecell>

onlymaterial = idf.idfobjects["MATERIAL"][0]

# <codecell>

idf.copyidfobject(onlymaterial)

# <codecell>

print(idf.idfobjects["MATERIAL"])

# <markdowncell>

# So now we have a copy of the material. You can use this method to copy idf objects from other idf files too.

# <headingcell level=2>

# Making an idf object with named arguments

# <markdowncell>

# What if we wanted to make an idf object with values for it's fields? We can do that too.

# <headingcell level=2>

# Renaming an idf object

# <codecell>

gypboard = idf.newidfobject('MATERIAL', Name="G01a 19mm gypsum board",
                            Roughness="MediumSmooth",
                            Thickness=0.019,
                            Conductivity=0.16,
                            Density=800,
                            Specific_Heat=1090)

# <codecell>

print(gypboard)

# <markdowncell>

# newidfobject() also fills in the default values like "Thermal Absorptance", "Solar Absorptance", etc.

# <codecell>

print(idf.idfobjects["MATERIAL"])

# <headingcell level=2>

# Renaming an idf object

# <markdowncell>

# It is easy to rename an idf object. If we want to rename the gypboard object that we created above, we simply say:

# <rawcell>

#     gypboard.Name = "a new name".

# <markdowncell>

# But this could create a problem. What if this gypboard is part of a "CONSTRUCTION" object. The construction object will refer to the gypboard by name. If we change the name of the gypboard, we should change it in the construction object. 
# 
# But there may be many constructions objects using the gypboard. Now we will have to change it in all those construction objects. Sounds painfull. 
# 
# Let us try this with an example:

# <codecell>

interiorwall = idf.newidfobject("CONSTRUCTION", Name="Interior Wall",
                 Outside_Layer="G01a 19mm gypsum board",
                 Layer_2="Shiny new material object",
                 Layer_3="G01a 19mm gypsum board")
print(interiorwall)

# <markdowncell>

# to rename gypboard and have that name change in all the places we call modeleditor.rename(idf, key, oldname, newname)

# <codecell>

modeleditor.rename(idf, "MATERIAL", "G01a 19mm gypsum board", "peanut butter")

# <codecell>

print(interiorwall)

# <markdowncell>

# Now we have "peanut butter" everywhere. At least where we need it. Let us look at the entir idf file, just to be sure

# <codecell>

idf.printidf()

# <headingcell level=2>

# Zone area and volume

# <markdowncell>

# The idf file has zones with surfaces and windows. It is easy to get the attributes of the surfaces and windows as we have seen in the tutorial. Let us review this once more:

# <codecell>

from eppy import modeleditor 
from eppy.modeleditor import IDF
iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "../eppy/resources/idffiles/V_7_2/box.idf"
# IDF.setiddname(iddfile)

# <codecell>

idf = IDF(fname1)

# <codecell>

surfaces = idf.idfobjects["BuildingSurface:Detailed".upper()]
surface = surfaces[0]
print("area = %s" % (surface.area, ))
print("tilt = %s" % (surface.tilt, ))
print("azimuth = %s" % (surface.azimuth, ))

# <markdowncell>

# Can we do the same for zones ? 
# 
# Not yet .. not yet. Not in this version on eppy
# 
# But we can still get the area and volume of the zone

# <codecell>

zones = idf.idfobjects["ZONE"]
zone = zones[0]
area = modeleditor.zonearea(idf, zone.Name)
volume = modeleditor.zonevolume(idf, zone.Name)
print("zone area = %s" % (area, ))
print("zone volume = %s" % (volume, ))

# <markdowncell>

# Not as slick, but still pretty easy

# <markdowncell>

# Some notes on the zone area calculation:
# 
# - area is calculated by summing up all the areas of the floor surfaces
# - if there are no floors, then the sum of ceilings and roof is taken as zone area
# - if there are no floors, ceilings or roof, we are out of luck. The function returns 0

