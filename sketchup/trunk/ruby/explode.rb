# this is the original code from 
# <http://suwiki.org/suwiki/index.php?title=Ruby_Tutorial_-_Accessing_Entities>

# loop through groups
# explode each group

model=Sketchup.active_model             # point to the active model

selection_set = model.active_entities # get the selected entities

# Put initial message into output string - count of entities selected
smess = sprintf("%d entities in selection set\n\n", selection_set.length)

# Loop through the entities in the selection set.
# "each" will execute the code in braces {} for each entity in the list.
# |entity| gives the loop a variable in which to store each entity as the loop is processed.
selection_set.each {|entity|
    # Get the ID and class for each entity
    sent = sprintf("ID: %s Type: %s", entity.entityID, entity.class)
    # Add the string for this entity to the total message
    smess = smess + sent + "\n" # append message to string
    puts smess
    if entity.class == Sketchup::Group:
      entity.entities.each {|groupentitiy| 
        sent = sprintf("ID: %s Type: %s", groupentitiy.entityID, groupentitiy.class)
        smess = smess + sent + "\n"
        puts smess
      }
    end
}

puts sprintf('%s just before explode %s', '*' * 10, '*' * 10)

# collect groups
allgroups = []
selection_set.each{|entity|
  if entity.class == Sketchup::Group
    allgroups += [entity]
  end
}

allgroups.each{|agroup|
  agroup.explode
} 

selection_set.each {|entity|
    # Get the ID and class for each entity
    sent = sprintf("ID: %s Type: %s", entity.entityID, entity.class)
    puts sent
}

#Display the full message
 # UI.messagebox(smess)