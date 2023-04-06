"""Configuration for testing

The configuration file provides several default graph fixtures
and test functions
"""


import pytest
import math
from mmodel import Model, MemHandler, ModelGraph, loop_modifier
from mrfmsim.experiment import Experiment
from textwrap import dedent
import sys


def addition(a, constant=2):
    """Add a constant to the value a."""
    return a + constant


def subtraction(c, d):
    """Subtraction operation."""
    return c - d


def power(c, f):
    """The value of c raise to the power of f."""
    return c**f


def multiplication(e, g):
    """Multiply e and g."""
    return e * g


def logarithm(c, b):
    """Logarithm operation."""
    return math.log(c, b)


@pytest.fixture
def module_script():
    """The content of a python module script."""

    module_str = '''
    # Test python script.

    import math

    def addition(a, constant=2):
        """Add a constant to the value a."""
        return a + constant


    def subtraction(c, d):
        """Subtraction operation."""
        return c - d


    def power(c, f):
        """The value of c raise to the power of f."""
        return c**f


    def multiplication(e, g):
        """Multiply e and g."""
        return e * g


    def logarithm(c, b):
        """Logarithm operation."""
        return math.log(c, b)

    '''
    return dedent(module_str)


@pytest.fixture
def modelgraph():
    """Model graph for creating experiment and model.

    The results are:
    k = (a + 2 - d)(a + 2)^f
    m = log(a + 2, b)
    """

    grouped_edges = [
        ("add", ["subtract", "power", "log"]),
        (["subtract", "power"], "multiply"),
    ]

    node_objects = [
        ("add", addition, "c"),
        ("subtract", subtraction, "e"),
        ("power", power, "g"),
        ("multiply", multiplication, "k"),
        ("log", logarithm, "m"),
    ]

    G = ModelGraph(name="test_graph")
    G.add_grouped_edges_from(grouped_edges)
    G.set_node_objects_from(node_objects)

    return G


@pytest.fixture
def experiment(modelgraph):
    """Test experiment instance with default settings."""
    return Experiment("test_experiment_plain", modelgraph)


@pytest.fixture
def experiment_mod(modelgraph):
    """Test experiment instance with modifiers and component substitutions."""

    return Experiment(
        "test_experiment",
        modelgraph,
        replace_inputs={"component": ["a", "b"]},
        modifiers=[(loop_modifier, {"parameter": "d"})],
        description="Test experiment with components.",
    )


@pytest.fixture
def units():
    return {
        "b1": {
            "unit": "[mT]",
            "format": ":.3f",
            "description": "transverse magnetic field",
        },
        "b0": {
            "unit": "[mT]",
            "format": ":.3e",
            "description": "longitudinal magnetic field",
        },
        "b_tot": {
            "unit": "[mT]",
            "format": ":.1f",
            "description": "total magnetic field",
        }
        # 'bz': {'unit': '[mT]', "format": ":.3f"}, # comment the entry for testing
    }


# External files


@pytest.fixture
def user_module(tmp_path, module_script):
    """Create a custom module for testing."""
    module_path = tmp_path / "user_module.py"
    module_path.write_text(module_script)

    yield module_path
    # runs after the test is complete
    if "user_module" in sys.modules:
        del sys.modules["user_module"]


@pytest.fixture
def expt_file(user_module, tmp_path):
    """Create a custom module for testing."""

    expt_yaml = """\
    !experiment
    user_module:
        !module
        user_module: {user_module_path}
    name: test_experiment
    graph:
        !graph
        name: test_graph
        grouped_edges:
            - [add, [subtract, power, log]]
            - [[subtract, power], multiply]
        node_objects:
            add:
                func: !import user_module.addition
                output: c
            subtract:
                func: !import user_module.subtraction
                output: e
            power:
                func: !import user_module.power
                output: g
            multiply:
                func: !import user_module.multiplication
                output: k
            log:
                func: !import user_module.logarithm
                output: m
    replace_inputs:
        component: [a, b]
    description: Test experiment with components.
    modifiers:
        - [!import mmodel.loop_modifier, {{'parameter': 'd'}}]
    """

    expt_yaml = dedent(expt_yaml).format(user_module_path=user_module)

    module_path = tmp_path / "expt.yaml"
    module_path.write_text(expt_yaml)
    return module_path


def graph_equal(G1, G2):
    """Test if graphs have the same nodes, edges, and attributes.
    Dictionary comparison does not care about key orders.
    """

    assert dict(G1.nodes) == dict(G2.nodes)
    assert dict(G1.edges) == dict(G2.edges)

    # test graph attributes
    # ModelGraph adds parser attribute, here we test if the functions
    # are the same.
    for key in G1.graph:
        if key == "parser":
            assert G1.graph[key]._parser_dict == G2.graph[key]._parser_dict
        else:
            assert G1.graph[key] == G2.graph[key]
    assert G1.name == G2.name

    return True
