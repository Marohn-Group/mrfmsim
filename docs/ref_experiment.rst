Experiment
======================

The ``Experiment`` class is a thin wrap of the ``mmodel.Model`` class.
The change is that the instantiation takes the additional dictionary
input "components", used to replace group inputs with component objects.

For example, if the model input arguments are
``["radius", "origin", "field"]``, 
and a magnet component contains the attributes "radius" and
"origin", then the magnet component can be used as a replacement
object with the argument:

.. code:: python

    components = {'magnet': ["radius", "origin"]}

The resulting model inputs are ``["magnet", "field"]``.

The ``Experiment`` class shares the same functionalities as the ``mmodel.Model``,
such as creating a new model with the ``edit`` method. For more details
see the `mmodel documentation <https://marohn-group.github.io/mmodel-docs/>`__.

:mod:`model` module
----------------------

.. automodule:: mrfmsim.model.Experiment
    :members:
    :show-inheritance:
