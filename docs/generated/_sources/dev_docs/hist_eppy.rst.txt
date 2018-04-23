History of Eppy
===============

:Author: Santosh Philip (santosh_philip at yahoo.com)

EPlusInterface
--------------

EPlusInterface is a text based interface to Energyplus. EPlusInterface is the direct ancestor to Eppy. The data structure of EPlusInterface was simple and quite robust. EPlusInterface also had good functions to read the idd file and the idf files. In principle the idd file reader of EPlusInterface was written so that it could read any version of the idd file. Eppy directly uses the file readers from EPlusInterface

.. Energyplus and python
.. `````````````````````
..
.. Around 2004 version 1 of Energyplus had been released. In an attempt to understand what Energyplus could do, I decided write a simple interface for Energyplus. I had recently discovered the programming language python, and was very impressed with how elegantly simple the language was. Python allowed me to focus on the task at hand and did not have me obsessing over "programming".
..
.. Writing an interface
.. ````````````````````
..
.. Writing good Graphic User Interface (GUI) can be a surprisingly complex design and programming task. I found a simple library that allowed me to build text based GUI. It was fairly limited in what it could do compared to a standard GUI. This suited my purposes as it let me focus on Energyplus rather than the GUI issues.