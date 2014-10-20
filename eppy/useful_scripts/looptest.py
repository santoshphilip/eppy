
# coding: utf-8

# In[1]:

import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../../'
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

idf1.saveas("bl.idf")


# In[5]:

keys = idf1.idfobjects.keys()


# In[6]:

from eppy.bunch_subclass import BadEPFieldError
for key in keys:
    for idfobject in idf1.idfobjects[key]:
        try:
            name = idfobject.Name
            print name
            if name.find(":") != -1:
                #print key, name
                newname = name.replace(':', '_') 
                #print idfobject[0]
                modeleditor.rename(idf1, key, name, newname)
        except BadEPFieldError , e:
            pass
        


# In[7]:

idf1.saveas("b2.idf")


# In[34]:

idf1.idfobjects['ZONE']


# In[10]:

"asfdsaljfa;slfj".find(':')


# In[ ]:



