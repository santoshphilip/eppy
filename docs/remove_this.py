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
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"

iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
import pdb; pdb.set_trace()
IDF.setiddname(iddfile)
# idf1 = IDF(fname1)




# - now let us open a file from the disk differently
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
fhandle = open(fname1, 'r') # open the file for reading and assign it a file handle
import pdb; pdb.set_trace()
idf_fromfilehandle = IDF(fhandle) # initialize the IDF object with the file handle

idf_fromfilehandle.printidf()

