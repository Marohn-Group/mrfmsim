Command Line Interface
======================

``mrfmsim`` provide quick command line actions for the plugins.

To see the commands and options::

    mrfmsim --help

To list all available plugins::

    mrfmsim --show-plugins

Specifically, the interface takes two stages, first to load the experiment,
and then execute related commands.

Load Experiment
^^^^^^^^^^^^^^^

The experiments can be loaded in two ways:

- Load experiments from plugin using ``--exp exp_to_load``.

  - The ``--plugin`` option is to specify which plugin package to load.
  - The ``--attr`` option is to specify which attribute to load from the plugin.
    
    - The default attribute is "experiment", "shortcut", "modifier", and "component".

- Load experiments from YAML file using ``--expfile exp_file``.

Execute Command
^^^^^^^^^^^^^^^

The command should follow after loading the experiment::

    mrfmsim --exp exp_to_load command

The available commands are:

- ``execute``: execute the job (job defined using ``--job job_file`` option).
- ``draw``: draw the experiment model graph.
- ``show``: show the experiment model metadata.
- ``template``: create a template job file based on the experiment.

.. :mod:`cli` module
.. ----------------------

.. .. automodule:: mrfmsim.cli
..     :members:
..     :show-inheritance:
