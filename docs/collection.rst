Collection
===========

Often, experiments that share similar nodes in a graph. 
We can use a `Collection` object to avoid duplication to define 
the nodes and edges. In a collection, we define the "node_objects"
list to include all the node objects necessary for the experiment,
along with the collection name and description. Typically, the
experiments under collection share the same experiment parameters,
such as "component" and "modifiers". These parameters are defined
in the "settings" dictionary. 

For individual experiments, we can define the experiment parameters
in the nested "instruction" dictionary. The keys are the experiment names,
and the values are the parameter dictionary. The parameter dictionary
is required to have "grouped_edges" as a key. Additional experiment
parameters can be added, and they overwrite the "settings" dictionary.

.. code-block:: python


    from mrfmsim import ExperimentCollection

    node_objects = [
        Node("add", np.add, inputs=["a", "h"], output="c"),
        Node("subtract", operator.sub, inputs=["c", "d"], output="e"),
        Node("power", math.pow, inputs=["c", "f"], output="g"),
        Node("multiply", np.multiply, inputs=["e", "g"], output="k", output_unit="m^2"),
        Node("log", math.log, inputs=["c", "b"], output="m"),
    ]

    grouped_edges = [
        ("add", ["subtract", "power", "log"]),
        (["subtract", "power"], "multiply"),
    ]

    instruction = {"grouped_edges": grouped_edges, "doc": "Test individual docstring."}
    collection = ExperimentCollection(
        "test_collection_object",
        "Test collection description.",
        node_objects,
        {"test": instruction},
    )

The above code creates a ``Collection`` object that contains one experiment "test".

.. code-block::

    >>> print(collection)
    test_collection_object
    experiments: ['test']
    nodes: ['add', 'subtract', 'power', 'multiply', 'log']

    Test collection description.


The experiment is stored as ``Experiment`` object in the ``Collection`` object.
The experiment can be accessed the same way as a dictionary:

.. code-block::

    >>> test_experiment = collection["test"]
    >>> print(test_experiment)
    test(a, b, d, f, h)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    collection: test_collection_object
    graph: test_graph
    handler: MemHandler

    Test individual docstring.
