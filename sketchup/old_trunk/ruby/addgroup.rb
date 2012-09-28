# this is the original code from 
# <http://suwiki.org/suwiki/index.php?title=Ruby_Tutorial_-_Accessing_Entities>

# add group

model=Sketchup.active_model             # point to the active model

selection_set = model.active_entities # get the selected entities

# Put initial message into output string - count of entities selected
smess = sprintf("%d entities in selection set\n\n", selection_set.length)

# Loop through the entities in the selection set.
# "each" will execute the code in braces {} for each entity in the list.
# |entity| gives the loop a variable in which to store each entity as the loop is processed.
mentities = []

selection_set.each {|entity|
    if entity.class == Sketchup::Group
      group = model.entities.add_group
      gentities = entity.explode
      gentities.each{|gentity|
        mentities += [gentity]
        # if gentity.class == Sketchup::Face
        #   group.entities.add_group gentity
        # end
        #puts gentity.class
      #model.entities.add_group(gentities)
      #group = model.entities.add_group
      group.entities.add_group gentities
      }
    end
}

#model.entities.add_group(mentities)

selection_set.each{|entity|
    puts entity.class
  }
#Display the full message
 # UI.messagebox(smess)