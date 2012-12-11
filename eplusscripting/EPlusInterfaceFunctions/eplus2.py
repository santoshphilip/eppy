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

import mylib1,mylib2,mylib3,string

class eplusdict:
	"""
	use this when you want to use a dictionary
	but want to maintain the order of the items.
	There is a alist that keeps the order
	"""
	adict={}
	alist=[]
	def __init__(self,dct=None,lst=None):
		if dct==None:
			self.adict={}
		else:
			self.adict=dct
		if lst==None:
			self.alist=[]
		else:
			self.alist=lst
	
	def add(self,name,content):
		"""
		you can replace an existing value with this.
		Dictionary values are entered as lists:
		{key1:[val1,val2,val3],key2:[val4,val8]}
		if a key already exists, the value is added 
		to the list rather than replacing the existing list
		"""
		if not self.adict.has_key(name):
			self.adict[name]=[]
		self.adict[name].append(content)
		self.alist.append(name)
	
	def remove(self,name):
		del self.adict[name]
		self.alist.remove(name)
		
# 	def update(self,name,content):
# 		if not(self.adict.has_key(name)):
# 			raise ValueError,'%s does not exists in the ordereddict' %(`name`,)
# 		self.adict[name]=content
	
	
class ordereddict:
	"""
	use this when you want to use a dictionary
	but want to maintain the order of the items.
	There is a alist that keeps the order
	"""
	adict={}
	alist=[]
	def __init__(self,dct=None,lst=None):
		if dct==None:
			self.adict={}
		else:
			self.adict=dct
		if lst==None:
			self.alist=[]
		else:
			self.alist=lst
	
	def add(self,name,content,warn=1):
		"""
		you can replace an existing value with this
		just keep warn=0
		"""
		if warn:
			if self.adict.has_key(name):
				raise ValueError,'%s already exists in the ordereddict' %(`name`,)
		self.adict[name]=content
		try:
			#in case you are replacing an existing value
			self.alist.remove(name)
		except:
			pass		

		self.alist.append(name)
	
	def remove(self,name):
		del self.adict[name]
		self.alist.remove(name)
		
	def update(self,name,content):
		if not(self.adict.has_key(name)):
			raise ValueError,'%s does not exists in the ordereddict' %(`name`,)
		self.adict[name]=content

	def reverse(self):
		self.alist.reverse()

class eplusdict1(ordereddict):
	"""
	first cycle of extracting the dictionary from the .idd file
	"""
	linesep=''
	def __init__(self,st):
		linesep=mylib3.getlinesep(st)
		self.linesep=linesep
		nocom=nocomment(st)
		iddst=nocom.nocom.strip()
		st=self.removecommasemi(iddst)
		
		#b=eplus1.ordereddict()
		while st.find(';')!=-1:
			(command,this,rest)=self.commandthisrest(st)
			st=rest
			self.add(command,this)
		
		self.reverse()
	
	def removecommasemi(self,iddst):
		"""
		need to change , and ; from the comment(\) line
		replace , with . and ; with :
		"""
		slashcomment='\\'
		comma=','
		dot='.'
		semi=';'
		colon=':'
		linesep=self.linesep
		ls=iddst.split(linesep)  
		for i in range(len(ls)):
			a=ls[i]
			if a.find(slashcomment)!=-1:
				als=a.split(slashcomment)
				tmp=als[-1]
				als[-1]=als[-1].replace(comma,dot)
				als[-1]=als[-1].replace(semi,colon)
				ls[i]=string.join(als,slashcomment)
		
		iddst=string.join(ls,linesep)
		return iddst

	def commandthisrest(self,st):
		"""
		st = 
		\gumby
		Lead Input;
		
		Simulation Data;
		
		\group Simulation Parameters
		
		VERSION,
			  \unique-object
		  A1 ; \field Version Identifier
			  \required-field
		
		BUILDING,
			   \unique-object
			   \required-object
			   \min-fields 6
		  A1 , \field Building Name
			   \required-field
			   \default NONE
		  N1 , \field North Axis
			   \note degrees from true North
			   \units deg
			   \type real
			   \default 0.0
			   ...
			   ...
		============================
		commandthisrest works backwords thru st
		In this case
		command = BUILDING
		this = 
		BUILDING,
			   \unique-object
			   \required-object
			   \min-fields 6
		  A1 , \field Building Name
			   \required-field
			   \default NONE
		  N1 , \field North Axis
			   \note degrees from true North
			   \units deg
			   \type real
			   \default 0.0
			   ...
			   ...
		rest =
		\gumby
		Lead Input;
		
		Simulation Data;
		
		\group Simulation Parameters
		
		VERSION,
			  \unique-object
		  A1 ; \field Version Identifier
			  \required-field
		"""
		linesep=self.linesep
		ls1=st.split(';')
		ls2=ls1[-2].split(',')
		ls3=ls2[0].split(linesep)
		command=ls3[-1].strip()
		
		st=string.join(ls3[:-1],linesep)
		ls=ls1[:-2]
		ls.append(st)
		rest=string.join(ls,';')
		
		ls2[0]=ls3[-1]
		ls2.append(ls1[-1])
		this=string.join(ls2,',')
		return command,this,rest
	
