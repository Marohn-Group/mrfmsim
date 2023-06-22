Experiment
======================

The ``Experiment`` class is a thin wrap of the ``mmodel.Model`` class.
The change is that the instantiation takes the additional dictionary
input "replace_inputs", used to replace group inputs with component objects.

For example, if the model input arguments are
["magnet_radius", "magnet_origin", "field"], 
and a magnet component contains the attributes "magnet_radius" and
"magnet_origin", then the magnet component can be used as a replacement
object with the argument::

    replace_inputs = {'magnet': ["magnet_radius", "magnet_origin"]}

The resulting model inputs are ["magnet", "field"].

The ``Experiment`` class shares the same functionalities as the ``mmodel.Model``,
such as creating a new model with the ``edit`` method. For more details
see the `mmodel documentation <https://marohn-group.github.io/mmodel-docs/>`__.

:mod:`model` module
----------------------

.. automodule:: mrfmsim.model
    :members:
    :show-inheritance:
