# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""some helper files"""

from string import ascii_letters, digits

def onlylegalchar(name):
    """return only legal chars"""
    legalchar = ascii_letters + digits + ' '
    return ''.join([s for s in name[:] if s in legalchar])

def makefieldname(namefromidd):
    """made a field name that can be used by bunch"""
    newname = onlylegalchar(namefromidd)
    bunchname = newname.replace(' ', '_')
    return bunchname
    
def intinlist(lst):
    """test if int in list"""
    for item in lst:
        try:
            item = int(item)
            return True
        except ValueError, e:
            pass
    return False
    
def replaceint(fname, replacewith='%s'):
    """replace int in lst"""
    words = fname.split()
    for i, word in enumerate(words):
        try:
            word = int(word)
            words[i] = '%s'
        except ValueError, e:
            pass
    return ' '.join(words)

def cleaniddfield(acomm):
    """make all the keys lower case"""
    for key in acomm.keys():
        val = acomm[key]
        acomm[key.lower()] = val
    for key in acomm.keys():
        val = acomm[key]
        if key != key.lower():
            acomm.pop(key)
    return acomm
    
def cleancommdct(commdct):
    """make all keys in commdct lower case"""
    return [[cleaniddfield(fcomm) for fcomm in comm] for comm in commdct]    
    