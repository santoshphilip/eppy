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
## VERSION: 0.003
## Last updated 21 Apr 2004

import sys
import getopt
import os
import string
import user

sys.path.append(user.home+'/Library/PythonFiles')
import mylib1,mylib2,mylib3
import eplus2,time

import cPickle

def nocomment(st,com):
    """
    just like the comment in python.
    removes any text after the phrase 'com'
    """
    ls=st.splitlines()
    for i in range(len(ls)):
        el=ls[i]
        pt=el.find(com)
        if pt!=-1:
            ls[i]=el[:pt]
    return '\n'.join(ls)

def get_nocom_vars(st):
    """
    input 'st' which is the Energy+.idd file as a string
    returns (st1,st2,lss)
    st1= with all the ! comments striped
    st2= strips all comments - both the '!' and '\\'
    lss= nested list of all the variables in Energy+.idd file
    """
    nocom=nocomment(st,'!')# remove '!' comments
    st1=nocom
    nocom1=nocomment(st1,'\\')# remove '\' comments
    st1=nocom
    st2=nocom1
    ls=string.split(st2,';')
    lss=[]
    
    # break the .idd file into a nested list
    #=======================================
    for el in ls:
        item=string.split(el,',')
        lss.append(item)
    for i in range(0,len(lss)):
        for j in range(0,len(lss[i])):
            lss[i][j]=lss[i][j].strip()
    if len(lss)>1:lss.pop(-1)
    #=======================================    
    
    #st1 has the '\' comments --- looks like I don't use this
    #lss is the .idd file as a nested list
    return (st1,st2,lss)

def removeblanklines(st):
    """
    removeblanklines(st)
    returns the string after
    remove blank lines in 'st'
    """
    linesep=mylib3.getlinesep(st)
    ls=st.split(linesep)
    lss=[]
    for el in ls:
        ell=el.strip()
        if ell!='':
            lss.append(el)
    st1=linesep.join(lss)
    return st1


