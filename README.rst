MrfmSim
=======

|GitHub version| |Unit tests|

MrfmSim is a Python package for simulating magnetic resonance force microscopy
experiments. The package is based on the
`mmodel <https://github.com/Marohn-Group/mmodel>`_
framework, with added command line interface and yaml experiment scripting
capabilities. 

The package also employs a plugin system. By calling ``load_plugin()``
function, the user can load a plugin that adds additional functionality.
It can also automatically load plugin packages with the prefix "mrfmsim_".


Quickstart
----------

Load plugin
^^^^^^^^^^^^

To load plugin run:

.. code:: python

    import mrfmsim
    mrfmsim.load_plugin()

The default plugin option attempts to load all plugins with the prefix "mrfmsim_".
The default submodules are "experiment", "modifier", "shortcut", and "component".

Command line interface
^^^^^^^^^^^^^^^^^^^^^^

Run at the terminal::

    mrfmsim

to see the command line interface help.

Installation
^^^^^^^^^^^^^

To install the package, run::

    pip install .


Tests
^^^^^

To run the tests locally::

    python -m pytest

To test in different environments::

    tox


.. |GitHub version| image:: https://badge.fury.io/gh/Marohn-Group%2Fmrfmsim.svg
   :target: https://github.com/Marohn-Group/mrfmsim

.. .. |PyPI version shields.io| image:: https://img.shields.io/pypi/v/mrfmsim.svg
..    :target: https://pypi.python.org/pypi/mrfmsim/

.. .. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/mrfmsim.svg

.. |Unit tests| image:: https://github.com/Marohn-Group/mrfmsim/actions/workflows/tox.yml/badge.svg
    :target: https://github.com/Marohn-Group/mrfmsim/actions

.. .. |Docs| image:: https://img.shields.io/badge/Documentation--brightgreen.svg
..     :target: https://github.com/Marohn-Group/mrfmsim-docs/
