from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# coding: utf-8

# In[1]:

import sys

# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = "../../"
sys.path.append(pathnameto_eppy)

from eppy import modeleditor
from eppy.modeleditor import IDF

iddfile = "../../eppy/resources/iddfiles/Energy+V8_1_0.idd"
fname1 = "../../eppy/resources/idffiles/V8_1_0/Boiler.idf"


# In[2]:

IDF.setiddname(iddfile)
idf1 = IDF(fname1)


# In[3]:

idf1 = IDF(fname1)


# In[4]:

idf1.saveas("bl_original.idf")


# In[5]:

keys = list(idf1.idfobjects.keys())


# In[6]:

# rename object name with a colon and any field that refers to that name
from eppy.bunch_subclass import BadEPFieldError

renamednames = []
for key in keys:
    for idfobject in idf1.idfobjects[key]:
        try:
            name = idfobject.Name
            if name.find(":") != -1:
                renamednames.append(name)
                newname = name.replace(":", "__")
                # print "%s, %s, %s" %  (key, name, newname)
                modeleditor.rename(idf1, key, name, newname)
        except BadEPFieldError as e:
            pass


# In[7]:

idf1.saveas("bl_renamed_names.idf")

# rename any fields that have a colon
for key in keys:
    for idfobject in idf1.idfobjects[key]:
        objectfields = idfobject["obj"]
        # idfobject['obj'] is unocumented functionality
        # to get fields of an object as a list
        for i, field in enumerate(objectfields[1:]):
            try:
                if field in renamednames:
                    if field.find(":") != -1:
                        newfield = field.replace(":", "__")
                        objectfields[i + 1] = newfield
            except AttributeError as e:
                # may be a number
                pass

idf1.saveas("bl_renamed_fields.idf")

# rename any field that is a node
for key in keys:
    for idfobject in idf1.idfobjects[key]:
        # idfobject['obj'] is unocumented functionality
        # to get fields of an object as a list
        objectfields = idfobject["obj"]
        # another undocumented functionality
        objectidds = idfobject["objidd"]
        for i, (field, f_idd) in enumerate(zip(objectfields[1:], objectidds[1:])):
            try:
                # print f_idd["field"][0]
                nodeinname = "Node" in f_idd["field"][0]
            except KeyError as e:
                # field may not be a key
                nodeinname = False
            if nodeinname:
                try:
                    # if field in renamednames:
                    if field.find(":") != -1:
                        newfield = field.replace(":", "__")
                        objectfields[i + 1] = newfield
                        # print f_idd["field"], field
                except AttributeError as e:
                    # may be a number
                    pass

idf1.saveas("bl_renamed_nodes.idf")


# to make the loop diagram do:
# python loopdiagram.py ../../eppy/resources/iddfiles/Energy+V8_1_0.idd bl_renamed_nodes.idf
