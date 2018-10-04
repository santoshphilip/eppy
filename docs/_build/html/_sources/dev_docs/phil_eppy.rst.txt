Philosophy of Eppy
==================

:Author: Santosh Philip

The *Philosophy of eppy* alludes to the `Unix Philosophy <http://en.wikipedia.org/wiki/Unix_philosophy>`_. The philosophy of eppy takes inspiration from the *Unix Philosophy*, that speaks of doing one thing and doing it well. Unix has the tradition of having small tools that do a single thing. A number of tools can be stitched together to do a more complex task.   
Of course, since eppy is written in Python, it adheres to the "Zen of Python" 

The rules of Unix are shown in the appendix at the bottom of this page.(You may find that eppy breaks the rules at times)



Purpose of Eppy
---------------

The purpose of eppy is to be a *scripting language* to Energyplus. So what does that mean ? Let us start by describing what it is not.

What eppy is **not**:

- Eppy is **not** a User Interface to Energyplus.
- Eppy is **not** a HVAC builder for Energyplus
- Eppy is **not** a Geometry builder for Energyplus
- Eppy does **not** make batch runs for Energyplus
- Eppy does **not** optimize Energyplus models

Now you may ask, "What use is eppy, if it cannot do any of these things ?"

Aha ! Eppy is a scripting language. That means you can write scripts that can help to do any of those things listed above. And many more that are not listed above :-)

A scripting language has to be *simple* and *expressive*. It has to be simple so that it is easy to understand and use, and should ideally have a negligible learning curve. Now, it can be simple, but may be simplistic and you may be able to do only simple things in it. To go beyond the simple, the language has to be expressive. Most natural languages (like English or Malayalam) are  expressive and you can write poetry in them. Of course, some languages are more expressive than others, which is why Malayalam is more poetic than English ... just kidding here :-)

In the world of programming languages, python is a very expressive language. If you doubt this, you should take a look at the *Zen of Python* to see the philosophy behind python. Eppy attempts to piggyback on the expressiveness of python. Developers who are working on eppy should use this as a guiding principle, especially if you are working deep within the innards of eppy. Some of this is tricky coding, because you are overriding the functionality within python itself. Depending on your coding ability and what you want to learn, you should pick an area you want to work in 

**Question**: You claim that Eppy is **not** a HVAC builder for Energyplus. I see a module called hvacbulider.py in eppy.

**Answer**: Yup ! you are right. I cheated. Hvacbulider should not be in eppy. We are at an early stage of the evolution of eppy and it made sense to keep it within eppy for now. In the future, it will be made into a standalone library that will use eppy for it's functionality. 

The power of the idd file
`````````````````````````

Due to historic reasons, the developers of Energyplus were tasked to write the simulation engine without an user interface. This meant they had to write Energyplus in such a way that others could write user interfaces to it. This constraint forced them to make two excellent design decisions:

- All models in Energyplus are text files called *idf* files. Text files are human readable and are platform agnostic. 
- There is a special text file called an *idd* file, that describes all the objects that can be in an Energyplus model. Again this file is human readable and it is very well documented with comments. If you intend to do any development in Energyplus or eppy, it is well worth taking a look at this file. It is usually called *Energy+.idd* and is found in the main Energyplus folder
- When newer versions of Energyplus are released, an updated idd file is released with it. The simulation engine within Energyplus uses the idd file to parse the objects in the model. If an interface software is able to read and understand the idd file, it can effectively understand any idf file.
- Eppy is written so that it can read and understand idd files, including idd files of future releases.In principle, eppy should be able to work with any future version of Energyplus without any changes. At the date this documentation was written, eppy can read all idf files, from version 1 to version 8. 

Idd file and eppy
-----------------

Both the idd file and idf file are text files. If you look at these files, you will see that there is a clear structure that is visible to you, the reader. Eppy reads these text files and pushes it into classic python data structures, like lists and dictionaries. Once this information is in lists and dicts, it becomes much easier to walk through the data structure and to add, delete and change the information.

At it's heart, eppy is simply a scripting language that puts the idd and idf file into a python data structure. Then it uses the power of python to edit the idf file.


Appendix: Unix Philosophy
-------------------------

From http://www.catb.org/esr/writings/taoup/html/ch01s06.html:

- Rule of Modularity: Write simple parts connected by clean interfaces.
- Rule of Clarity: Clarity is better than cleverness.
- Rule of Composition: Design programs to be connected to other programs.
- Rule of Separation: Separate policy from mechanism; separate interfaces from engines.
- Rule of Simplicity: Design for simplicity; add complexity only where you must.
- Rule of Parsimony: Write a big program only when it is clear by demonstration that nothing else will do.
- Rule of Transparency: Design for visibility to make inspection and debugging easier.
- Rule of Robustness: Robustness is the child of transparency and simplicity.
- Rule of Representation: Fold knowledge into data so program logic can be stupid and robust.
- Rule of Least Surprise: In interface design, always do the least surprising thing.
- Rule of Silence: When a program has nothing surprising to say, it should say nothing.
- Rule of Repair: When you must fail, fail noisily and as soon as possible.
- Rule of Economy: Programmer time is expensive; conserve it in preference to machine time.
- Rule of Generation: Avoid hand-hacking; write programs to write programs when you can.
- Rule of Optimization: Prototype before polishing. Get it working before you optimize it.
- Rule of Diversity: Distrust all claims for “one true way”.
- Rule of Extensibility: Design for the future, because it will be here sooner than you think.
