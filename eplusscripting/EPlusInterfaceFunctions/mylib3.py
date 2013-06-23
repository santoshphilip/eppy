# EPlusInterface (EPI) - An interface for EnergyPlus
# Copyright (C) 2004 Santosh Philip

# This file is part of EPlusInterface.
# 
# EPlusInterface is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EPlusInterface is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EPlusInterface; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 


# Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
# santosh_philip AT yahoo DOT com
# Please send all bug reports, enhancement proposals, questions and comments to that address.
# 
# VERSION: 0.001


import mylib1,mylib2
import string


def transpose2D(ls):
#transpose a 2D array. actually a list like
#[[a,b],[c,d],[e,f]]->[[a,c,e],[b,d,f]]
	outer=[]
	for i in range(len(ls[0])):
		inner=[]
		for j in range(len(ls)):
			inner=inner+[ls[j][i]]
		outer=outer+[inner]
	return outer



def getfilelist(flist,lsep):
#flist is s text file with a list of file names
#the file names are returned in a list
	st=mylib1.readfile(flist)
	st=st.rstrip()
	ls=st.split(lsep)
	return ls
	

dossep='\r\n'
macsep='\r'
unixsep='\n'

def getlinesep(st):
#returns the line seperators used in the string st
#mac is '\r'
#dos is '\r\n'
#unix is '\n'
	lsep=None
	if len(st)==0:lsep=None
	r=string.count(st,'\r')
	n=string.count(st,'\n')
	if n==r==0:lsep=None
	if n==0:lsep='\r'
	if r==0:lsep='\n'
	if n==r:lsep='\r\n'
	return lsep

#closefloat
def closefloat(f1,f2,closeness=0.01):
	#Check if the two floating points are close to each other
	dif=abs(f1-f2)
	return dif<closeness

