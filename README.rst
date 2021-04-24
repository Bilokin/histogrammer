Histogrammer
============
Have you ever wanted to explore a data file without 
firing up the ``jupyter-notebook`` server and writing a 
repetitive code again and again?
If yes, then this package is right for you!

*Histogrammer* allows you to plot basic histograms from any data file 
in a fast and user-friendly manner!

Installation
------------

This is a usual python package, but it is not yet indexed in https://pypi.org/. 

However, one can install any package from git directly:

.. code-block:: bash

  pip3 install git+https://github.com/Bilokin/histogrammer.git

Usage
-----

Histogrammer supports the following formats:

 * CSV
 * `ROOT <https://www.root.cern/>`_.

This isn't much, but the list will be expanded soon.

To launch the program on a file, one has to enter the following command:

.. code-block:: bash

  python3 -m histogrammer my_file.csv

By default, the program will ask user a column name for a histogram plot.

After the histogram is displayed, user may choose to do something else with the chosen column or select a new column to plot.
