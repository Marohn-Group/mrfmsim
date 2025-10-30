*mrfmsim* custom classes
=========================

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

``mrfmsim.graph.Graph`` changes the group "graph_module" to "mrfmsim", and
"node_type" to ``mrfmsim.node.Node``.


Experiment
-----------

The ``mrfmsim.model.Experiment`` class is a thin wrap of the ``mmodel.Model`` class.
The change is that the instantiation takes the additional dictionary
input "components", used to replace group inputs with component objects.

For example, if the model input arguments are
``["magnet_radius", "magnet_origin", "field"]``, 
and a magnet component contains the attributes "radius" and
"origin", then the magnet component can be used as a replacement
object with the argument:

.. code:: python

    components = {'magnet': ["magnet_radius", "magnet_origin"]}

The resulting model inputs are ``["magnet", "field"]``. In the event that
the target name is different from the component object attribute, a 
custom object can be defined with the matching attribute name. The design
is to allow simpler code base.

The components are not showing in the metadata output for simplicity. To
inspect the components in the experiment, use the ``components`` attribute.
To inspect the parameter that are replaced (subset of components) use the
``param_replacements`` attribute. Alternatively, customized metadata formatting
can be used.

Component objects
-------------------

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
``experiments`` and ``experiment_defaults`` alongside the parent class's
``models`` and ``model_defaults`` properties. 
