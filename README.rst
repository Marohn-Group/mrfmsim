MrfmSim
=======

|GitHub version| |Unit tests|

MrfmSim is a Python package for simulating magnetic resonance force microscopy (MRFM)
experiments. The package is based on the
`mmodel <https://github.com/Marohn-Group/mmodel>`_
framework, with added command line interface and yaml experiment scripting
capabilities. The package also employs a plugin system, all sub-packages can
be directly loaded into the ``mrfmsim`` to provide a uniform user experience.

Quickstart
----------

See documentation for detailed API documentation.

Load plugin
^^^^^^^^^^^^

To automatically load plugins run:

.. code:: python

    import mrfmsim
    mrfmsim.load_plugin()

The default plugin option attempts to load all plugins with the prefix "mrfmsim_".
The default submodules are "experiment", "modifier", "shortcut", and "component".
Users can also specify plugins and submodule attributes to load.

Configuration file
^^^^^^^^^^^^^^^^^^

To aid the portability of the experiment models, the experiment can be defined in
a YAML file, with the nodes, edges, graph and model settings. For simple jobs, a
job configuration file can be defined as well.

Command line interface
^^^^^^^^^^^^^^^^^^^^^^

Run at the terminal::

    mrfmsim --help

to see the command line interface help.

For show or draw experiments of existing experiments::

    mrfmsim --exp exp_to_show show
    mrfmsim --exp exp_to_draw draw

Use ``--expt`` for YAML experiment files. 

To execute a job::

    mrfmsim --job job_to_run execute

Experiments
^^^^^^^^^^^

See the ``mrfmsim-marohn`` for experiment examples.

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
