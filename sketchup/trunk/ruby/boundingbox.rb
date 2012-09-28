
model=Sketchup.active_model       
selection_set = model.selection
if selection_set.length == 0
  selection_set = model.active_entities   
end

selection_set.each {|entity|
  if entity.class == Sketchup::Group
    bounds = entity.bounds
    puts bounds
    puts '    ', bounds.max, bounds.min
  end
}

