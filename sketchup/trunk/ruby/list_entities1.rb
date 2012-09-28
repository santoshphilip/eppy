#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.
require "Sketchup.rb" #Make sure this ruby file is loaded
model=Sketchup.active_model             # point to the active model

#selection_set = model.selection # get the selected entities
selection_set = model.active_entities # get the all entities

# Put initial message into output string - count of entities selected
smess = sprintf("%d entities in selection set\n\n", selection_set.length)

# Loop through the entities in the selection set.
# "each" will execute the code in braces {} for each entity in the list.
# |entity| gives the loop a variable in which to store each entity as the loop is processed.
selection_set.each {|entity|
    puts entity.class
    a = 5
     if entity.class == Sketchup::Face
    #if entity.class == Sketchup::Edge
      #puts entity.class
      allverts = entity.vertices
      allverts.each {|vert|
        snippet3 = sprintf('%s', vert.position)
        puts snippet3
        }
    end
 }

#Display the full message
# UI.messagebox(smess)
