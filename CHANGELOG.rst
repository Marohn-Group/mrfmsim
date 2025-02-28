Changelog
========= 
All notable changes to this project will be documented in this file.

The format is based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to
`Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_

[0.3.0] - 2025-02-25
----------------------

Update the API to use the latest version of the mmodel package (0.8.0+).

Removed
^^^^^^^
- Remove the plugin system in favor of direct import of extension packages.
- Remove the yaml configuration functionalities to the *mrfmsim-yaml* package.
- Remove the collection module. The functionalities are moved to the group module.

Added
^^^^^
- Add Marohn group experiments. (From the previous *mrfmsim-marohn* package)

Changed
^^^^^^^

- Change the attribute names for ``Grid`` and ``Magnet`` to avoid conflicts.
- Change the component replacement behavior that requires the replacement attribute
  name is the same as the object attribute name.
- Remove "components" output in the experiment metadata. 

[0.2.0]
-------------------------

Changed
^^^^^^^
- Change python requirement to 3.10.
- Change the plugin system using package entry points. Automatically load
  plugins at import time.
- Change YAML tags for more accessible function definitions.
- Change the ``print_shortcut`` behavior to add modifiers to individual
  nodes.

Fixed
^^^^^
- Fix the issue that ``loop_shortcut`` failed to update the model "returns".

Added
^^^^^
- Add grid, magnet, sample, and cantilever component objects.
- Add custom node and model string representation.
- Add the collection class for creating a group of experiments.

Removed
^^^^^^^
- Remove the ``cli`` module to ``mrfmsim-cli`` plugin for separate     
  development.
- Remove the unit system to ``mrfmsim-units`` plugin for separate 
  development.

[0.1.1] - 2023-06-23
--------------------

Added
^^^^^
- Allow experiment configuration file to add additional node keyword arguments.

Fixed
^^^^^
- Change the ``print_shortcut`` algorithm to modify nodes instead of the model.

[0.1.0] - 2020-04-17
--------------------

The initial release of the mrfmsim framework.

Added
^^^^^
- Add the ``Experiment`` class designed for MRFM experiments.
- Add the ``Job`` class designed for MRFM execution jobs.
- Add the ``ComponentBase`` class for experiment components.
- Add ``loop_shortcut`` and ``print_shortcut`` shortcuts.
- Add ``replace_component``, ``print_inputs`` and ``print_outputs`` modifiers.
- Add command line interface.
- Add configuration module to parse experiment and job YAML files. 
- Add a plugin system that combines methods from different packages.
