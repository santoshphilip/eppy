
model=Sketchup.active_model       
selection_set = model.active_entities 

sel = model.selection

sel.each {|entity|
  puts entity
}

