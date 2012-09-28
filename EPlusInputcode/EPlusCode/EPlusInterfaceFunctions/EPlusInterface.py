#!/usr/bin/env python

## EPlusInterface (EPI) - An interface for EnergyPlus
## Copyright (C) 2004 Santosh Philip
##
## This file is part of EPlusInterface.
## 
## EPlusInterface is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## EPlusInterface is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with EPlusInterface; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
##
##
## Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
## santosh_philip AT yahoo DOT com
## Please send all bug reports, enhancement proposals, questions and comments to that address.
## 
## VERSION: 0.004

#open any file VERSION: 0.002
#edit entry
#using cPickle


import sys
import getopt
import os
import string
import user
import copy

import eplusdata
import parse_idd
import slashcomment

__author__ = 'Santosh Philip <santosh_philip AT Yahoo DOT com>'
__license__ = 'GNU General Public License'
__version__ = '0.003'


sys.path.append(user.home+'/Library/PythonFiles')
import mylib1,mylib2,mylib3
import tui1

def objselection(obj):
	"""
	used where a field refers to an object-list
	This routine allows you to select an item from the list of references
	"""
	global data
	global block
	global commdct
	global objlst_dct
	ls=data.getrefs(objlst_dct[obj])
	DescrObjs=[]
	for el in ls:
		DescrObjs.append((el,el))
	
	Prompt='Select an Item'
	return tui1.RadioButtons(Prompt,DescrObjs)
		

def keyselection(thekeys):
	"""
	There is a choice of values that can fill this field
	keyselection(thekeys) allows you to make the selection
	"""
	DescrObjs=[]
	for el in thekeys['key']:
		DescrObjs.append((el,el))
	
	Prompt='hit a button'
	return tui1.RadioButtons(Prompt,DescrObjs)

def tuisavefile(filename):
	"""
	Save the Energyplus file
	"""
	global data
	Prompt='Would you like to save this file ?'
	Action = tui1.RadioButtons("Choose an action",( ("Save",1),("Save As",2),("Quit",3) ))
	if Action==3:
		return
	if Action==1:
		mylib1.writeStr2File(filename,`data`)
		return
	Prompt='Choose new file name:'
	filename=tui1.TextEntry(Prompt)
	mylib1.writeStr2File(filename,`data`)
	
def tuiopenfile():
	"""
	Open an Energyplus file
	"""
	Prompt='make a selection to open a file'
	result=tui1.FileDirChooser(Prompt,'f',('idf',))
	return result

def allobjects():
	"""
	Show all objects in the EnergyPlus file
	print the object type
	"""
	global data
	global block
	global commlst
	global commdct
	fullls=[]
	for el in data.dtls:
		if data.dt[el]!=[]:
			fullls.append(el)
	DescrObjs=[]
	for el in fullls:DescrObjs.append((el,el))
	DescrObjs.append(('-- Quit --','#up#'))
	
	Prompt='hit a button'
	stay=1
	while stay:
		sel=tui1.RadioButtons(Prompt,DescrObjs)
		if sel=='#up#':return
		thisobject(sel)
	#==================================

def thisobject(sel1):	
	"""
	Show all the instances of this object
	if it is an unique object (only one instance possible)
	then goto allfields
	"""
	global data
	global block
	global commlst
	global commdct
	seldt=data.dt[sel1]
	
	Prompt='hit a button for:'+sel1
	stay=1
	index=slashcomment.getobjectindex(block,sel1)
	a=slashcomment.slashcomment()
	keyshere=a.keyshere(commdct[index][0])
	while stay:
		if 'unique-object' in keyshere:
			allfields(sel1,0)
			return
		DescrObjs=[]
		for i in range(0,len(seldt)):
			DescrObjs.append((seldt[i][1],i))
		DescrObjs.append(('-- Go up in menu --','#up#'))
		sel2=tui1.RadioButtons(Prompt,DescrObjs)
		if sel2=='#up#':return
		allfields(sel1,sel2)
	#==================================

