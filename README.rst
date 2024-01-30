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

Installation
^^^^^^^^^^^^^

*Graphviz* installation
***********************

To view the graph, Graphviz needs to be installed:
`Graphviz Installation <https://graphviz.org/download/>`_
For Windows installation, please choose "add Graphviz to the
system PATH for all users/current users" during the setup.

For macOS systems, sometimes `brew install` results
in an unexpected installation path, it is recommended to install
with conda::

    conda install -c conda-forge pygraphviz


*mrfmsim* installation
***********************

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
