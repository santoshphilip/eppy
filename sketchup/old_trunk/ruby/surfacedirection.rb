# find the angle between two planes
# returns tha anle that a plane makes with the horizontal
# test with a model that has only two planes

def surfacedirection(face)
  vect = face.normal
  hvector = Geom::Vector3d.new(0, 0, 1)
  ang = hvector.angle_between vect
  return ang
end

def toradians(ang)
  return 180 / Pi * ang
end

model=Sketchup.active_model       
selection_set = model.active_entities 

entities = []
selection_set.each {|entity|
  if entity.class == Sketchup::Face
    entities.push(entity)
  end
}


entities.each{|entity|
  ang = surfacedirection(entity)
  puts toradians(ang)  
}

