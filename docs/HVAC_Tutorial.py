# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# HVAC Loops

# <headingcell level=2>

# Conceptual Introduction to HVAC Loops

# <markdowncell>

# Eppy builds threee kinds of loops for the energyplus idf file:
# 
# 1. Plant Loops
# 2. Condensor Loops
# 3. Air Loops
# 
# All loops have two halves:
# 
# 1. Supply side
# 2. Demand Side
# 
# The supply side provides the energy to the demand side that needs the energy. So the end-nodes on the supply side connect to the end-nodes on the demand side. 
# 
# The loop is made up of branches connected to each other. A single branch can lead to multiple branches through a **splitter** component. Multiple branches can lead to a single branch through a **mixer** component. 
# 
# Each branch is made up of components connected in series (in a line)
# 
# Eppy starts off by building the shape or topology of the loop by connecting the branches in the right order. The braches themselves have a single component in them, that is just a place holder. Usually it is a pipe component. In an air loop it would be a duct component.
# 
# The shape of the loop for the supply or demand side is quite simple. 
# 
# It can be described in the following manner for the supply side
# 
# - The supply side starts single branch leads to a splitter
# - The splitter leads to multiple branches
# - these multiple branches come back and join in a mixer
# - the mixer leads to a single branch that becomes end of the suppply side
# 
# For the demand side we have:
# 
# - The demand side starts single branch leads to a splitter
# - The splitter leads to multiple branches
# - these multiple branches come back and join in a mixer
# - the mixer leads to a single branch that becomes end of the demand side
# 
# The two ends of the supply side connect to the two ends of the demand side.

# <markdowncell>

# Diagramtically the the two sides of the loop will look like this::

# <rawcell>

#     Supply Side:
#     ------------
#                     -> branch1 -> 
#     start_branch   --> branch2 --> end_branch
#                     -> branch3 ->
#     Demand Side:
#     ------------
#     
#                       -> d_branch1 -> 
#     d_start_branch   --> d_branch2 --> d_end_branch
#                       -> d_branch3 ->
#     

# <markdowncell>

# 
# In eppy you could embody this is a list

# <codecell>

supplyside = ['start_brandh',   [  'branch1',   'branch2',   'branch3'],   'end_branch']
demandside = ['d_start_brandh', ['d_branch1', 'd_branch2', 'd_branch3'], 'd_end_branch']

# <markdowncell>

# Eppy will build the build the shape/topology of the loop using the two lists above. Each branch will have a placeholder component, like a pipe or a duct::

# <rawcell>

#     
#     branch1 = --duct--

# <markdowncell>

# Now we will have to replace the placeholder with the real components that make up the loop. For instance, branch1 should really have a pre-heat coil leading to a supply fan leading to a cooling coil leading to a heating coil::

# <rawcell>

#     
#     new_branch = pre-heatcoil -> supplyfan -> coolingcoil -> heatingcoil

# <markdowncell>

# Eppy lets you build a new branch and you can replace branch1 with new_branch
# 
# In this manner we can build up the entire loop with the right components, once the initial toplogy is right

# <headingcell level=2>

# Building a Plant loops

# <markdowncell>

# Eppy can build up the topology of a plant loop using single pipes in a branch.  Once we do that the simple branch in the loop we have built can be replaced with a more complex branch.
# 
# Let us try this out ans see how it works.

# <headingcell level=3>

# Building the topology of the loop

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

# <codecell>

from eppy.modeleditor import IDF
from eppy import hvacbuilder

from io import StringIO
iddfile = "../eppy/resources/iddfiles/Energy+V7_0_0_036.idd"
IDF.setiddname(iddfile)

# <codecell>

# make the topology of the loop
idf = IDF(StringIO('')) # makes an empty idf file in memory with no file name
loopname = "p_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4'] # demand side of the loop
hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
idf.saveas("hhh1.idf")

# <markdowncell>

# We have made plant loop and saved it as hhh1.idf.  
# Now let us look at what the loop looks like.  

# <headingcell level=3>

# Diagram of the loop

# <markdowncell>

# Let us use the script "eppy/useful_scripts/loopdiagrams.py" to draw this diagram

# <markdowncell>

# See [Generating a Loop Diagram](useful_scripts.html#loopdiagram-py) page for details on how to do this

# <markdowncell>

# Below is the diagram for this simple loop
# 
# *Note: the supply and demnd sides are not connected in the diagram, but shown seperately for clarity*

# <codecell>

from eppy import ex_inits #no need to know this code, it just shows the image below
for_images = ex_inits
for_images.display_png(for_images.plantloop1) # display the image below

# <headingcell level=3>

# Modifying the topology of the loop

# <markdowncell>

# Let us make a new branch and replace the exisiting branch 
# 
# The existing branch name is "sb0" and it contains a single pipe component sb0_pipe.
# 
# Let us replace it with a branch that has a chiller that is connected to a pipe which is turn connected to another pipe. So the connections in the new branch would look like "chiller-> pipe1->pipe2"

# <codecell>

# make a new branch chiller->pipe1-> pipe2

# make a new pipe component
pipe1 = idf.newidfobject("PIPE:ADIABATIC", 'np1')

# make a new chiller
chiller = idf.newidfobject("Chiller:Electric".upper(), 'Central_Chiller')

