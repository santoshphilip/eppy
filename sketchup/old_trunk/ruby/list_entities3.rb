#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.
require "Sketchup.rb" #Make sure this ruby file is loaded
model=Sketchup.active_model             # point to the active model

selection_set = model.active_entities # get the all entities
aFile = File.new("/Users/santosh/Documents/coolshadowprojects/sketchupstuff/energypluscode/a.txt", 'w')

puts model
materials = model.materials  
puts materials
materials.each{|mat|
  puts mat
  }


selection_set.each {|entity|
  a = 5
  puts entity.class
  if entity.class == Sketchup::Face
    face = entity
    col = face.material
    if col
      puts 'material ', col.name
    else
      puts 'no material'
    end
    allloops = face.loops
    allloops.each {|lp|
      if lp.outer?
        snippet3 = sprintf('%s outer', lp )
        aFile.puts('--------------------')
        puts snippet3
        allvertex = lp.vertices
        allvertex.each{|vert|
          pts = vert.position.to_a
          snippet4 = sprintf('%s, %s, %s', pts[0], pts[1], pts[2] )
          puts snippet4
          aFile.puts(snippet4)
          }
      else
        snippet3 = sprintf('%s inner', lp )
        puts snippet3
      end
      }
  end
  }
  

aFile.close()