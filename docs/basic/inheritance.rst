Inherited classes
=================

*mrfmsim* adds additional metadata and functionalities to the *mmodel*'s 
``Node``, ``Graph``, ``Model``, and ``ModelGroup`` classes.
The inherited classes are ``Node``, ``Graph``, ``Experiment``, and ``ExperimentGroup``.
In most cases these node and models are interchangeable, however it is not recommended
to mix the classes in the experiment definition. For more details,
see the `mmodel documentation <https://marohn-group.github.io/mmodel-docs/>`__.

Node
----

``mrfmsim.node.Node`` adds additional unit output in the metadata.

Graph
-----

``mrfmsim.graph.Graph`` changes the group "graph_type" to "mrfmsim".


Experiment
-----------

The ``mrfmsim.model.Experiment`` class is a thin wrap of the ``mmodel.Model`` class.
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


Component
======================

An MRFM experiment typically consists of several components, such as
a resonator, a magnet, and a sample. The parameters and related calculations
of components can be encapsulated into an object to simplify the input
process.

The ``ComponentBase`` class is an abstract ``dataclass`` with a
formatted metadata output. It allows users to define the base unit
of a parameter as a ``dataclass`` field. Python 
`dataclass <https://docs.python.org/3.10/library/dataclasses.html>`_
is used to simplify the definition process.




ExperimentGroup
----------------

The ``mrfmsim.group.ExperimentGroup`` class adds additional properties
``epxeriments`` and ``epxeriment_defaults`` alongside the parent class's
``models`` and ``model_defaults`` properties. 
