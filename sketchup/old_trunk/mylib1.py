# Copyright (c) 2012 Santosh Philip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

# """checktext - Check that a text file has macintosh-style newlines"""

import string

def getworkingdir():
	fp=open('workingdir','r')
	return fp.read()
	
def justfilename(pathname):
	pt=string.rfind(pathname,':')
	return pathname[pt+1:]

def pathnameup(pathname):
	pt=string.rfind(pathname,':')
	return pathname[:pt]

def readfileasmac(fname):
#	retun the contents of file fname 
#	if it is a dos file convert it to Mac
	fp=open(fname,'rb')
	try:
		data = fp.read()
	except MemoryError:
		print 'Sorry, file is too big.'
		return
	if len(data) == 0:
		print 'File is empty.'
		return
	number_cr = string.count(data, '\r')
	number_lf = string.count(data, '\n')
	#if number_cr == number_lf == 0:
		#EasyDialogs.Message('File contains no lines.')
	if number_cr == 0:
		#EasyDialogs.Message('File has unix-style line endings')
		data=string.replace(data,'\n','\r') #make it a mac file
	#elif number_lf == 0:
		#EasyDialogs.Message('File has mac-style line endings')
	elif number_cr == number_lf:
		#EasyDialogs.Message('File probably has MSDOS-style line endings')
		data=string.replace(data,'\n','') #make it a mac file
	#else:
		#EasyDialogs.Message('File has no recognizable line endings (binary file?)')
	#f=open('Macintosh HD:Python 2.0:santosfiles:gumbhere1','w')
	#f.write(data)
	fp.close()
	return data
	


def readworkingdirfile(fname):
#	retun the contents of file fname 
#	if it is a dos file convert it to Mac
	fp=open(getworkingdir()+fname,'rb')
	try:
		data = fp.read()
	except MemoryError:
		print 'Sorry, file is too big.'
		return
	if len(data) == 0:
		print 'File is empty.'
		return
	number_cr = string.count(data, '\r')
	number_lf = string.count(data, '\n')
	#if number_cr == number_lf == 0:
		#EasyDialogs.Message('File contains no lines.')
	if number_cr == 0:
		#EasyDialogs.Message('File has unix-style line endings')
		data=string.replace(data,'\n','\r') #make it a mac file
	#elif number_lf == 0:
		#EasyDialogs.Message('File has mac-style line endings')
	elif number_cr == number_lf:
		#EasyDialogs.Message('File probably has MSDOS-style line endings')
		data=string.replace(data,'\n','') #make it a mac file
	#else:
		#EasyDialogs.Message('File has no recognizable line endings (binary file?)')
	#f=open('Macintosh HD:Python 2.0:santosfiles:gumbhere1','w')
	#f.write(data)
	fp.close()
	return data
	
def findnext(str,pointer,sub): 
#	find the next iinstance of sub in s
#	starting from the location pointer
	"find the next instance of sub in s starting from location pointer"
	cutstr=str[pointer:]
	findpoint=string.find(cutstr,sub)
	if findpoint==0 : #pointer is pointing to sub
		cutstr=cutstr[len(sub):]
		findpoint=string.find(cutstr,sub)+len(sub)
	if findpoint==-1 :
		return -1
	else:
		pointer=pointer+findpoint
		return pointer

def nextline(s,pt):
#	return a pointer to the next line 
#	in string s after location pt 
	"starting at location pt return the location of the next line"
	if s[pt:pt+1]=='\r': #if the pointer is at a return, just move by 1
		return pt+1
	if findnext(s,pt,'\r')==-1:
		return -1
	else:
		return findnext(s,pt,'\r')+1+1 # extra +1 is for dos system
	
def getword(s,n): 
#	return nth word in the string s
#	first word is indexed as 0
	"return the nth word in the string s"
	sp=string.split(s)
	if n>len(sp)-1:
		return ''
	return sp[n]

def numlines(s):
	return string.count(s, '\r') 

def printlines(s,first,last=-1):
	if (last==-1)or(last>numlines(s)):
		last=numlines(s)
	pt1=0
	for i in range(first,last+1):
		pt2=nextline(s,pt1)
		if pt1==-1:
			return
		print s[pt1:pt2-1]
		pt1=pt2

def getlineright(s,pt):
	pt1=nextline(s,pt)
	return s[pt:pt1-1]	

def getlineleft(s,pt):
	creturn='\r'
	prev_lnbreak=string.rfind(s[:pt],creturn)
#	return s[prev_lnbreak+1:pt] changed from mac version
	return s[prev_lnbreak+2:pt]

def getthisline(s,pt):
	return getlineleft(s,pt)+getlineright(s,pt)



def transformRectList(outerL):
#	transform  a rectanglular list
#	[[1,2,3,4],[5,6,7,8]] becomes
#	[[1, 5], [2, 6], [3, 7], [4, 8]]
#	or
#	[[1, 2, 3, 4], [5, 6, 7, 8], [8, 10, 11, 12]] becomes
#	[[1, 5, 8], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
#	will crash with just [1,2,3]
	jmax=len(outerL)
	imax=len(outerL[0])
	newL=[]
	innerL=[]
	L2=[]
	for i in range(0,imax):
		for j in range(0,jmax):
			innerL=outerL[j]
			L2=L2+[innerL[i]]
		newL=newL+[L2]
		L2=[]
	return newL

def RectList2str(outerL):
#	puts a rectangular list in a string
#	with tabs in between columns
#	will crash if list is single dimensional
	aa=''
	tab='	'
	cr='\r'
	for i in range(0,len(outerL)):
		for j in range(0,len(outerL[0])):
			innerL=outerL[i]
			aa=aa+innerL[j]+tab
		aa=aa+cr
	return aa

def writeStr2File(pathname,s):
#	writes a string to file
	fname=pathname
	f=open(fname,'wb')
	f.write(s)
	f.close()
	
def indexRectList(TheList):
#	index rectanglular List
	for i in range(0,len(TheList)):
		TheList[i][0:0]=[str(i)]
	return TheList	

def readfile(pathname):
#	retrun the data in the file
	f=open(pathname,'rb')
	data=f.read()
	f.close()	
	return data

def addRectList(s,r):
	for i in range(0,len(s)):
		s[i].extend(r[i])
	return s
	

def copyList(b):
	a=[]
	a.extend(b)
	return a

def stripinner(outer):
	a=[]
	for i in range(0,len(outer)):
		for j in range(0,len(outer[i])):
			inner=outer[i]
			a=a+[inner[j]]
	b=[]
	for i in range(0,len(a)):
		c=[a[i]]
		b=b+[c]
	return b
