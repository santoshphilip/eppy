#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.
require "Sketchup.rb" #Make sure this ruby file is loaded
model=Sketchup.active_model             # point to the active model

selection_set = model.selection # get the selected entities
#selection_set = model.active_entities # get the all entities

# Put initial message into output string - count of entities selected
smess = sprintf("%d entities in selection set\n\n", selection_set.length)

# Loop through the entities in the selection set.
# "each" will execute the code in braces {} for each entity in the list.
# |entity| gives the loop a variable in which to store each entity as the loop is processed.
selection_set.each {|entity|
    # Get the ID and class for each entity
    snippet = sprintf("ID: %s Type: %s | %s", entity.entityID, entity.class, entity.edges)
    theedges = entity.edges
    theedges.each {|anedge|
      verts = anedge.vertices
      verts.each {|vert|
        snippet2= sprintf("%s/n", vert.position)
        puts snippet2
        }
      
      
      snippet1 = sprintf("%s\n", anedge)
      # puts snippet1
      }
    # puts snippet
    sent = snippet
    # Add the string for this entity to the total message
    smess = smess + sent + "\n" # append message to string
}

#Display the full message
# UI.messagebox(smess)
