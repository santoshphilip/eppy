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
## VERSION: 0.001

import sys
import getopt
import os
import string
import user

sys.path.append(user.home+'/Library/PythonFiles')
import mylib1,mylib2,mylib3
import eplus2,time
import parse_idd

# block,commlst,commdct=parse_idd.extractidddata('./Energy+.idd')
# 
# cm=commdct[3]
# cmm=cm[0]

def printcdt(i):
	for el in comm[i]:
		print el



# commtype=['field', 'note', 'required-field', 'units', 'ip-units', 'minimum', 
# 'minimum>', 'maximum', 'maximum<', 'default', 'autosizable', 'type', 
# 'key', 'object-list', 'reference', 
# 'memo', 'unique-object', 'required-object', 'min-fields', 
# 'obsolete', 'extensible', 
# 'group']


		

class slashcomment:
	def __init__(self):
		self.allkeys=['field', 'note', 'required-field', 'units', 'ip-units', 'minimum', 
			'minimum>', 'maximum', 'maximum<', 'default', 'autosizable', 'type', 
			'key', 'object-list', 'reference', 
			'memo', 'unique-object', 'required-object', 'min-fields', 
			'obsolete', 'extensible', 
			'group']
		self.commentnow={
			'default': ['4'], 
			'maximum': ['6'], 
			'required-field': [''], 
			'note': [
				'Number in hour: validity 1 to 6: 4 suggested', 
				'Should be evenly divisible into 60', 
				'Specifying 6 as maximum as higher values may cause instability.'], 
			'field': ['Time Step in Hour'], 
			'minimum': ['1'], 
			'type': ['integer']}
	
	def keyshere(self,cmm):
		ls=[]
		for el in self.allkeys:
			if cmm.has_key(el):
				ls.append(el)
		
		return ls
	


def checkNumber(num):
	"""
	check if num is a number 
	and raise an error
	"""
	try:
		return float(num)
	except:
		raise "anError", "%s is not a real"%(num) 

def checkInteger(num):
	"""
	check if num is an integer 
	and raise an error
	"""
	try:
		return int(num)
	except:
		raise "anError", "%s is not an integer"%(num) 
		

def getobjectindex(blocklst,object):
	"""
	getobjectindex(blocklst,'SOLUTION ALGORITHM')
	returns the index of the object
	corresponding slashcomments can be retrived using this index
	"""
	ls=[]
	for el in blocklst:
		ls.append(el[0].upper())
	return ls.index(object.upper())



def getrepeats():
	"""
	no docs - 
	I used it for debugging
	to find how many items had 'field' in more than one line
	"""
	key='reference'
	for i in range(len(commdct)):
		for j in range(len(commdct[i])):
			try:
				val=commdct[i][j][key]
				if len(val)>1:
					print commdct[i][j]
					print i,j,'====',len(val)
			except:
				pass
		
	
def checkVal(val,commentdct=None):
	"""
	raise an error if the value does not fall into 
	the description of commentdct
	"""
	# check autosizable
	# check type - real, integer
	# check min max min> max<
	# check key
	# check object-list
	
	
	error="anError"
	#check on autosize - return if value is autosize
	if commentdct.has_key('autosizable'):
		print 'autosizeable'
		if val=='autosize':
			return
	
	#check type - initially check number
	keyval=getkeyval('type',commentdct)
	if keyval!=None:
		if keyval.upper()=='real'.upper():
			val=checkNumber(val)
	if keyval!=None:
		if keyval.upper()=='integer'.upper():
			val=checkInteger(val)
	
	# check min max min> max<
	keyval=getkeyval('minimum',commentdct)
	if keyval!=None:
		if not val>=keyval:
			raise error, "value should be greater than or equal to %s"%(keyval)
	keyval=getkeyval('minimum>',commentdct)
	if keyval!=None:
		if not val>keyval:
			raise error, "value should be greater than %s"%(keyval)
	keyval=getkeyval('maximum',commentdct)
	if keyval!=None:
		if not val<=keyval:
			raise error, "value should be less than or equal to %s"%(keyval)
	keyval=getkeyval('maximum<',commentdct)
	if keyval!=None:
		if not val<keyval:
			raise error, "value should be less than%s"%(keyval)
	
	# check key
	keyval=getkeyval('key',commentdct)
	if keyval!=None:
		try:
			keyval.index(val)
		except:
			raise "anError", "%s is not in list" %(val,)
		



def getkeyval(key,commentdct):
	"""
	returns the value of the key
	commentdct can be {'default': ['4'], 'maximum': ['6'], 'required-field': [''],
				'note':['this is', ' a note']}
	now key='default' will return the number 4
	key='note' will return 'this is\\n a note'
	"""
	#--------minimum, minimum>, maximum, maximum<, min-fields----------
	#returns the number or None
	if key.upper() in [
				'minimum'.upper(),
				'minimum>'.upper(),
				'maximum'.upper(),
				'maximum<'.upper(),
				'min-fields'.upper()]:
		try:
			val=commentdct[key][0]
			return float(val)
		except KeyError:
			return None
	#--------field, note, units, ip-units, 
	#        default, type, object-list, memo----------
	#returns the value or None
	if key.upper() in [
				'field'.upper(),
				'note'.upper(),
				'units'.upper(),
				'ip-units'.upper(),
				'default'.upper(),
				'type'.upper(),
				'object-list'.upper(),
				'memo'.upper()]:
		try:
			val=commentdct[key]
			st=''
			for el in val:
				st=st+el+'\n'
			st=st[:-1]
		except KeyError:
			return None
		return st
	#--------required-field, autosizable, unique-object, required-object----------
	#returns True or False
	if key.upper()in [
				'required-field'.upper(), 
				'autosizable'.upper(),
				'unique-object'.upper(),
				'required-object'.upper()]:
		return commentdct.has_key(key)
	#--------key, reference----------
	#returns a list
	if key.upper()in [
				'key'.upper(),
				'reference'.upper()]:
		try:
			return commentdct[key]
		except KeyError:
			return None




#key var -> to run getkeyval
# i=7
# j=0
# print block[i], block[i][j]
# cm=commdct[i]
# key='memo'
# print getkeyval(key,cm[j])

# block,commlst,commdct=parse_idd.extractidddata('./Energy+.idd')
# commentdct={
# 	'units': ['deltaC'], 
# 	'field': ['Temperature Convergence Tolerance Value'], 
# 	'minimum>': ['0.0'], 
# 	'type': ['real'], 'default': ['.4']}
# 
# 
# 
# checkVal(-5,commentdct)
# 
# 
# try:
# 	checkVal(-2,commentdct)	
# except "anError",d:
# 	print d
# 
# 
# try:
# 	checkNumber('a')	
# except "anError",d:
# 	print d
# 	
