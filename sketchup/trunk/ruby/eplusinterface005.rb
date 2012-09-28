#!/usr/bin/env ruby

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
## VERSION: 0.005

# Santosh's working notes:
# dumps the some sketchup geometry data to a file
# for each face it dumps the points3d
# this is data is used to make an energyplus file
#--------
# innerloop is fixed
# works with groups
# explode the group , process it and then undo the explode
# output angle that the face makes with the horizontal


require "Sketchup.rb" 

def writeout(aFile, astring)
  puts astring
  aFile.puts(astring)
end

def explodeforundo(model, entity)
  if entity.class == Sketchup::Group
    model.start_operation "explode"
    exploded = entity.explode
    model.commit_operation
  end  
  return exploded
end

def toradians(ang)
  # return 180 / Math::PI * ang
  return 180 / 3.14159265358979 * ang
end

def surface_direction(face)
  vect = face.normal
  hvector = Geom::Vector3d.new(0, 0, 1)
  ang = hvector.angle_between vect
  return ang
end

def dumpface(aFile, face, i)
  #face = entity
  if face.class != Sketchup::Face
    return i
  end
  tab = '    '
  facestring = sprintf('face:%s', i)
  writeout(aFile, facestring)
  layerstring = sprintf('%slayer:%s', tab*1, face.layer.name)
  writeout(aFile, layerstring)
  allloops = face.loops
  parent = i
  allloops.each {|lp|
    if not lp.outer?
      i += 1
      facestring = sprintf('face:%s', i)
      writeout(aFile, facestring)
      writeout(aFile, layerstring)
    end  
    allvertex = lp.vertices
    pointstring = sprintf('%spoints:%s', tab*1, allvertex.length)
    writeout(aFile, pointstring)
    allvertex.each{|vert|
      pts = vert.position.to_a
      allpointsstring = sprintf('%s%s %s %s', tab*2, pts[0], pts[1], pts[2] )
      writeout(aFile, allpointsstring)
      }
    norm = face.normal
    normstring = sprintf('%snormal:%s %s %s', tab*1, norm[0], norm[1], norm[2])
    writeout(aFile, normstring)
    facedirectionstring = sprintf('%ssurfacedirection:%s', tab*1, toradians(surface_direction(face)))
    writeout(aFile, facedirectionstring)
    if face.material
      materialstring = sprintf('%smaterial:%s', tab, face.material.name)
    else
      materialstring = sprintf('%smaterial:%s', tab, 'None')
    end
    writeout(aFile, materialstring)
      if lp.outer?
        innerstring = sprintf('%sparent:%s', tab*1, 'None')
      else
        innerstring = sprintf('%sparent:%s', tab*1, parent)
      end
    writeout(aFile, innerstring)
      }
  i += 1
  return i
end

def extractdata
  model=Sketchup.active_model             

  selection_set = model.active_entities 
  fname = UI.savepanel('Save this file', '', 'eplusinterface.txt')
  if fname == nil
    return
  end 
  aFile = File.new(fname, 'w')
  sel = model.selection
  sel.clear # may not be necessary 

  allentities = []
  selection_set.each{|entity|
    allentities.push(entity)
  }

  i = 1
  allentities.each {|entity|
    if entity.class == Sketchup::Face
      i = dumpface(aFile, entity, i)
    else 
      if entity.class == Sketchup::Group
        exploded = explodeforundo(model, entity)
        exploded.each {|groupentitiy| 
          i = dumpface(aFile, groupentitiy, i)
        }
      Sketchup.undo  
      end
    end
    }
  
  aFile.close()
end

if( not file_loaded?("eplusinterface005.rb") )
    add_separator_to_menu("Plugins")
    UI.menu("Plugins").add_item("eplusinterface V0.005") { extractdata }
end
#-----------------------------------------------------------------------------
file_loaded("eplusinterface005.rb")

