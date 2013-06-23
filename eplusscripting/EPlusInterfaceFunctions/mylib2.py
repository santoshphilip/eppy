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

import os,pickle,cPickle
import string
import mylib1


ret='\r\n'

def readfile(filename):
    f=open(filename,'rb')
    data=f.read()
    f.close()
    return data

def printlist(ls):
    for n in range(0,len(ls)):
        print ls[n]

def printdict(d):
    dl=d.keys()
    dl.sort()
    for i in range(0,len(dl)):
        print dl[i],d[dl[i]]

def tabfile2list(fname):
    #dat=mylib1.readfileasmac(fname)
    #data=string.strip(dat)
    data=mylib1.readfileasmac(fname)
    #data=data[:-2]#remove the last return
    alist=string.split(data,'\r')#since I read it as a mac file
    blist=string.split(alist[1],'\t')

    clist=[]
    for n in range(0,len(alist)):
        ilist=string.split(alist[n],'\t')
        clist=clist+[ilist]
    cclist=clist[:-1]#the last element is turning out to be empty
    return cclist

def tabstr2list(data):
    alist=string.split(data,os.linesep)
    blist=string.split(alist[1],'\t')

    clist=[]
    for n in range(0,len(alist)):
        ilist=string.split(alist[n],'\t')
        clist=clist+[ilist]
    cclist=clist[:-1]
      #the last element is turning out to be empty
      #this is because the string ends with a os.linesep
    return cclist

def list2doe(l):
    eq=''
    str=''
    lenj=len(l)
    leni=len(l[0])
    for i in range(0,leni-1):
        for j in range(0,lenj):
            if j==0:
                str=str+l[j][i+1]+eq+l[j][0]+ret
            else:
                str=str+l[j][0]+eq+l[j][i+1]+ret
        str=str+ret
    return str

def tabfile2doefile(tabfile,doefile):
    alist=tabfile2list(tabfile)
    str=list2doe(alist)
    mylib1.writeStr2File(doefile,str)

def tabstr2doestr(st):
    alist=tabstr2list(st)
    str=list2doe(alist)
    return str

def makedoedict(str1):
    blocklist=string.split(str1,'..')
    blocklist=blocklist[:-1]#remove empty item after last '..'
    blockdict={}
    belongsdict={}
    for n in range(0,len(blocklist)):
        blocklist[n]=blocklist[n].strip()
        linelist=string.split(blocklist[n],os.linesep)
        aline=linelist[0]
        alinelist=string.split(aline,'=')
        name=alinelist[0].strip()
        aline=linelist[1]
        alinelist=string.split(aline,'=')
        belongs=alinelist[-1].strip()
        theblock=blocklist[n]+os.linesep+'..'+os.linesep+os.linesep
            #put the '..' back in the block
        blockdict[name]=theblock
        belongsdict[name]=belongs
    return [blockdict,belongsdict]

def makedoetree(d,b):
    dl=d.keys()
    bl=b.keys()
    dl.sort()
    bl.sort()
    
    #make space dict
    doesnot='DOES NOT'
    lst=[]
    for n in range(0,len(bl)):
        if b[bl[n]]==doesnot:#belong
            lst=lst+[bl[n]]
    
    doedict={}    
    for n in range(0,len(lst))   :
        #print lst[n]
        doedict[lst[n]]={}
    lv1list=doedict.keys()
    lv1list.sort()
    
    #make wall dict
    #for each space
    for i in range(0,len(lv1list)):
        walllist=[]
        dict=doedict[lv1list[i]]
        #loop thru the entire bl dictonary and list the ones that belong into walllist
        for n in range(0,len(bl)):
            if b[bl[n]]==lv1list[i]:
                walllist=walllist+[bl[n]]
        #put walllist into dict
        for j in range(0,len(walllist)):
            dict[walllist[j]]={}
    
    #make window dict
    #for each space
    for i in range(0,len(lv1list)):
        dict1=doedict[lv1list[i]]
        #for each wall
        walllist=dict1.keys()
        walllist.sort()
        for j in range(0,len(walllist)):
            windlist=[]
            dict2=dict1[walllist[j]]
           #loop thru the entire bl dictonary and list the ones that belong into windlist
            for n in range(0,len(bl)):
                if b[bl[n]]==walllist[j]:
                    windlist=windlist+[bl[n]]
            #put walllist into dict
            for k in range(0,len(windlist)):
                dict2[windlist[k]]={}
    return doedict
                