def allfields(sel1,sel2):
	"""
	Show all fields of this object
	"""
	global data
	global block
	global commlst
	global commdct
	seldt=data.dt[sel1]
	blocknames=[]
	for el in data.dtls:
		blocknames.append(el)
	
	name=data.dt[sel1][sel2][0]
	print 'finding  '+name.upper()
	i=blocknames.index(name.upper())
	comm=commlst[i]
	

	Prompt='hit a button :' 
	stay=1
	while stay:
		item=data.dt[sel1][sel2]
		DescrObjs=[]
		for i in range(0,len(item)):
			if len(comm[i])==0:
				comment=''
			else:
				comment=comm[i][0]
			DescrObjs.append((item[i] + ' => ' + comment,i))
		DescrObjs.append(('-- Go up in menu --','#up#'))
		sel3=tui1.RadioButtons(Prompt,DescrObjs)
		if sel3=='#up#':return
		thisfield(comm,sel1,sel2,sel3)
	#==================================

def thisfield(comm,sel1,sel2,sel3):
	"""
	Show this field
	with Slash comments
	"""
	global dirty
	global data
	global block
	global commdct
	keeplooping=True
	while keeplooping:
		seldt=data.dt[sel1]
		item=data.dt[sel1][sel2][sel3]
		print item
		print '-'*len(item)
		print 'This is:'
		for el in comm[sel3]:
			print '\t'+el
		DescrObjs=[]
		DescrObjs.append(('Edit this value','#edit#'))
		DescrObjs.append(('-- Go up in menu --','#up#'))
		Prompt='hit a button :' 
		sel4=tui1.RadioButtons(Prompt,DescrObjs)
		if sel4=='#up#':return
		if sel4=='#edit#':
			keeplooping=editfield(sel1,sel2,sel3)
			
	#==================================

def editfield(sel1,sel2,sel3):
	"""
	Edit this field
	different types of field entries(key, object-list, real) 
	will result in diffferent interactions.
	"""
	global dirty
	global data
	global block
	global commdct
	print sel1
	index=slashcomment.getobjectindex(block,sel1)
	#-----key-----
	a=slashcomment.slashcomment()
	keyshere=a.keyshere(commdct[index][sel3])
	if 'key' in keyshere:
		#go to keyselection routine
		val=keyselection(commdct[index][sel3])
	elif 'object-list' in keyshere:
		val=objselection(commdct[index][sel3]['object-list'][0])
	elif 'autosizable' in keyshere:
		# button for 1.autosize and 2.enter number
		DescrObjs=[]
		DescrObjs.append(('autosize','autosize'))
		DescrObjs.append(('Enter a number','#EnterNumber#'))
		Prompt='Select an Option :' 
		autosizeselection=tui1.RadioButtons(Prompt,DescrObjs)
		if autosizeselection=='autosize':
			val=autosizeselection
		else:
			Prompt='Enter new Value'
			val=tui1.TextEntry(Prompt)		
	else:
		Prompt='Enter new Value'
		val=tui1.TextEntry(Prompt)
	try:
		slashcomment.checkVal(val,commdct[index][sel3])
		data.dt[sel1][sel2][sel3]=val
		dirty=True
		keeplooping=False
		return keeplooping
	except "anError",descr:
		print descr
		tmp=raw_input('hit RETURN to continue')
		keeplooping=True
		return keeplooping


def showlicense():
	"""
	print the preamble to the GPL license
	This function is called when using TUI as the interface
	"""
	print """

EPlusInterface (EPI) - An interface for EnergyPlus
Copyright (C) 2004 Santosh Philip

EPlusInterface is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

EPlusInterface is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with EPlusInterface; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 


Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
santosh_philip AT yahoo DOT com
Please send all bug reports, enhancement proposals, questions and comments to that address.

VERSION: 0.003

	"""
	print '='*35

def main():
	"""
	da main
	"""
	global data
	global block
	global commlst
	global commdct
	global objlst_dct
	showlicense()
	print 'It is a little slow here parsing data from the Energy.idd file'
	print 'Please wait .... '
	dictfile=fileloc+'Energy+V6_0.idd'
	
	block,commlst,commdct=parse_idd.extractidddata(dictfile)
	objlst_dct=parse_idd.getobjectref(block,commdct)
	tmp=raw_input('hit RETURN to continue')

	fname1=tuiopenfile()
	if fname1==-1:return

	
	theidd=eplusdata.idd(block,2)
	data=eplusdata.eplusdata(theidd,fname1)
		
	allobjects()
	global dirty
	if dirty:
		#save the file
		tuisavefile(fname1)
		#mylib1.writeStr2File('saved.idf',`data`)
		
#global variables
fileloc='../../../iddfiles/'
global dirty
global data
global block
global commlst
global commdct
global objlst_dct
dirty=False
if __name__ == "__main__":
    main()
