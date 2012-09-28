#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.

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
  return 180 / Math::PI * ang
end

def surfacedirection(face)
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
    facedirectionstring = sprintf('%ssurfacedirection:%s', tab*1, toradians(surfacedirection(face)))
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

model=Sketchup.active_model             

selection_set = model.active_entities 
aFile = File.new("/Users/santosh/Documents/coolshadowprojects/sketchupstuff/energypluscode/e.txt", 'w')
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