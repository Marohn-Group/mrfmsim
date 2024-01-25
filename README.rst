MrfmSim
=======

|GitHub version| |Unit tests| |DOI|

MrfmSim is a Python framework for simulating magnetic resonance force microscopy (MRFM)
experiments. The package is based on the
`mmodel <https://marohn-group.github.io/mmodel-docs/>`_ framework, which provides
modular modeling capabilities for the experiments. The framework offers additional
functionalities for interacting and modifying the experiment models, for example,
scripting using YAML files, creating optimized loops, printing out intermediate
results, and grouping experiments using experiment collections. The package also
provides various features through the plugin system, including a command line interface,
unit system, and three-dimensional plotting capabilities. The detailed API and the
available plugins are `documented <https://marohn-group.github.io/mrfmsim-docs/>`__.

Quickstart
----------

Selected features
^^^^^^^^^^^^^^^^^

Load plugins
****************

The ``mrfmsim`` package searches for all packages with the prefix "mrfmsim\_" and
loads them as plugins.

Configuration file
********************

To aid the portability of the experiment models, the experiment can be defined in
a YAML file, with the nodes, edges, graph and model settings. To execute the model
directly in the terminal, job configuration can be used to define the job.

Experiments and Collections
********************************

The `mrfmsim-marohn
<https://marohn-group.github.io/mrfmsim-marohn-docs/>`__ plugin is
required to access the Marohn group experiments. The plugin contains
individual experiments and experiment collections.

Command line interface
************************

The command line interface is provided by the `mrfmsim-cli
<https://github.com/Marohn-Group/mrfmsim-cli>`__ plugin.

Run at the terminal::

    mrfmsim --help

to see the command line interface help.

To show the experiment metadata::

    mrfmsim --exp name_of_exp metadata

To draw the experiment graph::

    mrfmsim --exp name_of_exp visualize

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

.. |DOI| image:: https://zenodo.org/badge/534295792.svg
   :target: https://zenodo.org/badge/latestdoi/534295792
