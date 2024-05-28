from mrfmsim.configuration import import_object, MrfmSimLoader
import pytest
import yaml
from textwrap import dedent
import numpy as np
from types import SimpleNamespace as SNs
import math


def test_import_object():
    """Load the function from the user module using dot path."""

    func = import_object("operator.add")
    assert func.__name__ == "add"
    assert func(1, 2) == 3

    func = import_object("numpy.emath.power")
    assert func.__name__ == "power"
    assert np.array_equal(func([2, 4], 2), [4, 16])


def test_import_object_error():
    """Test if it raises an error when the object is not found."""

    with pytest.raises(ModuleNotFoundError, match="Cannot import 'module.addition'."):
        import_object("module.addition")


def test_graph_constructor(experiment):
    """Test the graph constructor parsing the graph correctly."""
    graph_yaml = """
    # graph tag
    !Graph
    name: test_graph
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
            output_unit: m^2
        log:
            func: !import math.log
            output: m
            arglist: [c, b]
    """

    graph = yaml.load(dedent(graph_yaml), MrfmSimLoader)

    # Check if the two graphs are the same
    # however the function is directly parsed. Therefore
    # we can only check if the function names are the same.

    assert list(graph.nodes) == list(experiment.graph.nodes)
    assert graph.edges == graph.edges

    for nodes, attrs in graph.nodes.items():
        config_dict = attrs["node_object"].__dict__
        graph_dict = experiment.graph.nodes[nodes]["node_object"].__dict__

        assert (
            config_dict.pop("_base_func").__dict__
            == graph_dict.pop("_base_func").__dict__
        )
        assert (
            config_dict.pop("_node_func").__dict__
            == graph_dict.pop("_node_func").__dict__
        )
        assert config_dict == graph_dict


def test_func_constructor():
    """Test if it can load lambda function correctly."""

    lambda_yaml = """\
    !func:test "lambda a, b: a + b"
    """

    lambda_func = yaml.load(dedent(lambda_yaml), MrfmSimLoader)
    assert lambda_func(1, 2) == 3
    assert lambda_func.__name__ == "test"


def test_import_multi_obj_constructor():
    """Test import_multi_constructor that returns a SimpleNamespace instance."""

    dataobj_str = """
    !import:types.SimpleNamespace
    a: 1
    b: 'test'
    """

    dataobj = yaml.load(dataobj_str, MrfmSimLoader)
    assert dataobj.a == 1
    assert dataobj.b == "test"


@pytest.fixture
def expt_file(tmp_path):
    """Create a custom module for testing."""

    expt_yaml = """\
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
    """

    expt_yaml = dedent(expt_yaml)

    module_path = tmp_path / "expt.yaml"
    module_path.write_text(expt_yaml)
    return module_path


def test_parse_yaml_file(expt_file):
    """Test if the YAML file is parsed correctly."""

    with open(expt_file) as f:
        expt = yaml.load(f, MrfmSimLoader)

    assert expt.name == "test_experiment"
    assert expt.doc == "Test experiment with components."
    assert expt.graph.name == "test_graph"
    assert expt(comp=SNs(a1=1, b1=2), d_loop=[1, 2], f=2) == [
        (18, math.log(3, 2)),
        (9, math.log(3, 2)),
    ]
    assert expt(comp=SNs(a1=1, b1=2), d_loop=[1, 2], f=2, h=3) == [(48, 2), (32, 2)]
    assert expt.defaults == {"h": 2}  # check default is an int
    assert expt.get_node_object("add").doc == "Add a and h."
    assert expt.get_node_object("add").__name__ == "add"


def test_collection_constructor():
    yaml_str = """\
    !Collection
    name: test_collection
    doc: Test collection object.
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
    """

    collection = yaml.load(dedent(yaml_str), MrfmSimLoader)

    assert collection.name == "test_collection"
    assert collection.doc == "Test collection object."
    assert list(collection.nodes.keys()) == [
        "add",
        "subtract",
        "power",
        "multiply",
        "log",
    ]

    assert collection["test1"].doc == "Global docstring."
    assert collection["test1"](comp=SNs(a1=1, b1=2), d=1, f=2) == 18

    assert collection["test2"].doc == "Shortened graph."
    assert collection["test2"](comp=SNs(a1=1, b1=2), d=1, f=2) == (3, math.log(3, 2))
