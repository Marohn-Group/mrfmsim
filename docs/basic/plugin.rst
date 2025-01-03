Plugins
=================

Ancillary features are added to the mrfmsim ecosystem through plugin packages.
The separation of the core functionality and the plugins allows for an easy mantainance
of the mrfmsim package. The core functionalities do not depend on the plugins.

mrfmsim-ymal: YAML configuration plugin
---------------------------------------

mrfmsim classes can be fully defined using YAML configuration files. The plugin
creates a ``MrfmSimLoader`` and a ``MrfmSimDumper`` that can be used to load and
dump the mrfmsim classes to and from YAML files. For detailed usage of the package
see the `mrfmsim-ymal <https://github.com/Marohn-Group/mrfmsim-yaml>`_.

To define an experiment or experiment group with YAML files, the available tags are:
"!func", "!import", "!nodes", "!Graph", "!Experiment", and "!ExperimentGroup".

.. list-table::
   :widths: 10 40 40
   :header-rows: 1

   * - Tag
     - Usage
     - Description
   * - !func
     - !func:<name> '<expression>'
     - Define function object or expression.
   * - !import (function)
     - !import '<module>'
     - Import an object.
   * - !import (with applied arguments)
     - !import:<module> {<arg1>: <value1>, <arg2>: <value2>, ...}
     - Import an object and pass arguments to it.
   * - !nodes
     - !nodes name: {<node1>: {func: <value1>, output: <value2>, ...}, <node2>: ...}
     - Define a dictionary of node objects.
   * - !Graph
     - !Graph:<name> {grouped_edges: <value1>, node_objects: !nodes: <value2>, ...}
     - Define a graph object.
   * - !Experiment
     - !Experiment:<name> {graph: !Graph:<value1>, components: <value2>, ...}
     - Define an experiment object.
   * - !ExperimentGroup
     - !ExperimentGroup:<name> {node_objects: <value1>, ...}
     - A tag to define an experiment group object.


The following is an example of a YAML configuration file:

.. code-block:: YAML

    # experiment.yaml
    !Experiment:test_experiment
    graph: !Graph:test_graph
        grouped_edges:
        - [add, [subtract, power, log]]
        - [[subtract, power], multiply]
        node_objects: !nodes
            add:
                func: !func:add 'lambda a, h: a + h'
                output: c
            subtract:
                func: !import '_operator.sub'
                inputs: [c, d]
                output: e
            power:
                func: !import 'math.pow'
                inputs: [c, f]
                output: g
            log:
                func: !import 'math.log'
                inputs: [c, b]
                output: m
            multiply:
                func: !import 'numpy.multiply'
                inputs: [e, g]
                output: k
                output_unit: m^2
        graph_type: mrfmsim
    components:
        replace_obj: [[a, a1], [b, b1]]
    modifiers: [!import:mmodel.modifier.loop_input {parameter: d}]
    doc: Test experiment with components.
    param_defaults:
        h: 2

To load the experiment:

.. code-block:: python

    from mrfmsim_yaml import MrfmSimLoader
    import yaml

    with open('experiment.yaml', 'r') as f:
        experiment = yaml.load(f, MrfmSimLoader)

    >>> print(experiment)
    test_experiment(d_loop, f, replace_obj, h=2)
    returns: (k, m)
    return_units: {'k': 'm^2'}
    graph: test_graph
    handler: MemHandler
    modifiers:
    - loop_input(parameter='d')
    components:
    - replace_obj: [['a', 'a1'], ['b', 'b1']]

    Test experiment with components.

Or to dump an experiment object to a YAML file:

.. code-block:: python

    from mrfmsim_yaml import MrfmSimDumper
    import yaml

    with open('experiment.yaml', 'w') as f:
        yaml.dump(experiment, f, Dumper=MrfmSimDumper)



mrfmsim-cli: command line interface plugin
------------------------------------------

The command line interface is provided by the `mrfmsim-cli
<https://github.com/Marohn-Group/mrfmsim-cli>`__ plugin. See readme of the
mrfmsim-cli project for more examples.

To view the CLI options::

    mrfmsim --help

To show the experiment metadata::

    mrfmsim metadata --expt name_of_exp

To draw the experiment graph::

    mrfmsim visualize --expt name_of_exp

mrfmsim-unit: unit plugin
--------------------------------

`mrfmsim-unit <https://github.com/Marohn-Group/mrfmsim-unit>`_ 
plugin is a package that handles units and unit conversions for
the *mrfmsim* base unit system. The plugin is installed by default.

The plugin is based on the `pint
<https://pint.readthedocs.io/en/stable/>`_ package, and provides
a registry with *mrfmsim* base units pre-defined. The quantity also
has quick conversion method ``to_base_units()`` to convert to the
base units.

.. code:: python

    from mrfmsim_unit.unit import MRFMUnitRegistry

    mureg = MRFMUnitRegistry()
    a = 0.1 * mureg.micrometer
    b = 1.0 * mureg.nanometer

    >>> a * b
    0.1 nm µm

    >>> (a * b).to_base_units()
    100.0 nm^2

    >>> # (a * b).to_base_units().magnitude
    >>> # (a * b).base_magnitude
    >>> (a * b).bm
    100.0

The *mrfmsim* components do not accept ``pint.Quantity``. Only the magnitude
should be supplied to the components. The plugin provides a ``getattr`` method
to access the quantity with units.

.. code:: python

    magnet = SphereMagnet(radius=50.0, mu0_Ms=1800.0, origin=[0.0, 0.0, 50.0])
    r = mureg.getattr(magnet, "radius")
    
    >>> r
    50.0 nm
    >>> r ** 2
    2500.0 nm^2


mrfmsim-plot: plot plugin
------------------------------

To facilitate the visualization of three-dimensional experiment results, for example,
the magnetic field, polarization, and signal distribution, we created the
`mrfmsim-plot <https://github.com/Marohn-Group/mrfmsim-plot>`_ plugin that provides
conversion from the experiment data to the 
`mayavi mlab <http://docs.enthought.com/mayavi/mayavi/mlab.html>`_ and 
`PyVista <https://docs.pyvista.org/version/stable/>`_ data objects.
