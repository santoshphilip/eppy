#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.

# to get materials out of sketchup


require "Sketchup.rb" #Make sure this ruby file is loaded
model=Sketchup.active_model             # point to the active model



selection_set = model.active_entities # get the all entities


puts '***********Layer for each face: ****************'  
selection_set.each {|entity|
  if entity.class == Sketchup::Face
    face = entity
    mess = sprintf('faceID: %s Layer Name: %s', face.entityID, face.layer.name)
    puts mess
  end
  }

puts '***********List of layers: ****************'  
  
layers = model.layers
layers.each{|layer|
  puts layer.name
  }
