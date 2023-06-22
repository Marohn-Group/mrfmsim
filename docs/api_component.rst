Component
======================

An MRFM experiment typically consists of several components, such as
a resonator, a magnet, and a sample. These components can be grouped to 
simplify the simulation input. 

.. autosummary::

    mrfmsim.component.ComponentBase

The ``ComponentBase`` class is an abstract class with a
default metadata output. The ``attrs_to_dict`` method is to output
all public attributes.

Units
-----

To display the units of the parameters, the class attribute
``_units`` should be defined when inheriting the class. See :doc:`units <api_units>` for detailed units definition.


:mod:`component` module
------------------------

.. automodule:: mrfmsim.component
    :members:
    :show-inheritance:
