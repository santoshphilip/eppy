
model=Sketchup.active_model       
selection_set = model.active_entities 

selection_set.each {|entity|
}

result = UI.openpanel 
puts 'openpanel', result

result = UI.savepanel
puts 'savepanel', result
