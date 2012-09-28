# Copyright 2006, Google Inc.

# This software is provided as an example of using the Ruby interface
# to SketchUp.

# Permission to use, copy, modify, and distribute this software for 
# any purpose and without fee is hereby granted, provided that the above
# copyright notice appear in all copies.

# THIS SOFTWARE IS PROVIDED "AS IS" AND WITHOUT ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#-----------------------------------------------------------------------------

# This file defines a number of useful utilities that are used by other
# Ruby scripts.

#-----------------------------------------------------------------------------
# These functions are used to help with adding new menu items from a
# script.  The function file_loaded? is used to tell if the file
# has already been loaded.  If it returns true, then you should not
# add new menu items.  It is useful to allow you to reload a file
# while you are testing it without having to restart SketchUp and without
# Having it add new menu items every time it is loaded.

# This array keeps track of loaded files.  It is like the Ruby variable $"
# that is set by require, but it is not set automatically.  You have
# to call file_loaded to add a filename to the array
$loaded_files = []

# Call this method to see if a file is already loaded.
def file_loaded?(filename)
    $loaded_files.include? filename
end

# Call this function at the end of a file that you are loading to
# let the system know that you have loaded it.
def file_loaded(filename)
    $loaded_files.push(filename) if not $loaded_files.include?(filename)
end

#-----------------------------------------------------------------------------
# This function will add a separator to a given menu the first
# time it is called.  It is useful for adding a separator before
# the first plugin that is added to a given menu
$menu_separator_list = []
def add_separator_to_menu(menuname)
    if( not $menu_separator_list.include?(menuname) )
        UI.menu(menuname).add_separator
        $menu_separator_list.push menuname
    end
end

# This is a wrapper for UI.inputbox.  You call it exactly the same
# as UI.inputbox.  UI.inputbox will raise an exception if it can't
# convert the string entered for one of the values into the right type.
# This method will trap the exception and display an error dialog and
# then prompt for the values again.
def inputbox(*args)
    results = nil
    begin
        results = UI.inputbox *args
    rescue
        UI.messagebox $!.message
        retry
    end
    results
end

#-----------------------------------------------------------------------------
# By default, SketchUp automatically loads (using require) all files with
# the .rb extension in the plugins directory.  This function can be used
# to automatically load all .rb files from a different directory also.  to
# use this add a call like the following to a file in the plugins directory
# require_all "MyRubyScripts"
def require_all(dirname)
    begin
        rbfiles = Dir[File.join(dirname, "*.rb")]
        $:.push dirname
        rbfiles.each {|f| require f}
    rescue
        puts "could not load files from #{dirname}"
    end
end

def add_help_menu
help_file = Sketchup.find_support_file "index.html", "Ruby/Docs/"
if( help_file )
    helpurl = "file://" + help_file
    UI.menu("Help").add_item("Ruby Help") {UI.openURL(helpurl)}
else
    puts "Cannot find help file"
end
end

# Add some Ruby specific menu items
if( not file_loaded? "sketchup.rb" )

# Add a choice to the Window menu to display the Ruby console
add_separator_to_menu("Window")
UI.menu("Window").add_item("Ruby Console") do
	Sketchup.send_action("showRubyPanel:")
end

# Add "Ruby Help" to the Help menu
help_file = Sketchup.find_support_file "index.html", "Ruby/Docs/"
if( help_file )
    helpurl = "file://" + help_file
    UI.menu("Help").add_item("Ruby Help") {UI.openURL(helpurl)}
    add_separator_to_menu("Help")
else
    puts "Cannot find help file"
end

file_loaded "sketchup.rb"
end

