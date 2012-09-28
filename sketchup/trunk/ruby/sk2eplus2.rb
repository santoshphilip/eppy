#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.

# dumps the some sketchup geometry data to a file
# for each face it dumps the points3d
# this is data is used to make an energyplus file
#--------
# innerloop is fixed


require "Sketchup.rb" #Make sure this ruby file is loaded
model=Sketchup.active_model             # point to the active model

selection_set = model.active_entities # get the all entities
aFile = File.new("/Users/santosh/Documents/coolshadowprojects/sketchupstuff/energypluscode_old1/e.txt", 'w')

def writeout(aFile, astring)
  puts astring
  aFile.puts(astring)
end

i = 1
tab = '    '
selection_set.each {|entity|
  if entity.class == Sketchup::Face
    face = entity
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
  end
  }
  

aFile.close()