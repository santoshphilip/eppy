# Copyright (c) 2012 Santosh Phillip

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

"""routines for comfort calcs for Kuykendall hall, University of Hawaii."""
import mycsv

def indexloop(i, lst):
    """massage the loop index so that loops"""
    try:
        item = lst[i]
        return i
    except IndexError, e:
        return i - len(lst)
        
def avg_around(i, lst, upspan=0, downspan=0):
    """return the average going upspan items before i and downspan items after i
    lst = [1,2,3,4,5], i=1, upspan=2, downspan=2 returns sum[5,1,2,3,4]/5"""
    before = [lst[indexloop(j, lst)] for j in range(i-upspan, i)]
    after = [lst[indexloop(j, lst)] for j in range(i, i+downspan+1)]
    sublst = before + after
    return sum(sublst)/float(len(sublst))
    
def comfort_optimal(tavg, celsius=True):
    """optimal comfort temperature
    comfort = 17.8 + 0.31 * tavg"""
    return 17.8 + 0.31 * tavg
    
def comfort_upper(tavg, celsius=True, upperinc=3.5, windinc=0):
    """upper limit of comfort for 80perc limit"""
    return comfort_optimal(tavg, celsius=celsius) + upperinc + windinc
    
def comfort_lower(tavg, celsius=True, lowerdec=3.5):
    """lower limit of comfort for 80perc limit"""
    return comfort_optimal(tavg, celsius=celsius) - lowerdec    
    
def comfort(tavg, limit=80, windinc=0, celsius=True):
    """upper 80% acceptable limit of comfort
    comfort = 0.31 * tavg + 21.3 + windinc"""
    if limit == 80:
        return 0.31 * tavg + 21.3 + windinc
        
def comfortET(etavg, limit=80, windinc=0, celsius=True):
    """upper 80% acceptable limit of comfort using ET*
    comfort = 18.9 + 0.255 * etavg + 3.5 + windinc"""
    comfort = 18.9 + 0.255 * etavg + 3.5 + windinc
    return comfort        
    
    
def comfort_matrix(mat, comfunc, upspan=360, downspan=360, 
                            limit=80, windinc=0, celsius=True):
    """do the comfort calcs on several rows"""
    tavgs = []
    dbts = [dbt for dbt, tzone in mat]
    tzones = [tzone for dbt, tzone in mat]
    for i in range(len(mat)):
        tavgs.append(avg_around(i, dbts, upspan=upspan,
                                    downspan=downspan))
    comfs = [comfunc(t, limit=limit, windinc=windinc, 
                                    celsius=celsius) for t in tavgs]
    diffs = [c-t for t, c in zip(tzones, comfs)]
    outmat = [dbts] + [tzones] + [tavgs] + [comfs] + [diffs]
    return mycsv.transpose2d(outmat)
    
def comfort_matrix1(mat, comfunc, upspan=360, downspan=360, 
                            windinc=0, celsius=True):
    """do the comfort calcs on several rows"""
    tavgs = []
    dbts = [dbt for dbt, tzone in mat]
    tzones = [tzone for dbt, tzone in mat]
    for i in range(len(mat)):
        tavgs.append(avg_around(i, dbts, upspan=upspan,
                                    downspan=downspan))
    comfs = [comfunc(t, windinc=windinc, 
                                    celsius=celsius) for t in tavgs]
    diffs = [c-t for t, c in zip(tzones, comfs)]
    outmat = [dbts] + [tzones] + [tavgs] + [comfs] + [diffs]
    return mycsv.transpose2d(outmat)    
    
def comfort_matrix2(mat, comfunc, upspan=360, downspan=360, 
                         celsius=True):
    """do the comfort calcs on several rows"""
    tavgs = []
    dbts = [dbt for dbt, tzone in mat]
    tzones = [tzone for dbt, tzone in mat]
    for i in range(len(mat)):
        tavgs.append(avg_around(i, dbts, upspan=upspan,
                                    downspan=downspan))
    comfs = [comfunc(t, celsius=celsius) for t in tavgs]
    diffs = [c-t for t, c in zip(tzones, comfs)]
    outmat = [dbts] + [tzones] + [tavgs] + [comfs] + [diffs]
    return mycsv.transpose2d(outmat)        