def extractidddata(fname,debug=False):
    """
    extracts all the needed information out of the idd file
    if debug is True, it generates a series of text files.
    Each text file is incrementally different. You can do a diff 
    see what the change is
    """
    from StringIO import StringIO
    if isinstance(fname, (file, StringIO)):
        st = fname.read()
    else:
        st=mylib2.readfile(fname)
    (nocom,nocom1,blocklst)=get_nocom_vars(st)
    
    
    st=nocom
    st1=removeblanklines(st)
    if debug:
        mylib1.writeStr2File('nocom2.txt',st1)
    
    
    #find the groups and the start object of the group
    #find all the group strings
    groupls=[]
    ls=st1.splitlines()
    for el in ls:
        lss=el.split()
        if lss[0].upper()=='\\group'.upper():
            groupls.append(el)
    
    
    #find the var just after each item in groupls
    groupstart=[]
    for i in range(len(groupls)):
        ii=ls.index(groupls[i])
        groupstart.append([ls[ii],ls[ii+1]])
    
    #remove the group commentline
    for el in groupls:
        ls.remove(el)
    
    if debug:
        st1='\n'.join(ls)
        mylib1.writeStr2File('nocom3.txt',st1)
    
    #strip each line
    for i in range(len(ls)):
        ls[i]=ls[i].strip()
    
    if debug:
        st1='\n'.join(ls)
        mylib1.writeStr2File('nocom4.txt',st1)
    
    #ensure that each line is a comment or variable
    #find lines that don't start with a comment
    #if this line has a comment in it
    #   then move the comment to a new line below
    lss=[]
    for i in range(len(ls)):
        #find lines that don't start with a comment
        if ls[i][0]!='\\':
            #if this line has a comment in it
            pt=ls[i].find('\\')
            if pt!=-1:
                #then move the comment to a new line below
                lss.append(ls[i][:pt].strip())
                lss.append(ls[i][pt:].strip())
            else:
                lss.append(ls[i])
        else:
            lss.append(ls[i])
    
    
    ls=lss[:]
    if debug:
        st1='\n'.join(ls)
        mylib1.writeStr2File('nocom5.txt',st1)
    
    #need to make sure that each line has only one variable - as in WindowGlassSpectralData,
    lss=[]
    for el in ls:
        # if the line is not a comment
        if el[0]!='\\':
            #test for more than one var
            ll=el.split(',')
            if ll[-1]=='':
                tmp=ll.pop()
            for elm in ll:
                if elm[-1]==';':
                    lss.append(elm.strip())
                else:
                    lss.append((elm+',').strip())
        else:
            lss.append(el)
    
    ls_debug=ls[:] # needed for the next debug - 'nocom7.txt'
    ls=lss[:]
    if debug:
        st1='\n'.join(ls)
        mylib1.writeStr2File('nocom6.txt',st1)
    
    if debug:
        #need to make sure that each line has only one variable - as in WindowGlassSpectralData,
        #this is same as above.
        # but the variables are put in without the ';' and ','
        #so we can do a diff between 'nocom7.txt' and 'nocom8.txt'. Should be identical
        lss_debug=[]
        for el in ls_debug:
            # if the line is not a comment
            if el[0]!='\\':
                #test for more than one var
                ll=el.split(',')
                if ll[-1]=='':
                    tmp=ll.pop()
                for elm in ll:
                    if elm[-1]==';':
                        lss_debug.append(elm[:-1].strip())
                    else:
                        lss_debug.append((elm).strip())
            else:
                lss_debug.append(el)
        
        ls_debug=lss_debug[:]
        st1='\n'.join(ls_debug)
        mylib1.writeStr2File('nocom7.txt',st1)
    
    
    #replace each var with '=====var======'
    #join into a string,
    #split using '=====var====='
    for i in range(len(lss)):
        #if the line is not a comment
        if lss[i][0]!='\\':
            lss[i]='=====var====='
    
    st2='\n'.join(lss)
    lss=st2.split('=====var=====\n')
    lss.pop(0) # the above split generates an extra item at start
    
    if debug:
        fname='nocom8.txt'
        f=open(fname,'wb')
        k=0
        for i in range(len(blocklst)):
            for j in range(len(blocklst[i])):
                f.write(blocklst[i][j]+'\n')
                f.write(lss[k])
                k=k+1
        
        f.close()
    
    #map the structure of the comments -(this is 'lss' now) to 
    #the structure of blocklst - blocklst is a nested list
    #make lss a similar nested list
    k=0
    lst=[]
    for i in range(len(blocklst)):
        lst.append([])
        for j in range(len(blocklst[i])):
            lst[i].append(lss[k])
            k=k+1
    
    
    if debug:
        fname='nocom9.txt'
        f=open(fname,'wb')
        k=0
        for i in range(len(blocklst)):
            for j in range(len(blocklst[i])):
                f.write(blocklst[i][j]+'\n')
                f.write(lst[i][j])
                k=k+1
        
        f.close()
            
    
    
    #break up multiple line comment so that it is a list
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            lst[i][j]=lst[i][j].splitlines()
            # remove the '\'
            for k in range(len(lst[i][j])):
                lst[i][j][k]=lst[i][j][k][1:]
    commlst=lst
    
    
    #copied with minor modifications from readidd2_2.py -- which has been erased ha !
    c=lst
    lss=[]
    for i in range(0,len(c)):
        ls=[]
        for j in range(0,len(c[i])):
            it=c[i][j]
            dt={}
            for el in it:
                if len(el.split())==0:
                    break
                dt[el.split()[0].lower()]=[]
            
            for el in it:
                if len(el.split())==0:
                    break
                dt[el.split()[0].lower()].append(string.join(el.split()[1:]))
                                
            
            ls.append(dt)
        
        lss.append(ls)
    commdct=lss
    
    return blocklst,commlst,commdct


def getobjectref(blocklst,commdct):
    """
    makes a dictionary of object-lists
    each item in the dictionary points to a list of tuples
    the tuple is (objectname, fieldindex)
    """
    objlst_dct={}
    for eli in commdct:
        for elj in eli:
            if elj.has_key('object-list'):
                objlist=elj['object-list'][0]
                objlst_dct[objlist]=[] 
    
    for objlist in objlst_dct.keys():
        for i in range(len(commdct)):
            for j in range(len(commdct[i])):
                if commdct[i][j].has_key('reference'):
                    for ref in commdct[i][j]['reference']:
                        if ref==objlist:                        
                            objlst_dct[objlist].append((blocklst[i][0],j))
    return objlst_dct

        
# blocklst,commlst,commdct=extractidddata('Energy+.idd_old')
# dct=getobjectref(blocklst,commdct)
# 
# for el in dct.keys():
#   print el
#   print dct[el]
# fname='./Energy+.idd'
# debug=True
# blocklst,commlst,commdct=extractidddata(fname,debug)

# blocklst,commlst,commdct=extractidddata('Energy+.idd_old')


#mylib2.cpickledump((blocklst,lss),'block_comm.pik')
#this file is identical to the one produced by readidd2_2.py