# make another pipe component
pipe2 = idf.newidfobject("PIPE:ADIABATIC", 'np2')

# get the loop we are trying to modify
loop = idf.getobject('PLANTLOOP', 'p_loop') # args are (key, name)
# get the branch we are trying to modify
branch = idf.getobject('BRANCH', 'sb0') # args are (key, name)
listofcomponents = [chiller, pipe1, pipe2] # the new components are connected in this order

newbr = hvacbuilder.replacebranch(idf, loop, branch, listofcomponents, fluid='Water')
# in "loop"
# this replaces the components in "branch" with the components in "listofcomponents"

idf.saveas("hhh_new.idf")

# <markdowncell>

# We have saved this as  file "hhh_new.idf".  
# Let us draw the diagram of this file.  (run this from eppy/eppy folder)

# <rawcell>

# python ex_loopdiagram.py hhh_new.idf

# <codecell>

from eppy import ex_inits #no need to know this code, it just shows the image below
for_images = ex_inits
for_images.display_png(for_images.plantloop2) # display the image below

# <markdowncell>

# This diagram shows the new components in the branch

# <headingcell level=3>

# Traversing the loop

# <markdowncell>

# It would be nice to move through the loop using functions "nextnode()" and "prevnode()"
# 
# Eppy indeed has such functions
# 
# Let us try to traverse the loop above. 

# <codecell>

# to traverse the loop we are going to call some functions ex_loopdiagrams.py, 
# the program that draws the loop diagrams.
from eppy import ex_loopdiagram
fname = 'hhh_new.idf'
iddfile = '../eppy/resources/iddfiles/Energy+V8_0_0.idd'
edges = ex_loopdiagram.getedges(fname, iddfile)
# edges are the lines that draw the nodes in the loop. 
# The term comes from graph theory in mathematics

# <markdowncell>

# The above code gets us the edges of the loop diagram. Once we have the edges, we can traverse through the diagram. Let us start with the "Central_Chiller" and work our way down.

# <codecell>

from eppy import walk_hvac
firstnode = "Central_Chiller"
nextnodes = walk_hvac.nextnode(edges, firstnode)
print(nextnodes)

# <codecell>

nextnodes = walk_hvac.nextnode(edges, nextnodes[0])
print(nextnodes)

# <codecell>

nextnodes = walk_hvac.nextnode(edges, nextnodes[0])
print(nextnodes)

# <codecell>

nextnodes = walk_hvac.nextnode(edges, nextnodes[0])
print(nextnodes)

# <markdowncell>

# This leads us to three components -> ['sb1_pipe', 'sb2_pipe', 'sb3_pipe']. Let us follow one of them

# <codecell>

nextnodes = walk_hvac.nextnode(edges, nextnodes[0])
print(nextnodes)

# <codecell>

nextnodes = walk_hvac.nextnode(edges, nextnodes[0])
print(nextnodes)

# <codecell>

nextnodes = walk_hvac.nextnode(edges, nextnodes[0])
print(nextnodes)

# <markdowncell>

# We have reached the end of this branch. There are no more components. 
# 
# We can follow this in reverse using the function prevnode()

# <codecell>

lastnode = 'sb4_pipe'
prevnodes = walk_hvac.prevnode(edges, lastnode)
print(prevnodes)

# <codecell>

prevnodes = walk_hvac.prevnode(edges, prevnodes[0])
print(prevnodes)

# <codecell>

prevnodes = walk_hvac.prevnode(edges, prevnodes[0])
print(prevnodes)

# <codecell>

prevnodes = walk_hvac.prevnode(edges, prevnodes[0])
print(prevnodes)

# <codecell>

prevnodes = walk_hvac.prevnode(edges, prevnodes[0])
print(prevnodes)

# <codecell>

prevnodes = walk_hvac.prevnode(edges, prevnodes[0])
print(prevnodes)

# <codecell>

prevnodes = walk_hvac.prevnode(edges, prevnodes[0])
print(prevnodes)

# <markdowncell>

# All the way to where the loop ends

# <headingcell level=2>

# Building a Condensor loop

# <markdowncell>

# We build the condensor loop the same way we built the plant loop. Pipes are put as place holders for the components. Let us build a new idf file with just a condensor loop in it.

# <codecell>

condensorloop_idf = IDF(StringIO('')) 
loopname = "c_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4'] # demand side
theloop = hvacbuilder.makecondenserloop(condensorloop_idf, loopname, sloop, dloop)
condensorloop_idf.saveas("c_loop.idf")

# <markdowncell>

# Again, just as we did in the plant loop, we can change the components of the loop, by replacing the branchs and traverse the loop using the functions nextnode() and prevnode()

# <headingcell level=2>

# Building an Air Loop

# <markdowncell>

# Building an air loop is similar to the plant and condensor loop. The difference is that instead of pipes , we have ducts as placeholder components. The other difference is that we have zones on the demand side.

# <codecell>

airloop_idf = IDF(StringIO('')) 
loopname = "a_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
dloop = ['zone1', 'zone2', 'zone3'] # zones on the demand side
hvacbuilder.makeairloop(airloop_idf, loopname, sloop, dloop)
airloop_idf.saveas("a_loop.idf")

# <markdowncell>

# Again, just as we did in the plant and condensor loop, we can change the components of the loop, by replacing the branchs and traverse the loop using the functions nextnode() and prevnode()

