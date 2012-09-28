# this is the original code from 
# <http://suwiki.org/suwiki/index.php?title=Ruby_Tutorial_-_Accessing_Entities>

# loop through groups
# explode each group
# undo the explode

def explodeforundo(model, entity)
  if entity.class == Sketchup::Group
    puts entity
    model.start_operation "explode"
    entity.explode
    model.commit_operation
  end  
end

model=Sketchup.active_model             

selection_set = model.active_entities

allentities = []
selection_set.each{|entity|
  allentities.push(entity)
}

allentities.each {|entity|
  explodeforundo(model, entity)
  Sketchup.undo
}