def tree2doe(str1):
    retstuff=makedoedict(str1)
    ddict= makedoetree(retstuff[0],retstuff[1])
    d=retstuff[0]
    retstuff[1] ={}# don't need it anymore

    str1=''#just re-using it
    L1list=ddict.keys()
    L1list.sort()
    for i in range(0,len(L1list)):
        str1=str1+d[L1list[i]]
        L2list=ddict[L1list[i]].keys()
        L2list.sort()
        for j in range(0,len(L2list)):
            str1=str1+d[L2list[j]]
            L3list=ddict[L1list[i]][L2list[j]].keys()
            L3list.sort()
            for k in range(0,len(L3list)):
                str1=str1+d[L3list[k]]
    return str1

def Mtabstr2doestr(st1):
    seperator='$=================='
    ls=string.split(st1,seperator)

    #this removes all the tabs that excel
    #puts after the seperator and before the next line
    for n in range(0,len(ls)):
        ls[n]=string.lstrip(ls[n])
    st2=''
    for n in range(0,len(ls)):
        alist=tabstr2list(ls[n])
        st2=st2+list2doe(alist)

    lss=string.split(st2,'..')
    mylib1.writeStr2File('forfinal.txt',st2)#for debugging
    print len(lss)


    st3=tree2doe(st2)
    lsss=string.split(st3,'..')
    print len(lsss)
    return st3

def getoneblock(st,start,end):
#get the block bounded by start and end
#doesn't work for multiple blocks
    ls=string.split(st,start)
    st=ls[-1]
    ls=string.split(st,end)
    st=ls[0]
    return st

def doestr2tabstr(st,kword):
    ls=string.split(st,'..')
    del st
    #strip junk put .. back
    for n in range(0,len(ls)):
        ls[n]=string.strip(ls[n])
        ls[n]=ls[n]+os.linesep+'..'+os.linesep
    ls.pop()

    lblock=[]
    for n in range(0,len(ls)):
        linels=string.split(ls[n],os.linesep)
        firstline=linels[0]
        assignls=string.split(firstline,'=')
        keyword=string.strip(assignls[-1])
        if keyword==kword:
            lblock=lblock+[ls[n]]
            #print firstline

    #get all val
    lval=[]
    for n in range(0,len(lblock)):
        block=lblock[n]
        linel=string.split(block,os.linesep)
        lvalin=[]
        for k in range(0,len(linel)):
            line=linel[k]
            assignl=string.split(line,'=')
            if k==0:
                lvalin=lvalin+[assignl[0]]
            else:
                if assignl[-1]=='..':
                    assignl[-1]='.'
                lvalin=lvalin+[assignl[-1]]
        lvalin.pop()
        lval=lval+[lvalin]

    #get keywords
    kwordl=[]
    block=lblock[0]
    linel=string.split(block,os.linesep)
    for k in range(0,len(linel)):
        line=linel[k]
        assignl=string.split(line,'=')
        if k==0:
            kword='= '+string.strip(assignl[1])
        else:
            if assignl[0]=='..':
                assignl[0]='.'
            else:
                assignl[0]=assignl[0]+'='
            kword=string.strip(assignl[0])       
        kwordl=kwordl+[kword]
    kwordl.pop()
    
    st=''
    for n in range(0,len(kwordl)):
        linest=''
        linest=linest+kwordl[n]
        for k in range(0,len(lval)):
            linest=linest+'\t'+lval[k][n]
        st=st+linest+os.linesep

    return st

def myreplace(s,f,r):
    "in string s replace all occurences of f with r"
    alist=string.split(s,f)
    new_s=string.join(alist,r)
    return new_s

def fslicebefore(s,sub):
    "Return the slice starting at sub in string s"
    f=string.find(s,sub)
    return s[f:]

def fsliceafter(s,sub):
    "Return the slice after at sub in string s"
    f=string.find(s,sub)
    return s[f+len(sub):]

def pickleload(fname):
    "same as pickle.load(f).takes filename as parameter"
    f=open(fname,'rb')
    return pickle.load(f)

def pickledump(o,fname):
    "same as pickle.dump(o,f).takes filename as parameter"
    f=open(fname,'wb')
    pickle.dump(o,f)

def cpickleload(fname):
    "same as pickle.load(f).takes filename as parameter"
    f=open(fname,'rb')
    return cPickle.load(f)

def cpickledump(o,fname):
    "same as pickle.dump(o,f).takes filename as parameter"
    f=open(fname,'wb')
    cPickle.dump(o,f)
