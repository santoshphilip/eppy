#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.

# to get materials out of sketchup


require "Sketchup.rb" #Make sure this ruby file is loaded
model=Sketchup.active_model             # point to the active model

selection_set = model.active_entities # get the all entities

mats = model.materials
mats.each{|m| 
  puts m.name
}


puts 'loop through materials'

selection_set.each {|entity|
  if entity.class == Sketchup::Face
    face = entity
    col = face.material
    if col
      puts col, col.name, col.color
    else
      puts col, 'no material'
    end
  end
  }
  

