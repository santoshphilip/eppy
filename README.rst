====
eppy
====


.. image:: https://img.shields.io/pypi/v/eppy.svg
        :target: https://pypi.python.org/pypi/eppy

.. image:: https://img.shields.io/travis/santoshphilip/eppy.svg
        :target: https://travis-ci.com/santoshphilip/eppy

.. image:: https://readthedocs.org/projects/eppy/badge/?version=latest
        :target: https://eppy.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




scripting language for E+, Energyplus
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

The documentation *stable* version is at:
<http://eppy.readthedocs.io/en/master/>

The documentation *latest* version is at:
<http://eppy.readthedocs.io/en/latest/>

to get a quick sense of how it feels to use eppy, take a look at
<http://eppy.readthedocs.io/en/latest/Main_Tutorial.html>

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
