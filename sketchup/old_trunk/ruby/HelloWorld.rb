#!/usr/bin/env ruby
#
#  Created by santosh on 2006-09-12.
#  Copyright (c) 2006. All rights reserved.

#Make sure this ruby file is loaded
# ("require" will load a file only if it is not loaded yet)
require "Sketchup.rb" #Make sure this ruby file is loaded

#Our hello function
def hello
    UI.messagebox("Hello World!")
end

#The function "hello" only gets run if you type in: hello
#other code gets run whenever the .rb file is loaded

# define our file name so we will know when we load it twice 
filename="HelloWorld.rb"

#run this code the first time this script is loaded
#If it is loaded again, file_loaded!(filename) will return true
if !file_loaded?(filename)
    # get the SketchUp plugins menu
    plugins_menu = UI.menu("Plugins")
    # add a seperator and our function to the "plugins" menu
    if plugins_menu
        plugins_menu.add_separator
        plugins_menu.add_item("Hello World") { hello}
    end
    # Let Ruby know we have loaded this file
    file_loaded(filename)
end