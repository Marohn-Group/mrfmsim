"""Configuration for testing

The configuration file provides several default graph fixtures
and test functions
"""


import pytest
import math
from mmodel import Model, MemHandler, ModelGraph, loop_modifier
from mrfmsim.experiment import Experiment


def addition(a, b=2):
    return a + b


def subtraction(c, d):
    return c - d


def polynomial(c, f):
    return c**f


def multiplication(e, g):
    return e * g


def logarithm(c, b):
    return math.log(c, b)


@pytest.fixture
def modelgraph():
    """Model graph for creating experiment and model

    The results are:
    k = (a + b - d)(a + b)^f
    m = log(a + b, b)
    """

    grouped_edges = [
        ("add", ["subtract", "poly", "log"]),
        (["subtract", "poly"], "multiply"),
    ]

    node_objects = [
        ("add", addition, "c"),
        ("subtract", subtraction, "e"),
        ("poly", polynomial, "g"),
        ("multiply", multiplication, "k"),
        ("log", logarithm, "m"),
    ]

    G = ModelGraph(name="test")
    G.add_grouped_edges_from(grouped_edges)
    G.set_node_objects_from(node_objects)

    return G


@pytest.fixture
def model(modelgraph):
    """Create model that mimic the behavior of an experiment instance"""

    model = Model(
        "test_model",
        modelgraph,
        (MemHandler, {}),
        description="test_model",
    )

    return model


@pytest.fixture
def expt_plain(modelgraph):
    """Test experiment instance with default settings"""
    return Experiment("test_experiment_plain", modelgraph)


@pytest.fixture
def expt(modelgraph):
    """Test experiment instance with modifiers and component substitutions"""

    return Experiment(
        "test_experiment",
        modelgraph,
        component_substitutes={"component": ["a", "b"]},
        modifiers=[(loop_modifier, {"parameter": "d"})],
        description="test experiment with components",
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


def graph_equal(G1, G2):
    """Test if graphs have the same nodes, edges and attributes
    Dictionary comparison does not care about key orders
    """

    assert dict(G1.nodes) == dict(G2.nodes)
    assert dict(G1.edges) == dict(G2.edges)

    # test graph attributes
    assert G1.graph == G2.graph
    assert G1.name == G2.name

    return True
