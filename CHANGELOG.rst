Changelog
========= 
All notable changes to this project will be documented in this file.

The format is based on
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_
and this project adheres to
`Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_

[Unreleased]
------------

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
- Add configuration module to parse experiment and job yaml files. 
- Add a plugin system that combines methods from different packages.
