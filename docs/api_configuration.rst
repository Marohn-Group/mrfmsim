Configuration
======================

To facilitate collaboration and better visual representation,
``mrfmsim`` allows using YAML configuration files to define
experiments. 

Here we create 
For example, a simple model and graph can be defined::

    # example.yaml
    !import:mrfmsim.model.Experiment
    name: example_experiment
    graph:
        !graph
        name: example_graph
        grouped_edges:
            - [add, [subtract, power, log]]
            - [[subtract, power], multiply]
        node_objects:
            add:
                func: !import numpy.add
                output: c
                inputs: [a, [constant, 2]]
            subtract:
                func: !import operator.sub
                output: e
                inputs: [c, d]
            power:
                func: !import math.pow
                output: g
                inputs: [c, f]
            multiply:
                func: !import numpy.multiply
                output: k
                inputs: [e, g]
            log:
                func: !import math.log
                output: m
                inputs: [c, b]
    replace_inputs: {component: [a, b]}
    description: Example experiment with components.
    modifiers: [!import:mmodel.modifier.loop_input {parameter: d}]

The above experiment defines a model that calculates the following:

.. math:: 
    k = (a + 2 - d)(a + 2)^f
    m = log(a + 2, b)

To convert the file from YAML to a Python object::

    import yaml
    from mrfmsim.configuration import MrfmSimLoader

    with open('example.yaml', 'r') as f:
        experiment = yaml.load(f, Loader=MrfmSimLoader)

The ``experiment`` object is an instance of the ``Experiment`` class.
The modifier creates a loop over the ``d`` parameter. We can print the
experiment::

    >>> print(experiment)
    >>> test_experiment(component, d, f)
        returns: (k, m)
        graph: test_graph
        handler: MemHandler
        modifiers:
        - loop_input('d')
        - replace_component({'component': ['a', 'b']})

        Example experiment with components.

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

- create a ``mmodel.ModelGraph`` instance

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
                inputs: [a, [constant, 2]]
            subtract:
                func: !import operator.sub
                output: e
                inputs: [c, d]
            power:
                func: !import math.pow
                output: g
                inputs: [c, f]
            multiply:
                func: !import numpy.multiply
                output: k
                inputs: [e, g]
            log:
                func: !import math.log
                output: m
                inputs: [c, b]

- generate a Python function from an expression

    .. code-block:: yaml

        !func "lambda x: x+1"

- execute a function input parameter using lambda expression

    .. code-block:: yaml

        !execute func(arguments)

    is equivalent to

    .. code-block:: python

        def outerfunc(func, arguments):
            return func(arguments)
    
    and 

    .. code-block:: yaml

        !execute func(*arguments)

    is equivalent to

    .. code-block:: python

        def outerfunc(func, arguments):
            return func(*arguments)

    This is used to simplify the definition process.

Security
--------

Since the configuration files allow direct Python function expression
definition, there is always a risk of malicious code execution. Since
the case of running directly Python code to define the experiment has
the same issue, we do not consider this a major issue. We encourage
users to always inspect the code or the experiment file before executing.

:mod:`configuration` module
----------------------------

.. automodule:: mrfmsim.configuration
    :members:
    :show-inheritance:
