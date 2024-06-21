"""Configuration for testing.

The configuration file provides several default graph fixtures
and test functions.
"""

import pytest
import math
from mmodel.modifier import loop_input
from mrfmsim import Experiment, Graph, Node
import numpy as np
import operator


@pytest.fixture
def modelgraph():
    """Model graph for creating experiment and model.

    The results are:
    k = (a + h - d)(a + h)^f
    m = log(a + h, b)

    h defaults to 2
    """

    grouped_edges = [
        ("add", ["subtract", "power", "log"]),
        (["subtract", "power"], "multiply"),
    ]

    # Lambda node object
    add = lambda a, h: a + h
    add.__expr__ = "lambda a, h: a + h"
    add.__name__ = "add"
    add_node = Node("add", add, output="c")

    node_objects = [
        add_node,
        Node("subtract", operator.sub, arglist=["c", "d"], output="e"),
        Node("power", math.pow, arglist=["c", "f"], output="g"),
        Node(
            "multiply", np.multiply, arglist=["e", "g"], output="k", output_unit="m^2"
        ),
        Node("log", math.log, arglist=["c", "b"], output="m"),
    ]

    G = Graph(name="test_graph")
    G.add_grouped_edges_from(grouped_edges)
    G.set_node_objects_from(node_objects)

    return G


@pytest.fixture
def experiment(modelgraph):
    """Test experiment instance with default settings."""
    return Experiment("test_experiment_plain", modelgraph, defaults={"h": 2})


@pytest.fixture
def experiment_mod(modelgraph):
    """Test experiment instance with modifiers and component substitutions."""

    return Experiment(
        "test_experiment",
        modelgraph,
        components={"replace_obj": [("a", "a1"), ("b", "b1")]},
        modifiers=[loop_input(parameter="d")],
        doc="Test experiment with components.",
        defaults={"h": 2},
    )
