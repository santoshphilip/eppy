# calculate the area of faces


model=Sketchup.active_model       
selection_set = model.selection
if selection_set.length == 0
  selection_set = model.active_entities   
end


fcount = 1
selection_set.each {|entity|
  if entity.class == Sketchup::Face
    puts sprintf('face:%s', fcount)
    puts sprintf('    area:%s', entity.area)
    fcount += 1
  end
}