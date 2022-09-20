"""Configuration for testing

The configuration file provides several default graph fixtures
and test functions
"""


import pytest
import math
from mmodel import Model, BasicHandler, ModelGraph
from networkx.utils import nodes_equal, edges_equal


@pytest.fixture
def model(scope="Function"):
    """Mock test graph generated using ModelGraph

    The result is:
    k = (a + b - d)(a + b)f
    m = log(a + b, b)
    """

    def addition(a, b=2):
        return a + b

    def subtraction(c, d):
        return c - d

    def multiplication(c, f):
        return c * f

    def polynomial(e, g):
        return e * g

    def logarithm(c, b):
        return math.log(c, b)

    grouped_edges = [
        ("add", ["subtract", "multiply", "log"]),
        (["subtract", "multiply"], "poly"),
    ]

    node_objects = [
        ("add", addition, ["c"]),
        ("subtract", subtraction, ["e"]),
        ("multiply", multiplication, ["g"]),
        ("poly", polynomial, ["k"]),
        ("log", logarithm, ["m"]),
    ]

    G = ModelGraph(name="test")
    G.add_grouped_edges_from(grouped_edges)
    G.set_node_objects_from(node_objects)

    model = Model('test model', G, (BasicHandler, {}), description="test model")

    return model


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
    """Test if graphs have the same nodes, edges and attributes"""

    assert nodes_equal(G1._node, G2._node)
    assert edges_equal(G1._adj, G2._adj)

    assert G1._pred == G2._pred
    assert G1._succ == G2._succ

    # test graph attributes
    assert G1.graph == G2.graph
    assert G1.name == G2.name

    return True
