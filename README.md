Eppy
====
[![PyPI](https://img.shields.io/pypi/dm/eppy.svg)](https://pypi.python.org/pypi/eppy)
 from PyPI

[![Travis](https://img.shields.io/travis/santoshphilip/eppy/master.svg)](https://travis-ci.org/santoshphilip/eppy)
 for Python 2.7 and 3.5 on Linux and OSX via Travis

[![Appveyor](https://img.shields.io/appveyor/ci/santoshphilip/eppy/master.svg)](https://ci.appveyor.com/api/projects/status/github/santoshphilip/eppy)
 for Python 2.7 and 3.5 on Windows via Appveyor

[![CodeCov](https://img.shields.io/codecov/c/github/santoshphilip/eppy/master.svg)](https://codecov.io/github/santoshphilip/eppy)
 via CodeCov

Eppy is a scripting language for EnergyPlus idf files, and EnergyPlus output files. Eppy is written in the programming language Python. As a result it takes full advantage of the rich data structure and idioms that are available in Python. You can programmatically navigate, search, and modify EnergyPlus idf files using eppy. The power of using a scripting language allows you to do the following:

- Make a large number of changes in an idf file with a few lines of eppy code.
- Use conditions and filters when making changes to an idf file
- Make changes to multiple idf files.
- Read data from the output files of a EnergyPlus simulation run.
- Based on the results of a EnergyPlus simulation run, generate the input file for the next simulation run.

So what does this matter? 
Here are some of the things you can do with eppy:


- Change construction for all north facing walls.
- Change the glass type for all windows larger than 2 square meters.
- Change the number of people in all the interior zones.
- Change the lighting power in all south facing zones.
- Change the efficiency and fan power of all rooftop units.
- Find the energy use of all the models in a folder (or of models that were run after a certain date)

You can install from :
<https://pypi.python.org/pypi/eppy/>

The documentation is at:
<http://pythonhosted.org//eppy/>

to get a quick sense of how it feels to use eppy, take a look at
<http://pythonhosted.org//eppy/Main_Tutorial.html>