class eplusdict2(eplusdict1):
	"""
	second cycle of extracting the dictionary from the .idd file
	"""
	def __init__(self,st):
		eplusdict1.__init__(self,st)

	def parsecommand1(self,key):
		linesep=self.linesep
		st=self.adict[key]
		st=st+linesep
		ls=st.split(',')
		for i in range(len(ls)):
			ls[i]=ls[i].split(linesep)
		
		for i in range(len(ls)-1):
			ls[i]=ls[i]+(ls[i+1][:-1])
			ls[i+1]=[ls[i+1][-1]]
		
		ls.pop()
		
		bb=ordereddict()
		for el in ls:
			key=el[0]
			bb.add(el[0].strip(),el[1:])
		
		return bb


class nocomment:
	"""
	strips the commentts form the energyplus file
	"""
	def __init__(self,st):
		self.nocom=self.stripcomments(st)
	
	def __repr__(self):
		return self.nocom
		
	def sp(self,a):
		return string.split(a,'!')
			
	def striplinecomments(self,aline):
		ls=self.sp(aline)
		#range(8)=[0, 1, 2, 3, 4, 5, 6, 7]
		#range(1,8,2)=[1, 3, 5, 7]
		popthis=range(1,len(ls),2)

		popthis.reverse()
		for i in popthis:
			ls.pop(i)
		return string.join(ls,'')
	
	def stripcomments(self,text):
		lsep=mylib3.getlinesep(text)
		ls=string.split(text,lsep)
		for i in range(len(ls)):
			ls[i]=self.striplinecomments(ls[i])
		return string.join(ls,lsep)
		
	def tofile(self,filename):
		mylib2.str2file(filename,`self`)


class nocomment1:
	"""
	strips the commentts form the energyplus file
	"""
	def __init__(self,st,c='!'):
		self.cm=c 
		self.nocom=self.stripcomments(st)
	
	def __repr__(self):
		return self.nocom
		
	def sp(self,a):
		return string.split(a,self.cm)
			
	def striplinecomments(self,aline):
		ls=self.sp(aline)
		#range(8)=[0, 1, 2, 3, 4, 5, 6, 7]
		#range(1,8,2)=[1, 3, 5, 7]
		popthis=range(1,len(ls),2)

		popthis.reverse()
		for i in popthis:
			ls.pop(i)
		return string.join(ls,'')
	
	def stripcomments(self,text):
		lsep=mylib3.getlinesep(text)
		ls=string.split(text,lsep)
		for i in range(len(ls)):
			ls[i]=self.striplinecomments(ls[i])
		return string.join(ls,lsep)
		
	def tofile(self,filename):
		mylib2.str2file(filename,`self`)


class parseidd:
	"""
	Complete parser for .idd file
	works well
	simply too slow
	takes 30 minutes on my G3
	I may never use.
	Instead use just in time parsing for each command as needed
	"""
	finallst=[]
	commentbin=[]
	wordbin=[]
	
	def __init__(self,st):
		self.finallst=[]
		self.commentbin=[]
		self.wordbin=[]
		sep=';'
		linesep=mylib3.getlinesep(st)
		st='dummy;'+linesep+st#the first command is skipped
		(comment,word,rest)=self.commentwordrest(st,sep,linesep)
		self.commentbin.append(comment)
		self.wordbin.append(word)
		while rest!=None:
			rest=self.commasemifinish(rest,linesep)
		
	
	def commentwordrest(self,st,sep,linesep):
		ls=st.split(sep)
		comment=ls[-1]
		rest=string.join(ls[:-1],sep)
		ls1=rest.split(linesep)
		lastline=ls1[-1]
		sentence=lastline
		if sentence.find(',')!=-1:
			ls2=sentence.split(',')
			word=ls2[-1].strip()
			#remove the word
			ls2.pop()
			lastline=string.join(ls2,',')
			ls1[-1]=lastline
		else:
			word=sentence.strip()
			ls1.pop()#remove the sentence/lastline
		rest=string.join(ls1,linesep)
		return (comment,word,rest)
	
	def commasemifinish(self,st,linesep):
		#no comma no semiis = finish
		if st.find(',')==-1 and st.find(';')==-1:
			self.finallst.reverse()
			return None
		else:
			ls1=st.split(',')
			ls2=st.split(';')
			comma=len(ls1[-1])
			semi=len(ls2[-1])
			if semi>comma:
				return self.docommastuff(st,linesep)
			else:
				return self.dosemistuff(st,linesep)
	
	def dofinish(self):
		print 'finished'
		
	
		
	def docommastuff(self,st,linesep):
		sep=','
		(comment,word,rest)=self.commentwordrest(st,sep,linesep)
		self.commentbin.append(comment)
		self.wordbin.append(word)
		print word
		#self.commasemifinish(rest,linesep)
		return rest
	
	
	def dosemistuff(self,st,linesep):
		self.doblock()
		sep=';'
		(comment,word,rest)=self.commentwordrest(st,sep,linesep)
		self.commentbin.append(comment)
		self.wordbin.append(word)
		print word
		#self.commasemifinish(rest,linesep)
		return rest
	
	def doblock(self):
		self.commentbin.reverse()
		self.wordbin.reverse()
		d=ordereddict()
		for i in range(len(self.wordbin)):
			d.add(self.wordbin[i],self.commentbin[i])
		self.commentbin=[]
		self.wordbin=[]
		self.finallst.append(d)
		del d
	
