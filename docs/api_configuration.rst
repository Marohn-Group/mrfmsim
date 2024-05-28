Configuration
======================

To facilitate collaboration and better visual representation,
``mrfmsim`` allows using YAML configuration files to define
experiments. The configuration files also make the experiments
more portable for sharing and archiving. 

For example, an ``Experiment`` object can be defined:

.. code-block:: yaml

    # example.yaml
    !Experiment
    name: test_experiment
    graph:
        !Graph
        name: test_graph
        grouped_edges:
            - [add, [subtract, power, log]]
            - [[subtract, power], multiply]
        node_objects:
            add:
                func: !func:add "lambda a, h: a + h"
                doc: Add a and h.
                arglist: [a, h]
                output: c
            subtract:
                func: !import operator.sub
                output: e
                arglist: [c, d]
            power:
                func: !import math.pow
                output: g
                arglist: [c, f]
            multiply:
                func: !import numpy.multiply
                output: k
                arglist: [e, g]
                output_unit: m^2
            log:
                func: !import math.log
                output: m
                arglist: [c, b]
    components: {comp: [[a, a1], [b, b1]]}
    doc: Test experiment with components.
    modifiers: [!import:mmodel.modifier.loop_input {parameter: d}]
    defaults:
        h: 2

The above YAML string is stored in the "experiment.yaml" file.
The above experiment's graph defines a model that calculates the following:

.. math::

    k = (a + h - d)(a + h)^f
    m = log(a + h, b)

The model is equivalent to the function with the modifiers and component
replacements, The h value is defaulted to 2:

.. code-block:: python

    def test_experiment(comp, d_loop, f, h=2):

        a = comp.a1
        b = comp.b1

        # the following is executed in steps
        # to show the intermediate values that the model presents
        c = a + h
        result = []
        for d in d_loop:
            e = c - d
            g = c ** f
            k = e * g
            m = log(c, b)
            result.append((k, m))
        return result

To convert the above string from YAML to a Python object:

.. code-block:: python

    import yaml
    from mrfmsim.configuration import MrfmSimLoader


    with open('experiment.yaml', 'r') as f:
        experiment = yaml.load(f, Loader=MrfmSimLoader)


If the YAML is defined as a string, read from the string directly.


The ``experiment`` object is an instance of the ``Experiment`` class.
The modifier creates a loop over the ``d`` parameter. We can print the
experiment:

.. code-block:: python

    >>> print(experiment)
    test_experiment(comp, d_loop, f, h=2)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    graph: test_graph
    handler: MemHandler
    modifiers:
    - loop_input('d')
    components:
    - comp: [['a', 'a1'], ['b', 'b1']]

    Test experiment with components.

YAML Tags
---------

YAML tags add additional functionality to the YAML parsing. For detailed usage
see `yaml tags <https://yaml.org/spec/1.2.2/#24-tags>`__. The following tags
are available in ``mrfmsim``:

- import a Python object

.. code-block:: yaml

    !import:object

- import a Python class and instantiate

.. code-block:: yaml

    !import:types.SimpleNamespace
    a: 1
    b: 2

- create a ``mmodel.Graph`` instance

.. code-block:: yaml

    !graph
    name: example_graph
    grouped_edges:
        - [add, [subtract, power, log]]
        - [[subtract, power], multiply]
    node_objects:
        add:
            func: !import numpy.add
            output: c
            arglist: [a, h]
        subtract:
            func: !import operator.sub
            output: e
            arglist: [c, d]
        power:
            func: !import math.pow
            output: g
            arglist: [c, f]
        multiply:
            func: !import numpy.multiply
            output: k
            arglist: [e, g]
        log:
            func: !import math.log
            output: m
            arglist: [c, b]

- create a Python function called "test" from an expression 

.. code-block:: yaml

    !func:test "lambda x: x+1"

- create an ``Experiment`` object

.. code-block:: yaml

    !Experiment
    name: test_experiment
    graph:
        !Graph
        name: test_graph
        grouped_edges:
            - [add, [subtract, power, log]]
            - [[subtract, power], multiply]
        node_objects:
            add:
                func: !func:add "lambda a, h: a + h"
                doc: Add a and h.
                arglist: [a, h]
                output: c
            subtract:
                func: !import operator.sub
                output: e
                arglist: [c, d]
            power:
                func: !import math.pow
                output: g
                arglist: [c, f]
            multiply:
                func: !import numpy.multiply
                output: k
                arglist: [e, g]
                output_unit: m^2
            log:
                func: !import math.log
                output: m
                arglist: [c, b]
    components: {comp: [[a, a1], [b, b1]]}
    doc: Test experiment with components.
    modifiers: [!import:mmodel.modifier.loop_input {parameter: d}]
    defaults:
        h: 2

- create a ``Collection`` object

.. code-block:: yaml

        !Collection
    name: test_collection
    description: Test collection object.
    node_objects:
        add:
            func: !func:add "lambda a, h: a + h"
            doc: Add a and h.
            arglist: [a, h]
            output: c
        subtract:
            func: !import operator.sub
            output: e
            arglist: [c, d]
        power:
            func: !import math.pow
            output: g
            arglist: [c, f]
        multiply:
            func: !import numpy.multiply
            output: k
            arglist: [e, g]
            output_unit: m^2
        log:
            func: !import math.log
            output: m
            arglist: [c, b]
    instructions:
        test1:
            grouped_edges:
                - [add, [subtract, power, log]]
                - [[subtract, power], multiply]
            returns: [k]
        test2:
            grouped_edges:
                - [add, [subtract, power, log]]
            doc: Shortened graph.
            returns: [c, m]
    settings:
        components: {comp: [[a, a1], [b, b1]]}
        doc: Global docstring.
        defaults:
            h: 2


Security
--------

Since the configuration files allow direct Python function expression
definition, there is always a risk of malicious code execution. Since
running the Python code directly to define the experiment has
the same issue, we do not consider this a significant problem. We encourage
users to inspect the code or the experiment file before executing.

:mod:`configuration` module
----------------------------

.. automodule:: mrfmsim.configuration
    :members:
    :show-inheritance:
